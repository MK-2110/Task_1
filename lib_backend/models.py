from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Directory(Base):
    __tablename__ = "directories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    photos = relationship("Photo", back_populates="directory")

class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    upload_date = Column(DateTime, default=datetime.utcnow)
    description = Column(String, nullable=True)
    directory_id = Column(Integer, ForeignKey("directories.id"), nullable=True)
    tags = Column(String, nullable=True) # Example: Store tags as comma-separated string

    directory = relationship("Directory", back_populates="photos")

# If using a separate tags table:
# photo_tags = Table('photo_tags', Base.metadata,
#     Column('photo_id', ForeignKey('photos.id'), primary_key=True),
#     Column('tag_id', ForeignKey('tags.id'), primary_key=True)
# )
#
# class Tag(Base):
#     __tablename__ = "tags"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True, index=True)
#
#     photos = relationship("Photo", secondary=photo_tags, back_populates="tags")
#     tags = relationship("Tag", secondary=photo_tags, back_populates="photos")