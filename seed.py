"""
Run once against a fresh database to populate the controlled vocabularies
and one example peptide:

    python seed.py
"""
from app.database import SessionLocal, Base, engine
from app import models

Base.metadata.create_all(bind=engine)
db = SessionLocal()

CATEGORIES = [
    ("healing", "Healing"),
    ("gut-health", "Gut Health"),
    ("growth-hormone", "Growth Hormone"),
    ("fat-loss", "Fat Loss"),
    ("cognitive", "Cognitive"),
    ("longevity", "Longevity"),
    ("immune", "Immune Support"),
]

INJECTION_SITES = [
    ("abdomen-subq", "Abdomen (subcutaneous)"),
    ("thigh-subq", "Thigh (subcutaneous)"),
    ("glute-im", "Glute (intramuscular)"),
    ("deltoid-im", "Deltoid (intramuscular)"),
    ("near-injury", "Near injury site (subcutaneous)"),
]

for id_, name in CATEGORIES:
    if not db.get(models.Category, id_):
        db.add(models.Category(id=id_, name=name))

for id_, name in INJECTION_SITES:
    if not db.get(models.InjectionSite, id_):
        db.add(models.InjectionSite(id=id_, name=name))

db.commit()

if not db.get(models.Peptide, "bpc-157"):
    p = models.Peptide(
        id="bpc-157",
        name="BPC-157",
        status="published",
        overview="A synthetic peptide derived from a protective protein found in gastric juice.",
        mechanism_of_action="Promotes angiogenesis and modulates growth factor pathways.",
        qsg_typical_dose="250\u2013500 mcg",
        qsg_frequency="1\u20132x daily",
        qsg_best_timing="On an empty stomach",
        qsg_effects_timeline="Initial effects in 1\u20132 weeks; full benefit over 4\u20136 weeks",
        qsg_storage="Refrigerate after reconstitution; use within 30 days",
        qsg_cycle_length="4\u20136 weeks",
        qsg_break_between="2\u20134 weeks",
        pk_peak="~1 hour",
        pk_half_life="~4 hours (est., limited human data)",
        pk_cleared="~24 hours",
        what_to_expect="Most users report no acute sensation; healing benefits are gradual over weeks, not days.",
        safety_notes="Limited long-term human safety data exists. Consult a healthcare provider.",
    )
    p.categories = [db.get(models.Category, "healing"), db.get(models.Category, "gut-health")]
    p.injection_sites = [db.get(models.InjectionSite, "abdomen-subq"), db.get(models.InjectionSite, "near-injury")]
    db.add(p)
    db.flush()
    db.add(models.ResearchProtocol(
        peptide_id=p.id, goal="Tendon/Ligament Recovery", dose="250 mcg 2x daily",
        timing="Morning and evening",
        disclaimer="For research purposes only. Not evaluated by the FDA.",
    ))
    db.commit()

print("Seed complete.")
db.close()
