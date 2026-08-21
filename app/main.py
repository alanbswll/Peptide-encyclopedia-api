from fastapi import FastAPI

from .database import Base, engine, ensure_additive_columns
from .routers import peptides
from .routers.lookups import categories_router, injection_sites_router
from .routers.hormones import router as hormones_router

Base.metadata.create_all(bind=engine)
ensure_additive_columns()

app = FastAPI(
    title="Peptide Encyclopedia API",
    description="Backend for the Bio Hacker app's peptide encyclopedia — lets new "
                 "peptides be added without an app store release.",
    version="1.0.0",
)

app.include_router(peptides.router)
app.include_router(categories_router)
app.include_router(injection_sites_router)
app.include_router(hormones_router)


@app.get("/health")
def health():
    return {"status": "ok"}
