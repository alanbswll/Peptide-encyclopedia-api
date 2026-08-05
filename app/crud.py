import json
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import or_

from . import models, schemas


def _loads(value: Optional[str]) -> list:
    return json.loads(value) if value else []


def _dumps(value: list) -> str:
    return json.dumps(value or [])


def get_lookup_or_404(db: Session, model, id_: str, kind: str):
    obj = db.get(model, id_)
    if not obj:
        raise ValueError(f"Unknown {kind} id: {id_}")
    return obj


def build_peptide_out(db: Session, p: models.Peptide) -> schemas.PeptideOut:
    interactions = (
        db.query(models.PeptideInteraction)
        .filter(
            or_(
                models.PeptideInteraction.peptide_id == p.id,
                models.PeptideInteraction.related_peptide_id == p.id,
            )
        )
        .all()
    )
    interaction_out = []
    for i in interactions:
        other_id = i.related_peptide_id if i.peptide_id == p.id else i.peptide_id
        other = db.get(models.Peptide, other_id)
        interaction_out.append(
            schemas.PeptideInteractionOut(
                related_peptide_id=other_id,
                related_peptide_name=other.name if other else None,
                note=i.note,
                severity=i.severity,
            )
        )

    return schemas.PeptideOut(
        id=p.id,
        name=p.name,
        status=p.status,
        categories=[schemas.LookupOut(id=c.id, name=c.name) for c in p.categories],
        overview=p.overview,
        key_benefits=_loads(p.key_benefits),
        mechanism_of_action=p.mechanism_of_action,
        quick_start_guide=schemas.QuickStartGuide(
            typical_dose=p.qsg_typical_dose,
            frequency=p.qsg_frequency,
            injection_site_ids=[s.id for s in p.injection_sites],
            best_timing=p.qsg_best_timing,
            effects_timeline=p.qsg_effects_timeline,
            storage=p.qsg_storage,
            cycle_length=p.qsg_cycle_length,
            break_between=p.qsg_break_between,
        ),
        pharmacokinetics=schemas.Pharmacokinetics(
            peak=p.pk_peak, half_life=p.pk_half_life, cleared=p.pk_cleared
        ),
        research_protocols=[
            schemas.ResearchProtocolOut(
                id=rp.id, goal=rp.goal, dose=rp.dose, timing=rp.timing,
                disclaimer=rp.disclaimer, sort_order=rp.sort_order,
            )
            for rp in sorted(p.research_protocols, key=lambda r: r.sort_order)
        ],
        research_indications=_loads(p.research_indications),
        peptide_interactions=interaction_out,
        reconstitution_steps=_loads(p.reconstitution_steps),
        quality_indicators=_loads(p.quality_indicators),
        what_to_expect=p.what_to_expect,
        side_effects_common=_loads(p.side_effects_common),
        safety_notes=p.safety_notes,
        references=[schemas.ReferenceItem(**r) for r in _loads(p.references)],
        schema_version=p.schema_version,
        created_at=str(p.created_at) if p.created_at else None,
        updated_at=str(p.updated_at) if p.updated_at else None,
    )


def apply_scalar_fields(peptide: models.Peptide, data: dict) -> None:
    """Map flat + nested-dict update fields onto the ORM row's flat columns."""
    simple_map = {
        "name": "name",
        "status": "status",
        "overview": "overview",
        "mechanism_of_action": "mechanism_of_action",
        "what_to_expect": "what_to_expect",
        "safety_notes": "safety_notes",
    }
    for src, dest in simple_map.items():
        if src in data and data[src] is not None:
            setattr(peptide, dest, data[src])

    json_map = {
        "key_benefits": "key_benefits",
        "research_indications": "research_indications",
        "reconstitution_steps": "reconstitution_steps",
        "quality_indicators": "quality_indicators",
        "side_effects_common": "side_effects_common",
    }
    for src, dest in json_map.items():
        if src in data and data[src] is not None:
            setattr(peptide, dest, _dumps(data[src]))

    if "references" in data and data["references"] is not None:
        peptide.references = _dumps([r if isinstance(r, dict) else r.dict() for r in data["references"]])

    qsg = data.get("quick_start_guide")
    if qsg:
        qsg = qsg if isinstance(qsg, dict) else qsg.dict()
        peptide.qsg_typical_dose = qsg.get("typical_dose", peptide.qsg_typical_dose)
        peptide.qsg_frequency = qsg.get("frequency", peptide.qsg_frequency)
        peptide.qsg_best_timing = qsg.get("best_timing", peptide.qsg_best_timing)
        peptide.qsg_effects_timeline = qsg.get("effects_timeline", peptide.qsg_effects_timeline)
        peptide.qsg_storage = qsg.get("storage", peptide.qsg_storage)
        peptide.qsg_cycle_length = qsg.get("cycle_length", peptide.qsg_cycle_length)
        peptide.qsg_break_between = qsg.get("break_between", peptide.qsg_break_between)

    pk = data.get("pharmacokinetics")
    if pk:
        pk = pk if isinstance(pk, dict) else pk.dict()
        peptide.pk_peak = pk.get("peak", peptide.pk_peak)
        peptide.pk_half_life = pk.get("half_life", peptide.pk_half_life)
        peptide.pk_cleared = pk.get("cleared", peptide.pk_cleared)


def set_category_links(db: Session, peptide: models.Peptide, category_ids: List[str]) -> None:
    peptide.categories = [
        get_lookup_or_404(db, models.Category, cid, "category") for cid in category_ids
    ]


def set_injection_site_links(db: Session, peptide: models.Peptide, site_ids: List[str]) -> None:
    peptide.injection_sites = [
        get_lookup_or_404(db, models.InjectionSite, sid, "injection_site") for sid in site_ids
    ]


def replace_research_protocols(db: Session, peptide: models.Peptide, protocols) -> None:
    for rp in list(peptide.research_protocols):
        db.delete(rp)
    peptide.research_protocols = [
        models.ResearchProtocol(
            peptide_id=peptide.id,
            goal=rp.goal if hasattr(rp, "goal") else rp["goal"],
            dose=rp.dose if hasattr(rp, "dose") else rp["dose"],
            timing=rp.timing if hasattr(rp, "timing") else rp.get("timing"),
            disclaimer=rp.disclaimer if hasattr(rp, "disclaimer") else rp.get("disclaimer"),
            sort_order=rp.sort_order if hasattr(rp, "sort_order") else rp.get("sort_order", 0),
        )
        for rp in protocols
    ]
