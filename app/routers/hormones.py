from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..auth import require_admin_key

router = APIRouter(prefix="/hormones", tags=["lookups"])


@router.get("", response_model=List[schemas.HormoneOut])
def list_hormones(db: Session = Depends(get_db)):
    return db.query(models.Hormone).order_by(models.Hormone.name).all()


@router.post("", response_model=schemas.HormoneOut, dependencies=[Depends(require_admin_key)])
def create_hormone(payload: schemas.HormoneCreate, db: Session = Depends(get_db)):
    if db.get(models.Hormone, payload.id):
        raise HTTPException(409, f"hormone id '{payload.id}' already exists")
    obj = models.Hormone(id=payload.id, name=payload.name, unit=payload.unit, group=payload.group)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{item_id}", dependencies=[Depends(require_admin_key)])
def delete_hormone(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.Hormone, item_id)
    if not obj:
        raise HTTPException(404, "hormone not found")
    db.delete(obj)
    db.commit()
    return {"deleted": item_id}
