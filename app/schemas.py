from typing import List, Optional, Literal
from pydantic import BaseModel, Field

Severity = Literal["synergistic", "caution", "avoid"]
Status = Literal["draft", "published"]


# --- Lookup vocab -----------------------------------------------------------

class LookupOut(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True


class LookupCreate(BaseModel):
    id: str
    name: str


# --- Nested pieces -----------------------------------------------------------

class QuickStartGuide(BaseModel):
    typical_dose: Optional[str] = None
    frequency: Optional[str] = None
    injection_site_ids: List[str] = Field(default_factory=list)
    best_timing: Optional[str] = None
    effects_timeline: Optional[str] = None
    storage: Optional[str] = None
    cycle_length: Optional[str] = None
    break_between: Optional[str] = None


class Pharmacokinetics(BaseModel):
    peak: Optional[str] = None
    half_life: Optional[str] = None
    cleared: Optional[str] = None


class ReferenceItem(BaseModel):
    citation: str
    url: Optional[str] = None


class ResearchProtocolIn(BaseModel):
    goal: str
    dose: str
    timing: Optional[str] = None
    disclaimer: Optional[str] = None
    sort_order: int = 0


class ResearchProtocolOut(ResearchProtocolIn):
    id: str

    class Config:
        from_attributes = True


class PeptideInteractionIn(BaseModel):
    related_peptide_id: str
    note: Optional[str] = None
    severity: Severity


class PeptideInteractionOut(BaseModel):
    related_peptide_id: str
    related_peptide_name: Optional[str] = None
    note: Optional[str] = None
    severity: Severity


# --- Peptide -----------------------------------------------------------------

class PeptideCreate(BaseModel):
    id: str  # slug, e.g. "bpc-157"
    name: str
    status: Status = "draft"
    category_ids: List[str] = Field(default_factory=list)

    overview: Optional[str] = None
    key_benefits: List[str] = Field(default_factory=list)
    mechanism_of_action: Optional[str] = None

    quick_start_guide: QuickStartGuide = Field(default_factory=QuickStartGuide)
    pharmacokinetics: Pharmacokinetics = Field(default_factory=Pharmacokinetics)

    research_indications: List[str] = Field(default_factory=list)
    reconstitution_steps: List[str] = Field(default_factory=list)
    quality_indicators: List[str] = Field(default_factory=list)
    what_to_expect: Optional[str] = None

    side_effects_common: List[str] = Field(default_factory=list)
    safety_notes: Optional[str] = None

    references: List[ReferenceItem] = Field(default_factory=list)
    research_protocols: List[ResearchProtocolIn] = Field(default_factory=list)


class PeptideUpdate(BaseModel):
    """All fields optional — PUT sends only what's changing."""
    name: Optional[str] = None
    status: Optional[Status] = None
    category_ids: Optional[List[str]] = None

    overview: Optional[str] = None
    key_benefits: Optional[List[str]] = None
    mechanism_of_action: Optional[str] = None

    quick_start_guide: Optional[QuickStartGuide] = None
    pharmacokinetics: Optional[Pharmacokinetics] = None

    research_indications: Optional[List[str]] = None
    reconstitution_steps: Optional[List[str]] = None
    quality_indicators: Optional[List[str]] = None
    what_to_expect: Optional[str] = None

    side_effects_common: Optional[List[str]] = None
    safety_notes: Optional[str] = None

    references: Optional[List[ReferenceItem]] = None
    research_protocols: Optional[List[ResearchProtocolIn]] = None


class StatusPatch(BaseModel):
    status: Status


class PeptideOut(BaseModel):
    id: str
    name: str
    status: Status
    categories: List[LookupOut]

    overview: Optional[str] = None
    key_benefits: List[str] = Field(default_factory=list)
    mechanism_of_action: Optional[str] = None

    quick_start_guide: QuickStartGuide
    pharmacokinetics: Pharmacokinetics

    research_protocols: List[ResearchProtocolOut] = Field(default_factory=list)
    research_indications: List[str] = Field(default_factory=list)
    peptide_interactions: List[PeptideInteractionOut] = Field(default_factory=list)

    reconstitution_steps: List[str] = Field(default_factory=list)
    quality_indicators: List[str] = Field(default_factory=list)
    what_to_expect: Optional[str] = None

    side_effects_common: List[str] = Field(default_factory=list)
    safety_notes: Optional[str] = None

    references: List[ReferenceItem] = Field(default_factory=list)

    schema_version: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class PeptideListItem(BaseModel):
    """Lighter payload for GET /peptides list view."""
    id: str
    name: str
    status: Status
    categories: List[LookupOut]
    overview: Optional[str] = None
