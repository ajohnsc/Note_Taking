from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from pydantic import BaseModel
import time
import os

app = FastAPI()
database_url = os.getenv('DATABASE_URL')
def get_engine():
    while True:
        try:
            engine = create_engine(database_url)
            # Test the connection
            with engine.connect() as connection:
                return engine
        except OperationalError:
            print("Database is not yet available, waiting...")
            time.sleep(5)
engine = get_engine()
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Model
class NoteInDB(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    created_at = Column(DateTime)

# Pydantic Models
class NoteCreate(BaseModel):
    title: str
    body: str

class NoteResponse(NoteCreate):
    id: int

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get('/notes', response_model=list[NoteResponse])
def list_notes():
    db: Session = SessionLocal()
    notes = db.query(NoteInDB).all()
    return [{"id": note.id, "title": note.title, "body": note.body} for note in notes]

@app.post('/notes', response_model=NoteResponse)
def create_note(note: NoteCreate):
    db: Session = SessionLocal()
    new_note = NoteInDB(**note.dict())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return {"id": new_note.id, "title": new_note.title, "body": new_note.body}

@app.get('/notes/{note_id}', response_model=NoteResponse)
def get_note(note_id: int):
    db: Session = SessionLocal()
    note = db.query(NoteInDB).filter(NoteInDB.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"id": note.id, "title": note.title, "body": note.body}

@app.put('/notes/{note_id}', response_model=NoteResponse)
def update_note(note_id: int, note: NoteCreate):
    db: Session = SessionLocal()
    existing_note = db.query(NoteInDB).filter(NoteInDB.id == note_id).first()
    if not existing_note:
        raise HTTPException(status_code=404, detail="Note not found")
    existing_note.title = note.title
    existing_note.body = note.body
    db.commit()
    db.refresh(existing_note)
    return {"id": existing_note.id, "title": existing_note.title, "body": existing_note.body}

@app.delete('/notes/{note_id}')
def delete_note(note_id: int):
    db: Session = SessionLocal()
    existing_note = db.query(NoteInDB).filter(NoteInDB.id == note_id).first()
    if not existing_note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(existing_note)
    db.commit()
    return {"detail": "Note deleted"}
