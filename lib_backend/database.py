from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib_backend.models import Base
  # Import your models

DATABASE_URL ="postgresql://postgres:Mithun21@localhost:5432/photo_library_db"  # Replace with your database URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()