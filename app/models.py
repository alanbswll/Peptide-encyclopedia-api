import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column, String, Text, ForeignKey, CheckConstraint, UniqueConstraint, DateTime, Integer, Table
)
from sqlalchemy.orm import relationship

from .database import Base


def new_id(prefix: str = "") -> str:
    return f"{prefix}{uuid.uuid4().hex[:12]}"


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


# --- Controlled vocabularies ---------------------------------------------

class Category(Base):
    __tablename__ = "categories"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, unique=True)


class InjectionSite(Base):
    __tablename__ = "injection_sites"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, unique=True)


class Hormone(Base):
    __tablename__ = "hormones"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    unit = Column(String, nullable=False)
    group = Column(String, nullable=False)  # e.g. "androgen", "estrogen", "pituitary"


peptide_categories = Table(
    "peptide_categories",
    Base.metadata,
    Column("peptide_id", String, ForeignKey("peptides.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", String, ForeignKey("categories.id", ondelete="RESTRICT"), primary_key=True),
)

peptide_injection_sites = Table(
    "peptide_injection_sites",
    Base.metadata,
    Column("peptide_id", String, ForeignKey("peptides.id", ondelete="CASCADE"), primary_key=True),
    Column("injection_site_id", String, ForeignKey("injection_sites.id", ondelete="RESTRICT"), primary_key=True),
)


# --- Core peptide ----------------------------------------------------------

class Peptide(Base):
    __tablename__ = "peptides"

    id = Column(String, primary_key=True)  # slug, e.g. "bpc-157"
    name = Column(String, nullable=False)
    status = Column(String, nullable=False, default="draft")  # 'draft' | 'published'

    overview = Column(Text)
    key_benefits = Column(Text, default="[]")  # JSON array of strings
    aliases = Column(Text, default="[]")       # JSON array of strings (vendor label name variants)
    mechanism_of_action = Column(Text)

    # Quick start guide
    qsg_typical_dose = Column(Text)
    qsg_frequency = Column(Text)
    qsg_best_timing = Column(Text)
    qsg_effects_timeline = Column(Text)
    qsg_storage = Column(Text)
    qsg_cycle_length = Column(Text)
    qsg_break_between = Column(Text)

    # Pharmacokinetics
    pk_peak = Column(Text)
    pk_half_life = Column(Text)
    pk_cleared = Column(Text)

    research_indications = Column(Text, default="[]")  # JSON array of strings
    reconstitution_steps = Column(Text, default="[]")  # JSON array of ordered strings
    quality_indicators = Column(Text, default="[]")    # JSON array of strings
    what_to_expect = Column(Text)

    side_effects_common = Column(Text, default="[]")   # JSON array of strings
    safety_notes = Column(Text)

    references = Column(Text, default="[]")  # JSON array of {citation, url}

    schema_version = Column(Integer, nullable=False, default=2)
    created_at = Column(DateTime, default=now_utc)
    updated_at = Column(DateTime, default=now_utc, onupdate=now_utc)

    categories = relationship("Category", secondary=peptide_categories)
    injection_sites = relationship("InjectionSite", secondary=peptide_injection_sites)
    research_protocols = relationship(
        "ResearchProtocol", back_populates="peptide", cascade="all, delete-orphan"
    )


class ResearchProtocol(Base):
    __tablename__ = "research_protocols"

    id = Column(String, primary_key=True, default=lambda: new_id("proto_"))
    peptide_id = Column(String, ForeignKey("peptides.id", ondelete="CASCADE"), nullable=False)
    goal = Column(String, nullable=False)
    dose = Column(String, nullable=False)
    timing = Column(Text)
    disclaimer = Column(Text)
    sort_order = Column(Integer, default=0)

    peptide = relationship("Peptide", back_populates="research_protocols")


class PeptideInteraction(Base):
    __tablename__ = "peptide_interactions"
    __table_args__ = (
        CheckConstraint("severity IN ('synergistic', 'caution', 'avoid')", name="ck_interaction_severity"),
        UniqueConstraint("peptide_id", "related_peptide_id", name="uq_interaction_pair"),
    )

    id = Column(String, primary_key=True, default=lambda: new_id("int_"))
    peptide_id = Column(String, ForeignKey("peptides.id", ondelete="CASCADE"), nullable=False)
    related_peptide_id = Column(String, ForeignKey("peptides.id", ondelete="CASCADE"), nullable=False)
    note = Column(Text)
    severity = Column(String, nullable=False)
