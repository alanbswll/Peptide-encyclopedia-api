from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..auth import require_admin_key

router = APIRouter(tags=["lookups"])


def _make_lookup_router(model, prefix: str, kind: str) -> APIRouter:
    r = APIRouter(prefix=prefix, tags=["lookups"])

    @r.get("", response_model=List[schemas.LookupOut])
    def list_items(db: Session = Depends(get_db)):
        return db.query(model).order_by(model.name).all()

    @r.post("", response_model=schemas.LookupOut, dependencies=[Depends(require_admin_key)])
    def create_item(payload: schemas.LookupCreate, db: Session = Depends(get_db)):
        if db.get(model, payload.id):
            raise HTTPException(409, f"{kind} id '{payload.id}' already exists")
        obj = model(id=payload.id, name=payload.name)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @r.delete("/{item_id}", dependencies=[Depends(require_admin_key)])
    def delete_item(item_id: str, db: Session = Depends(get_db)):
        obj = db.get(model, item_id)
        if not obj:
            raise HTTPException(404, f"{kind} not found")
        # Will raise an IntegrityError if still referenced by a peptide (ON DELETE RESTRICT) —
        # that's intentional: you shouldn't be able to delete a category still in use.
        db.delete(obj)
        db.commit()
        return {"deleted": item_id}

    return r


categories_router = _make_lookup_router(models.Category, "/categories", "category")
injection_sites_router = _make_lookup_router(models.InjectionSite, "/injection-sites", "injection_site")
