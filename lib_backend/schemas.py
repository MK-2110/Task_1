from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class DirectoryBase(BaseModel):
    name: str

class DirectoryCreate(DirectoryBase):
    pass

class Directory(DirectoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PhotoBase(BaseModel):
    description: Optional[str] = None
    tags: Optional[str] = None
    directory_id: Optional[int] = None

class PhotoCreate(PhotoBase):
    filename: str
    upload_date: datetime

class Photo(PhotoBase):
    id: int
    filename: str
    upload_date: datetime
    directory: Optional[Directory] = None

    class Config:
        from_attributes = True