# Peptide Encyclopedia API

Standalone backend service for the Bio Hacker app's peptide encyclopedia. Lets you add or
edit peptides by hitting an API — no app build, no store review.

This is a **separate project/service** from the Bio Hacker Android app and from AB Signal.
Deployed independently on Render with its own database.

See [`SCHEMA.md`](./SCHEMA.md) for the full finalized data model, design rationale, and
example JSON shapes.

## Stack

- FastAPI + SQLAlchemy
- SQLite on a Render Persistent Disk (same pattern as AB Signal)
- API-key-gated admin writes; open reads for published entries

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env             # then edit ADMIN_API_KEY to a real secret
python seed.py                   # creates peptides.db, seeds lookup tables + one example peptide

uvicorn app.main:app --reload
python scripts/load_all.py       # loads every peptide from peptides_source/*.yaml
```

API docs (interactive): http://127.0.0.1:8000/docs

## Project layout

```
app/
  main.py              FastAPI app + router registration
  database.py           SQLAlchemy engine/session
  models.py              ORM models (peptides, protocols, interactions, lookup tables)
  schemas.py            Pydantic request/response models
  crud.py                  Assembly logic: ORM <-> JSON columns <-> response objects
  auth.py                  X-Admin-Key header check for write routes
  routers/
    peptides.py        GET/POST/PUT/PATCH/DELETE for peptides + interactions
    lookups.py          GET/POST/DELETE for categories and injection sites
seed.py                Populate lookup tables + one example peptide
render.yaml            Render deployment config (web service + persistent disk)
```

## Auth

Admin (write) routes require an `X-Admin-Key` header matching `ADMIN_API_KEY`. Public GET
routes are open and only ever return `status: published` entries by default.

```bash
curl -X POST https://your-service.onrender.com/peptides \
  -H "X-Admin-Key: $ADMIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d @new_peptide.json
```

## Endpoints

| Method | Path                              | Auth  | Purpose                                  |
|--------|------------------------------------|-------|-------------------------------------------|
| GET    | `/peptides`                       | none  | List peptides (default: published only)  |
| GET    | `/peptides/{id}`                  | none  | Full peptide detail                       |
| POST   | `/peptides`                       | admin | Create a peptide (defaults to draft)      |
| PUT    | `/peptides/{id}`                  | admin | Update fields                             |
| PATCH  | `/peptides/{id}/status`           | admin | Flip draft \u2194 published                    |
| DELETE | `/peptides/{id}`                  | admin | Remove a peptide                          |
| POST   | `/peptides/{id}/interactions`     | admin | Add an interaction to another peptide     |
| GET/POST | `/categories`                   | mixed | List / add a category                     |
| GET/POST | `/injection-sites`               | mixed | List / add an injection site              |

## Adding a peptide (content workflow)

Peptide content lives as YAML files in `peptides_source/` — this gives you git history
on the encyclopedia content itself, and YAML is much easier to hand-write or review
than raw JSON.

1. Copy `peptides_source/_template.yaml` to `peptides_source/<slug>.yaml` and fill it in.
   Check `GET /categories` and `GET /injection-sites` for valid lookup IDs.
2. Push it as a draft:
   ```bash
   python scripts/add_peptide.py peptides_source/<slug>.yaml --api-url https://your-service.onrender.com
   ```
3. Review it — either open the URL the script prints, or check it in `/docs`.
4. Publish it:
   ```bash
   python scripts/publish_peptide.py <slug> --api-url https://your-service.onrender.com
   ```
5. Commit the YAML file to git so the content change has history alongside the code.

To edit an existing peptide, update its YAML file and re-run `add_peptide.py` with `--update`.

To pull a published peptide back for edits without deleting it: `publish_peptide.py <slug> --draft`.

Interactions between two peptides aren't in the YAML flow yet (they reference another
peptide by ID, so both sides need to exist first) — add them with a direct call:
```bash
curl -X POST $API_URL/peptides/<slug>/interactions \
  -H "X-Admin-Key: $ADMIN_API_KEY" -H "Content-Type: application/json" \
  -d '{"related_peptide_id": "<other-slug>", "note": "...", "severity": "synergistic"}'
```

## The database is disposable — `peptides_source/` is the real backup

The SQLite database is treated as a rebuildable cache, not the source of truth. Every
peptide that exists lives as a YAML file in `peptides_source/`, committed to git. If the
Render disk is ever lost, corrupted, or you migrate hosts, the full encyclopedia comes
back with:

```bash
python seed.py                   # lookup tables (categories, injection sites)
python scripts/load_all.py       # upserts every peptide from peptides_source/*.yaml
```

`load_all.py` is idempotent — safe to re-run any time (e.g. after editing several YAML
files at once) since it creates what's missing and updates what already exists.

## Deploying

1. Push this repo to GitHub.
2. In Render: New → Blueprint → point at the repo (picks up `render.yaml` automatically).
3. Set `ADMIN_API_KEY` in the Render dashboard environment settings (not committed to git).
4. After first deploy, run `python seed.py` via a Render Shell session to seed the persistent disk.

## Status

Scaffolded from the finalized v2 schema. Not yet deployed — see the "Encyclopedia Remote
Backend" list on the Peptide tracker Trello board for the remaining setup/deploy/Android-side
work.
