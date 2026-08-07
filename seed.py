"""
Run once against a fresh database to populate the controlled vocabularies
(categories, injection sites). Peptide content itself is NOT seeded here —
it lives in peptides_source/*.yaml and gets loaded via scripts/load_all.py,
so the database can always be fully rebuilt from what's in git.

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
    ("sexual-health", "Sexual Health"),
    ("sleep", "Sleep & Relaxation"),
    ("skin", "Skin & Anti-Aging"),
    ("bone", "Bone & Structural Health"),
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
print("Lookup tables seeded (categories, injection sites).")
print("Now load peptide content: uvicorn app.main:app (in another terminal), then")
print("  python scripts/load_all.py")
db.close()
