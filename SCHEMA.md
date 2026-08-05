# Peptide Encyclopedia Schema (v2 — finalized)

## Design notes

- **`bookmarked` is client-only.** Per-user state, stored in Room on-device only — never synced to/from the API.
- **`categories` and `injection_sites` are controlled vocabularies**, not free text. Each has its own lookup table. The admin write endpoints only accept IDs from these tables — the admin UI renders them as dropdowns/multi-selects, so inconsistent entries ("Abdomen" vs "Stomach") are structurally impossible, not just discouraged by convention. Add new categories/sites by inserting a lookup row, not by typing in a peptide record.
- **`research_protocols`** — one peptide → many protocols (unchanged from v1).
- **`peptide_interactions`** — many-to-many via join table, self-referencing on `peptides`. A peptide can have any number of interactions. Directionality is handled at query time: when rendering a peptide's page, query interactions where it appears as *either* `peptide_id` or `related_peptide_id`, and merge the results. You only enter BPC-157 ↔ TB-500 once; it shows on both pages automatically.
- **`severity`** is now a locked enum — `synergistic`, `caution`, `avoid` — enforced with a `CHECK` constraint at the database level so bad values can't be inserted even by a buggy admin call.
- **`references`** stays as a simple JSON array — no relational value in normalizing citations.

---

## SQL DDL (SQLite)

```sql
CREATE TABLE peptides (
    id                      TEXT PRIMARY KEY,          -- e.g. slug: "bpc-157"
    name                    TEXT NOT NULL,
    status                  TEXT NOT NULL DEFAULT 'draft', -- 'draft' | 'published'

    overview                TEXT,
    key_benefits            TEXT DEFAULT '[]',          -- JSON array of strings
    mechanism_of_action     TEXT,

    -- Quick start guide
    qsg_typical_dose        TEXT,
    qsg_frequency           TEXT,
    qsg_best_timing         TEXT,
    qsg_effects_timeline    TEXT,
    qsg_storage             TEXT,
    qsg_cycle_length        TEXT,
    qsg_break_between       TEXT,

    -- Pharmacokinetics
    pk_peak                 TEXT,
    pk_half_life            TEXT,
    pk_cleared              TEXT,

    research_indications    TEXT DEFAULT '[]',          -- JSON array of strings

    -- Reconstitution
    reconstitution_steps    TEXT DEFAULT '[]',          -- JSON array of ordered strings

    quality_indicators      TEXT DEFAULT '[]',          -- JSON array of strings
    what_to_expect          TEXT,

    -- Side effects and safety
    side_effects_common     TEXT DEFAULT '[]',          -- JSON array of strings
    safety_notes            TEXT,

    "references"            TEXT DEFAULT '[]',          -- JSON array of {citation, url}

    schema_version          INTEGER NOT NULL DEFAULT 2,
    created_at              TEXT NOT NULL,
    updated_at              TEXT NOT NULL
);

-- Controlled vocabulary: categories
CREATE TABLE categories (
    id      TEXT PRIMARY KEY,   -- e.g. "healing"
    name    TEXT NOT NULL UNIQUE -- e.g. "Healing"
);

CREATE TABLE peptide_categories (
    peptide_id      TEXT NOT NULL REFERENCES peptides(id) ON DELETE CASCADE,
    category_id     TEXT NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    PRIMARY KEY (peptide_id, category_id)
);

-- Controlled vocabulary: injection sites
CREATE TABLE injection_sites (
    id      TEXT PRIMARY KEY,   -- e.g. "abdomen-subq"
    name    TEXT NOT NULL UNIQUE -- e.g. "Abdomen (subcutaneous)"
);

CREATE TABLE peptide_injection_sites (
    peptide_id          TEXT NOT NULL REFERENCES peptides(id) ON DELETE CASCADE,
    injection_site_id   TEXT NOT NULL REFERENCES injection_sites(id) ON DELETE RESTRICT,
    PRIMARY KEY (peptide_id, injection_site_id)
);

CREATE TABLE research_protocols (
    id              TEXT PRIMARY KEY,
    peptide_id      TEXT NOT NULL REFERENCES peptides(id) ON DELETE CASCADE,
    goal            TEXT NOT NULL,
    dose            TEXT NOT NULL,
    timing          TEXT,
    disclaimer      TEXT,
    sort_order      INTEGER DEFAULT 0
);

CREATE TABLE peptide_interactions (
    id                  TEXT PRIMARY KEY,
    peptide_id          TEXT NOT NULL REFERENCES peptides(id) ON DELETE CASCADE,
    related_peptide_id  TEXT NOT NULL REFERENCES peptides(id) ON DELETE CASCADE,
    note                TEXT,
    severity            TEXT NOT NULL CHECK (severity IN ('synergistic', 'caution', 'avoid')),
    UNIQUE (peptide_id, related_peptide_id)
);

CREATE INDEX idx_peptides_status ON peptides(status);
CREATE INDEX idx_protocols_peptide ON research_protocols(peptide_id);
CREATE INDEX idx_interactions_peptide ON peptide_interactions(peptide_id);
CREATE INDEX idx_interactions_related ON peptide_interactions(related_peptide_id);
CREATE INDEX idx_peptide_categories_peptide ON peptide_categories(peptide_id);
CREATE INDEX idx_peptide_sites_peptide ON peptide_injection_sites(peptide_id);
```

