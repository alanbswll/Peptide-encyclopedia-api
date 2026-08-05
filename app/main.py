from fastapi import FastAPI

from .database import Base, engine
from .routers import peptides
from .routers.lookups import categories_router, injection_sites_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Peptide Encyclopedia API",
    description="Backend for the Bio Hacker app's peptide encyclopedia — lets new "
                 "peptides be added without an app store release.",
    version="1.0.0",
)

app.include_router(peptides.router)
app.include_router(categories_router)
app.include_router(injection_sites_router)


@app.get("/health")
def health():
    return {"status": "ok"}
