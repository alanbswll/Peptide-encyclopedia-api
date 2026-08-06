"""
Run once against a fresh database to populate the controlled vocabularies,
migrate the legacy in-app peptide list, and seed one richly-detailed example
peptide:

    python seed.py
"""
import json
import re

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

# --- Migrate legacy in-app peptide list -----------------------------------
# Source: Bio Hacker Tracker Android app, AppPreferences.kt `defaultPeptides()`.
# That app-side model only has 5 free-text fields (name, description,
# mixingDetails, useDetails, category) -- far simpler than this schema. Per
# the Trello migration card, everything is imported as `published` and mapped
# onto the closest matching fields; the richer fields (mechanism of action,
# pharmacokinetics, research protocols, interactions, etc.) don't exist in
# the source data and are left blank for admins to fill in later.
# BPC-157 is skipped here since it already has the hand-authored entry above.


def slugify(name: str) -> str:
    slug = name.lower().replace("+", " plus ")
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


LEGACY_CATEGORY_TO_ID = {
    "Healing & Recovery": "healing",
    "Growth Hormone & Growth Factors": "growth-hormone",
    "Metabolic & Weight Management": "fat-loss",
    "Cognitive & Neuroprotective": "cognitive",
    "Longevity & Cellular Health": "longevity",
    "Sexual Health": "sexual-health",
    "Immune & Inflammation": "immune",
    "Sleep & Relaxation": "sleep",
    "Skin & Anti-Aging": "skin",
    "Bone & Structural Health": "bone",
}

