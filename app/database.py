import os
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base

# On Render, point this at a file on the mounted Persistent Disk, e.g.
# DATABASE_URL=sqlite:////var/data/peptides.db
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./peptides.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def ensure_additive_columns() -> None:
    """
    Base.metadata.create_all() only creates tables that don't exist yet -- it never
    ALTERs an existing table to add a newly-declared column. There's no Alembic here
    (see README), so new nullable/defaulted columns on already-live tables (like
    `peptides.aliases`) need this tiny manual migration instead, or every query
    against the ORM model fails with "no such column" against the persisted disk.

    Safe to run on every startup: only adds a column if it's actually missing.
    """
    inspector = inspect(engine)
    for table in Base.metadata.tables.values():
        if not inspector.has_table(table.name):
            continue
        existing_columns = {col["name"] for col in inspector.get_columns(table.name)}
        for column in table.columns:
            if column.name in existing_columns:
                continue
            col_type = column.type.compile(engine.dialect)
            default_clause = ""
            if column.default is not None and column.default.is_scalar:
                default_clause = f" DEFAULT {column.default.arg!r}"
            with engine.begin() as conn:
                conn.execute(text(f'ALTER TABLE "{table.name}" ADD COLUMN "{column.name}" {col_type}{default_clause}'))
