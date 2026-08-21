from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Response
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..database import get_db
from ..auth import require_admin_key

router = APIRouter(prefix="/peptides", tags=["peptides"])


# --- Public reads ------------------------------------------------------------
# Both endpoints below are public and only ever return `status: published`
# entries — the app should never see drafts. They support two complementary
# incremental-sync mechanisms: an ETag/If-None-Match pair for a cheap "has
# anything changed" check, and an `updated_since` query param (list endpoint
# only) for pulling just the rows that changed instead of the full list.

def _naive(dt: Optional[datetime]) -> Optional[datetime]:
    return dt.replace(tzinfo=None) if dt and dt.tzinfo else dt


@router.get("", response_model=List[schemas.PeptideListItem])
def list_peptides(
    updated_since: Optional[datetime] = None,
    response: Response = None,
    if_none_match: Optional[str] = Header(default=None),
    db: Session = Depends(get_db),
):
    peptides = db.query(models.Peptide).filter(models.Peptide.status == "published").all()

    if updated_since is not None:
        cutoff = _naive(updated_since)
        peptides = [p for p in peptides if p.updated_at and _naive(p.updated_at) > cutoff]

    latest = max((p.updated_at for p in peptides), default=None)
    etag = f'W/"{len(peptides)}-{latest.isoformat() if latest else "empty"}"'

    if response is not None:
        response.headers["ETag"] = etag
        if latest:
            response.headers["Last-Modified"] = str(latest)

    if if_none_match == etag:
        return Response(status_code=304, headers={"ETag": etag})

    return [
        schemas.PeptideListItem(
            id=p.id,
            name=p.name,
            status=p.status,
            categories=[schemas.LookupOut(id=c.id, name=c.name) for c in p.categories],
            overview=p.overview,
            aliases=crud._loads(p.aliases),
        )
        for p in peptides
    ]


@router.get("/{peptide_id}", response_model=schemas.PeptideOut)
def get_peptide(
    peptide_id: str,
    response: Response = None,
    if_none_match: Optional[str] = Header(default=None),
    db: Session = Depends(get_db),
):
    p = db.get(models.Peptide, peptide_id)
    if not p or p.status != "published":
        raise HTTPException(404, "Peptide not found")

    etag = f'W/"{p.updated_at.isoformat() if p.updated_at else "unknown"}"'
    if response is not None:
        response.headers["ETag"] = etag

    if if_none_match == etag:
        return Response(status_code=304, headers={"ETag": etag})

    return crud.build_peptide_out(db, p)


# --- Admin writes (require X-Admin-Key header) --------------------------------

@router.post("", response_model=schemas.PeptideOut, dependencies=[Depends(require_admin_key)])
def create_peptide(payload: schemas.PeptideCreate, db: Session = Depends(get_db)):
    if db.get(models.Peptide, payload.id):
        raise HTTPException(409, f"Peptide id '{payload.id}' already exists")

    p = models.Peptide(id=payload.id, name=payload.name, status=payload.status)
    try:
        crud.apply_scalar_fields(p, payload.dict())
        crud.set_category_links(db, p, payload.category_ids)
        crud.set_injection_site_links(db, p, payload.quick_start_guide.injection_site_ids)
    except ValueError as e:
        raise HTTPException(400, str(e))

    db.add(p)
    db.flush()  # so peptide_id FK is valid for protocols below
    crud.replace_research_protocols(db, p, payload.research_protocols)
    db.commit()
    db.refresh(p)
    return crud.build_peptide_out(db, p)


@router.put("/{peptide_id}", response_model=schemas.PeptideOut, dependencies=[Depends(require_admin_key)])
def update_peptide(peptide_id: str, payload: schemas.PeptideUpdate, db: Session = Depends(get_db)):
    p = db.get(models.Peptide, peptide_id)
    if not p:
        raise HTTPException(404, "Peptide not found")

    data = payload.dict(exclude_unset=True)
    try:
        crud.apply_scalar_fields(p, data)
        if data.get("category_ids") is not None:
            crud.set_category_links(db, p, data["category_ids"])
        if data.get("quick_start_guide", {}).get("injection_site_ids") is not None:
            crud.set_injection_site_links(db, p, data["quick_start_guide"]["injection_site_ids"])
        if data.get("research_protocols") is not None:
            crud.replace_research_protocols(db, p, payload.research_protocols)
    except ValueError as e:
        raise HTTPException(400, str(e))

    db.commit()
    db.refresh(p)
    return crud.build_peptide_out(db, p)


@router.patch("/{peptide_id}/status", response_model=schemas.PeptideOut, dependencies=[Depends(require_admin_key)])
def patch_status(peptide_id: str, payload: schemas.StatusPatch, db: Session = Depends(get_db)):
    p = db.get(models.Peptide, peptide_id)
    if not p:
        raise HTTPException(404, "Peptide not found")
    p.status = payload.status
    db.commit()
    db.refresh(p)
    return crud.build_peptide_out(db, p)


@router.delete("/{peptide_id}", dependencies=[Depends(require_admin_key)])
def delete_peptide(peptide_id: str, db: Session = Depends(get_db)):
    p = db.get(models.Peptide, peptide_id)
    if not p:
        raise HTTPException(404, "Peptide not found")
    db.delete(p)
    db.commit()
    return {"deleted": peptide_id}


# --- Interactions --------------------------------------------------------------

@router.post(
    "/{peptide_id}/interactions",
    response_model=schemas.PeptideInteractionOut,
    dependencies=[Depends(require_admin_key)],
)
def add_interaction(peptide_id: str, payload: schemas.PeptideInteractionIn, db: Session = Depends(get_db)):
    if not db.get(models.Peptide, peptide_id):
        raise HTTPException(404, "Peptide not found")
    if not db.get(models.Peptide, payload.related_peptide_id):
        raise HTTPException(400, f"Unknown related_peptide_id: {payload.related_peptide_id}")

    interaction = models.PeptideInteraction(
        peptide_id=peptide_id,
        related_peptide_id=payload.related_peptide_id,
        note=payload.note,
        severity=payload.severity,
    )
    db.add(interaction)
    db.commit()

    other = db.get(models.Peptide, payload.related_peptide_id)
    return schemas.PeptideInteractionOut(
        related_peptide_id=payload.related_peptide_id,
        related_peptide_name=other.name if other else None,
        note=payload.note,
        severity=payload.severity,
    )