**Seed data for lookup tables** — starter sets to insert on first migration; add more via a lookup-table insert whenever you need one, never by typing into a peptide record:

```sql
INSERT INTO categories (id, name) VALUES
  ('healing', 'Healing'),
  ('gut-health', 'Gut Health'),
  ('growth-hormone', 'Growth Hormone'),
  ('fat-loss', 'Fat Loss'),
  ('cognitive', 'Cognitive'),
  ('longevity', 'Longevity'),
  ('immune', 'Immune Support');

INSERT INTO injection_sites (id, name) VALUES
  ('abdomen-subq', 'Abdomen (subcutaneous)'),
  ('thigh-subq', 'Thigh (subcutaneous)'),
  ('glute-im', 'Glute (intramuscular)'),
  ('deltoid-im', 'Deltoid (intramuscular)'),
  ('near-injury', 'Near injury site (subcutaneous)');
```

---

## API response JSON shape

`GET /peptides/{id}` — server joins the lookup tables and interaction rows back into a flat, app-friendly object:

```json
{
  "id": "bpc-157",
  "name": "BPC-157",
  "status": "published",
  "categories": [
    { "id": "healing", "name": "Healing" },
    { "id": "gut-health", "name": "Gut Health" }
  ],

  "overview": "A synthetic peptide derived from a protective protein found in gastric juice...",
  "key_benefits": [
    "Supports tendon and ligament healing",
    "May support gut lining integrity"
  ],
  "mechanism_of_action": "Promotes angiogenesis and modulates growth factor pathways...",

  "quick_start_guide": {
    "typical_dose": "250–500 mcg",
    "frequency": "1–2x daily",
    "injection_sites": [
      { "id": "abdomen-subq", "name": "Abdomen (subcutaneous)" },
      { "id": "near-injury", "name": "Near injury site (subcutaneous)" }
    ],
    "best_timing": "On an empty stomach",
    "effects_timeline": "Initial effects in 1–2 weeks; full benefit over 4–6 weeks",
    "storage": "Refrigerate after reconstitution; use within 30 days",
    "cycle_length": "4–6 weeks",
    "break_between": "2–4 weeks"
  },

  "research_protocols": [
    {
      "id": "proto_01",
      "goal": "Tendon/Ligament Recovery",
      "dose": "250 mcg 2x daily",
      "timing": "Morning and evening",
      "disclaimer": "For research purposes only. Not evaluated by the FDA."
    },
    {
      "id": "proto_02",
      "goal": "Gut Health Support",
      "dose": "500 mcg 1x daily",
      "timing": "Morning, empty stomach",
      "disclaimer": "For research purposes only. Not evaluated by the FDA."
    }
  ],

  "pharmacokinetics": {
    "peak": "~1 hour",
    "half_life": "~4 hours (est., limited human data)",
    "cleared": "~24 hours"
  },

  "research_indications": ["Tendinopathy", "IBD models", "Wound healing"],

  "peptide_interactions": [
    {
      "related_peptide_id": "tb-500",
      "related_peptide_name": "TB-500",
      "note": "Commonly stacked for synergistic healing effects",
      "severity": "synergistic"
    }
  ],

  "how_to_reconstitute": {
    "steps": [
      "Wipe vial top with alcohol swab",
      "Draw bacteriostatic water into syringe",
      "Inject slowly down the side of the vial — do not spray directly onto powder",
      "Gently swirl, do not shake, until fully dissolved"
    ]
  },

  "quality_indicators": [
    "Third-party COA available from vendor",
    "Powder is white/off-white and fully dissolves clear"
  ],

  "what_to_expect": "Most users report no acute sensation; healing benefits are gradual over weeks, not days.",

  "side_effects_and_safety": {
    "common_side_effects": ["Mild injection site redness", "Rare headache"],
    "safety_notes": "Limited long-term human safety data exists. Consult a healthcare provider."
  },

  "references": [
    {
      "citation": "Sikiric et al., stable gastric pentadecapeptide BPC 157",
      "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8844085/"
    }
  ],

  "schema_version": 2,
  "created_at": "2026-08-05T00:00:00Z",
  "updated_at": "2026-08-05T00:00:00Z"
}
```

---

## Admin write payload for controlled fields

When creating/editing a peptide, the admin endpoint accepts **IDs**, not free text, for categories and injection sites:

```json
{
  "name": "BPC-157",
  "category_ids": ["healing", "gut-health"],
  "quick_start_guide": {
    "injection_site_ids": ["abdomen-subq", "near-injury"],
    "typical_dose": "250–500 mcg"
  }
}
```

If an ID doesn't exist in the lookup table, the API rejects the write with a 400 — this is what makes the controlled vocabulary actually enforced rather than just a suggestion. New categories/sites get added via a small `POST /categories` / `POST /injection-sites` admin endpoint, which you'd only call when a genuinely new one is needed.

## Status: resolved

All three open questions from v1 are settled. This schema is ready to scaffold into FastAPI/SQLAlchemy models.
