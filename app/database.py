import os
from sqlalchemy import create_engine
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