# (name, description, mixingDetails, useDetails, category)
LEGACY_PEPTIDES = [
    ("TB-500", "Recovery and flexibility", "Reconstitute carefully and keep a consistent schedule.", "Popular for connective tissue support", "Healing & Recovery"),
    ("KPV", "Anti-inflammatory tripeptide", "Stable in solution; refrigerate after mixing.", "Explored for gut and skin inflammation", "Healing & Recovery"),
    ("ARA-290", "Tissue-protective erythropoietin fragment (Cibinetide)", "Reconstitute with bacteriostatic water; keep cold.", "Studied for nerve pain and tissue protection", "Healing & Recovery"),
    ("TB-500 (Frag)", "Active fragment of Thymosin Beta-4", "Reconstitute with bacteriostatic water; refrigerate.", "Explored for angiogenesis and localized tissue repair", "Healing & Recovery"),
    ("Wolverine Stack", "BPC-157 and TB-500 combination blend", "Reconstitute with bacteriostatic water; refrigerate.", "Popular combined stack for joint and tissue recovery", "Healing & Recovery"),
    ("GLOW Blend", "BPC-157, GHK-Cu, and TB-500 combination blend", "Reconstitute with bacteriostatic water; refrigerate.", "Marketed for skin, gut, and tissue repair together", "Healing & Recovery"),
    ("KLOW Blend", "BPC-157, GHK-Cu, TB-500, and KPV combination blend", "Reconstitute with bacteriostatic water; refrigerate.", "Marketed for skin, gut, and inflammation support together", "Healing & Recovery"),

    ("CJC-1295", "Growth hormone support", "Use only under professional guidance.", "Complex dosing and timing", "Growth Hormone & Growth Factors"),
    ("Ipamorelin", "Selective growth hormone secretagogue", "Reconstitute with bacteriostatic water and refrigerate.", "Often paired with CJC-1295", "Growth Hormone & Growth Factors"),
    ("GHRP-2", "Growth hormone releasing peptide", "Mix with bacteriostatic water; store cold.", "Stimulates appetite and GH release", "Growth Hormone & Growth Factors"),
    ("GHRP-6", "Growth hormone releasing peptide with strong appetite stimulation", "Mix with bacteriostatic water; store cold.", "Older-generation secretagogue", "Growth Hormone & Growth Factors"),
    ("Sermorelin", "GHRH analog", "Reconstitute gently; avoid shaking.", "Supports natural GH pulse pattern", "Growth Hormone & Growth Factors"),
    ("Tesamorelin", "GHRH analog studied for visceral fat reduction", "Reconstitute with supplied diluent; refrigerate.", "Requires consistent daily timing", "Growth Hormone & Growth Factors"),
    ("Hexarelin", "Potent GH secretagogue", "Mix with bacteriostatic water; store cold.", "Can desensitize with prolonged use", "Growth Hormone & Growth Factors"),
    ("IGF-1 LR3", "Long-acting insulin-like growth factor", "Reconstitute carefully; use within the recommended window.", "Short window of activity once mixed", "Growth Hormone & Growth Factors"),
    ("MGF", "IGF-1 splice variant (Mechano Growth Factor)", "Mix immediately before use; unstable in solution.", "Explored for localized muscle repair", "Growth Hormone & Growth Factors"),
    ("PEG-MGF", "PEGylated Mechano Growth Factor", "Mix immediately before use; unstable in solution.", "Longer-acting alternative to standard MGF", "Growth Hormone & Growth Factors"),
    ("ACE-031", "Myostatin-blocking fusion protein", "Reconstitute per supplier instructions; refrigerate.", "Explored for muscle preservation and strength", "Growth Hormone & Growth Factors"),
    ("CJC-1295 (with DAC)", "Extended-release GHRH analog with Drug Affinity Complex", "Reconstitute with bacteriostatic water; refrigerate.", "Longer half-life than no-DAC CJC-1295; less frequent dosing", "Growth Hormone & Growth Factors"),
    ("CJC-1295 + Ipamorelin", "Combined GHRH/ghrelin-mimetic secretagogue stack", "Reconstitute with bacteriostatic water; refrigerate.", "Common paired stack for GH pulse support", "Growth Hormone & Growth Factors"),
    ("HGH", "Recombinant human growth hormone", "Reconstitute per supplier instructions; refrigerate.", "Requires professional guidance and monitoring", "Growth Hormone & Growth Factors"),
    ("HGH Frag 176-191", "Fat-burning fragment of human growth hormone", "Reconstitute with bacteriostatic water; refrigerate.", "Studied specifically for subcutaneous fat reduction", "Growth Hormone & Growth Factors"),

    ("AOD-9604", "Fat-loss support", "Use with a clear titration plan.", "Best tracked with body composition notes", "Metabolic & Weight Management"),
    ("Semaglutide", "GLP-1 receptor agonist", "Reconstitute per manufacturer instructions; refrigerate.", "Weekly dosing schedule typical", "Metabolic & Weight Management"),
    ("Tirzepatide", "Dual GIP/GLP-1 receptor agonist", "Reconstitute per manufacturer instructions; refrigerate.", "Weekly dosing schedule typical", "Metabolic & Weight Management"),
    ("Retatrutide", "Triple GIP/GLP-1/glucagon receptor agonist", "Reconstitute per manufacturer instructions; refrigerate.", "Newer-generation metabolic peptide", "Metabolic & Weight Management"),
    ("Cagrilintide", "Long-acting amylin analog", "Reconstitute per manufacturer instructions; refrigerate.", "Often studied alongside GLP-1 agonists", "Metabolic & Weight Management"),
    ("Liraglutide", "GLP-1 receptor agonist", "Reconstitute per manufacturer instructions; refrigerate.", "Daily dosing typical; shorter-acting than newer GLP-1 agonists", "Metabolic & Weight Management"),
    ("Survodutide", "Dual GLP-1/glucagon receptor agonist", "Reconstitute per manufacturer instructions; refrigerate.", "Studied for weight loss and liver health", "Metabolic & Weight Management"),
    ("5-Amino-1MQ", "NNMT enzyme inhibitor", "Often supplied oral; follow supplier instructions.", "Explored for fat metabolism and NAD+ support", "Metabolic & Weight Management"),
    ("Adipotide", "Fat-cell vasculature targeting compound", "Reconstitute per supplier instructions; refrigerate.", "Early-stage research compound for visceral fat", "Metabolic & Weight Management"),
    ("AICAR", "AMPK-activating compound", "Reconstitute per supplier instructions; refrigerate.", "Studied for endurance and insulin sensitivity", "Metabolic & Weight Management"),
    ("L-Carnitine", "Amino-acid derivative supporting fat transport", "Often supplied pre-mixed; refrigerate.", "Commonly paired with fat-loss protocols for energy support", "Metabolic & Weight Management"),
    ("Lipo-B", "Injectable lipotropic B-vitamin blend", "Typically supplied pre-mixed; refrigerate.", "Marketed for fat metabolism and energy support", "Metabolic & Weight Management"),
    ("Lipo-C", "Injectable lipotropic blend with vitamin C", "Typically supplied pre-mixed; refrigerate.", "Marketed for fat metabolism, liver, and energy support together", "Metabolic & Weight Management"),
    ("Lipo-C Fat Blaster", "Injectable lipotropic blend", "Typically supplied pre-mixed; refrigerate.", "Marketed fat-burning blend combining lipotropic agents", "Metabolic & Weight Management"),
    ("Super Shred", "Advanced fat-burning injectable blend", "Typically supplied pre-mixed; refrigerate.", "Marketed combination blend for fat burning and energy", "Metabolic & Weight Management"),

    ("Semax", "Nootropic peptide derived from ACTH", "Often used intranasally; keep refrigerated.", "Studied for focus and cognitive support", "Cognitive & Neuroprotective"),
    ("Selank", "Anxiolytic peptide related to tuftsin", "Often used intranasally; keep refrigerated.", "Studied for stress and anxiety support", "Cognitive & Neuroprotective"),
    ("Dihexa", "Neurogenic compound studied for synaptic health", "Follow supplier handling instructions.", "Long half-life relative to other nootropic peptides", "Cognitive & Neuroprotective"),
    ("Cerebrolysin", "Neuropeptide preparation studied for cognitive recovery", "Typically supplied pre-mixed; refrigerate.", "Usually administered in cycles", "Cognitive & Neuroprotective"),
    ("Pinealon", "Short peptide bioregulator", "Reconstitute with bacteriostatic water; refrigerate.", "Explored for brain aging support", "Cognitive & Neuroprotective"),
    ("P21", "Neurogenesis-promoting peptide", "Reconstitute with bacteriostatic water; refrigerate.", "Explored for memory and new neuron growth", "Cognitive & Neuroprotective"),
    ("Adamax", "Adamantane-modified nootropic peptide", "Reconstitute with bacteriostatic water; refrigerate.", "Studied for memory and focus support", "Cognitive & Neuroprotective"),
    ("PE 22-28", "BDNF-pathway peptide", "Reconstitute with bacteriostatic water; refrigerate.", "Explored for mood and emotional balance", "Cognitive & Neuroprotective"),
    ("VIP", "Vasoactive Intestinal Peptide", "Reconstitute with bacteriostatic water; refrigerate.", "Studied for neuroprotection and immune modulation", "Cognitive & Neuroprotective"),
    ("Semax + Selank Blend", "Combined Semax and Selank blend (10mg + 10mg)", "Often used intranasally; keep refrigerated.", "Paired dosing for focus and stress support together", "Cognitive & Neuroprotective"),

    ("Epithalon", "Telomerase-activating tetrapeptide", "Reconstitute with bacteriostatic water; refrigerate.", "Typically used in short cycles", "Longevity & Cellular Health"),
    ("MOTS-c", "Mitochondrial-derived peptide", "Reconstitute with bacteriostatic water; refrigerate.", "Studied for metabolic and exercise adaptation", "Longevity & Cellular Health"),
    ("Humanin", "Mitochondrial-derived peptide with cytoprotective effects", "Reconstitute with bacteriostatic water; refrigerate.", "Early-stage longevity research interest", "Longevity & Cellular Health"),
    ("SS-31", "Mitochondria-targeted peptide (Elamipretide)", "Reconstitute with bacteriostatic water; refrigerate.", "Studied for mitochondrial function support", "Longevity & Cellular Health"),
    ("FOXO4-DRI", "Senolytic peptide", "Reconstitute with bacteriostatic water; refrigerate.", "Early-stage cellular senescence research", "Longevity & Cellular Health"),
    ("Thymalin", "Thymus-derived peptide bioregulator", "Reconstitute with bacteriostatic water; refrigerate.", "Studied for immune regulation and longevity", "Longevity & Cellular Health"),
    ("Vilon", "Thymus-derived dipeptide bioregulator", "Reconstitute with bacteriostatic water; refrigerate.", "Studied alongside Thymalin for longevity support", "Longevity & Cellular Health"),
    ("NAD+", "Coenzyme central to cellular energy metabolism (not a peptide)", "Reconstitute per supplier instructions; refrigerate.", "Declines with age; explored for cellular energy and DNA repair", "Longevity & Cellular Health"),
    ("Glutathione", "Tripeptide master antioxidant", "Reconstitute per supplier instructions; refrigerate.", "Studied for detoxification, immune function, and skin brightening", "Longevity & Cellular Health"),

    ("PT-141", "Melanocortin receptor agonist (Bremelanotide)", "Reconstitute with bacteriostatic water; refrigerate.", "Studied for sexual desire support", "Sexual Health"),
    ("Melanotan II", "Melanocortin agonist", "Reconstitute with bacteriostatic water; refrigerate.", "Explored for tanning and libido effects", "Sexual Health"),
    ("Kisspeptin-10", "Reproductive hormone regulator", "Reconstitute with bacteriostatic water; refrigerate.", "Studied for hormonal axis signaling", "Sexual Health"),
    ("Gonadorelin", "GnRH analog", "Reconstitute with bacteriostatic water; refrigerate.", "Studied for LH/FSH stimulation and fertility support", "Sexual Health"),
    ("HCG", "Human Chorionic Gonadotropin (not a peptide)", "Reconstitute per supplier instructions; refrigerate.", "Studied for fertility and testosterone support", "Sexual Health"),
    ("HMG", "Human Menopausal Gonadotropin (not a peptide)", "Reconstitute per supplier instructions; refrigerate.", "Studied for fertility hormone stimulation", "Sexual Health"),

    ("Thymosin Alpha-1", "Immune-modulating peptide", "Reconstitute with bacteriostatic water; refrigerate.", "Studied for immune system support", "Immune & Inflammation"),
    ("LL-37", "Antimicrobial host-defense peptide", "Reconstitute with bacteriostatic water; refrigerate.", "Studied for antimicrobial and wound support", "Immune & Inflammation"),
    ("Thymogen", "Immune-modulating dipeptide", "Reconstitute with bacteriostatic water; refrigerate.", "Studied for immune regulation", "Immune & Inflammation"),

    ("DSIP", "Delta sleep-inducing peptide", "Reconstitute with bacteriostatic water; refrigerate.", "Studied for sleep quality support", "Sleep & Relaxation"),

    ("GHK-Cu", "Copper-binding tripeptide", "Sensitive to light; store cold and shielded.", "Popular in skin and hair research", "Skin & Anti-Aging"),
    ("Melanotan I", "Melanocortin agonist (Afamelanotide)", "Reconstitute with bacteriostatic water; refrigerate.", "Studied for photoprotection", "Skin & Anti-Aging"),
    ("AHK-Cu", "Copper peptide variant of GHK-Cu", "Sensitive to light; store cold and shielded.", "Explored for hair growth and scalp repair", "Skin & Anti-Aging"),
    ("SNAP-8", "Topical octapeptide", "Typically supplied as a topical formulation.", "Marketed for reducing expression lines", "Skin & Anti-Aging"),
    ("Matrixyl", "Palmitoyl pentapeptide-4", "Typically supplied as a topical formulation.", "Marketed for collagen production and firmness", "Skin & Anti-Aging"),
    ("Botulinum Toxin", "Muscle-relaxing neurotoxin (not a peptide)", "Administered by a licensed provider; not self-mixed.", "Used for expression lines and wrinkle reduction", "Skin & Anti-Aging"),
    ("Hyaluronic Acid", "Hydrating glycosaminoglycan (not a peptide)", "Topical or injectable per product instructions.", "Used for hydration, plumpness, and joint cushioning", "Skin & Anti-Aging"),

    ("Teriparatide", "PTH-derived peptide", "Reconstitute per manufacturer instructions; refrigerate.", "FDA-approved for osteoporosis and bone density support", "Bone & Structural Health"),
]

for name, description, mixing, use, category_label in LEGACY_PEPTIDES:
    id_ = slugify(name)
    if db.get(models.Peptide, id_):
        continue
    p = models.Peptide(
        id=id_,
        name=name,
        status="published",
        overview=description,
        key_benefits=json.dumps([use]),
        reconstitution_steps=json.dumps([mixing]) if mixing else "[]",
    )
    p.categories = [db.get(models.Category, LEGACY_CATEGORY_TO_ID[category_label])]
    db.add(p)

db.commit()

print("Seed complete.")
db.close()
