from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Form
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# Get the absolute path to the parent directory of 'lib_backend'
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Now try the import without 'lib_backend.' prefix
from lib_backend.database import get_db
from lib_backend.models import Base
import lib_backend.schemas as schemasc
# ... other imports
from sqlalchemy.orm import Session
from lib_backend.database import get_db
from lib_backend import models, schemas
import os
from datetime import datetime
from sqlalchemy import func

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
async def redirect_to_docs():
    return RedirectResponse("/docs")

@app.post("/api/photos/upload", response_model=schemas.Photo, status_code=201)
async def upload_photo(
    image: UploadFile = File(...),
    description: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    if not image.filename.endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="Invalid file type")

    file_extension = image.filename.split('.')[-1]
    new_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{image.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, new_filename)

    with open(file_path, "wb") as buffer:
        content = await image.read()
        buffer.write(content)

    db_photo = models.Photo(
        filename=new_filename,
        upload_date=datetime.now(),
        description=description,
        tags=tags
    )
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo

@app.get("/api/photos", response_model=List[schemas.Photo])
async def get_photos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    photos = db.query(models.Photo).offset(skip).limit(limit).all()
    return photos

@app.get("/api/photos/{photo_id}", response_model=schemas.Photo)
async def get_photo(photo_id: int, db: Session = Depends(get_db)):
    db_photo = db.query(models.Photo).filter(models.Photo.id == photo_id).first()
    if db_photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    return db_photo

@app.put("/api/photos/{photo_id}", response_model=schemas.Photo)
async def update_photo(photo_id: int, photo: schemas.PhotoBase, db: Session = Depends(get_db)):
    db_photo = db.query(models.Photo).filter(models.Photo.id == photo_id).first()
    if db_photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")

    for key, value in photo.dict(exclude_unset=True).items():
        setattr(db_photo, key, value)
    db.commit()
    db.refresh(db_photo)
    return db_photo

@app.delete("/api/photos/{photo_id}", status_code=204)
async def delete_photo(photo_id: int, db: Session = Depends(get_db)):
    db_photo = db.query(models.Photo).filter(models.Photo.id == photo_id).first()
    if db_photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    db.delete(db_photo)
    db.commit()
    return {"message": f"Photo with id {photo_id} deleted successfully"}

@app.post("/api/directories", response_model=schemas.Directory, status_code=201)
async def create_directory(directory: schemas.DirectoryCreate, db: Session = Depends(get_db)):
    db_directory = models.Directory(name=directory.name)
    db.add(db_directory)
    db.commit()
    db.refresh(db_directory)
    return db_directory

@app.get("/api/directories", response_model=List[schemas.Directory])
async def get_directories(db: Session = Depends(get_db)):
    directories = db.query(models.Directory).all()
    return directories

@app.put("/api/directories/{directory_id}", response_model=schemas.Directory)
async def update_directory(directory_id: int, directory: schemas.DirectoryBase, db: Session = Depends(get_db)):
    db_directory = db.query(models.Directory).filter(models.Directory.id == directory_id).first()
    if db_directory is None:
        raise HTTPException(status_code=404, detail="Directory not found")
    db_directory.name = directory.name
    db.commit()
    db.refresh(db_directory)
    return db_directory

@app.delete("/api/directories/{directory_id}", status_code=204)
async def delete_directory(directory_id: int, db: Session = Depends(get_db)):
    db_directory = db.query(models.Directory).filter(models.Directory.id == directory_id).first()
    if db_directory is None:
        raise HTTPException(status_code=404, detail="Directory not found")
    db.delete(db_directory)
    db.commit()
    return {"message": f"Directory with id {directory_id} deleted successfully"}

@app.get("/api/photos/search")
async def search_photos(query: str, db: Session = Depends(get_db)):
    # Basic search across filename, description, and tags (case-insensitive)
    results = db.query(models.Photo).filter(
        (func.lower(models.Photo.filename).contains(query.lower())) |
        (func.lower(models.Photo.description).contains(query.lower())) |
        (func.lower(models.Photo.tags).contains(query.lower()))
    ).all()
    return results

@app.get("/uploads/{filename}")
async def get_image(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)