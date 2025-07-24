from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

# PUBLIC_INTERFACE
class NoteBase(BaseModel):
    """Base model for creating and updating notes."""
    title: str = Field(..., description="The title of the note", min_length=1)
    content: str = Field(..., description="The content of the note")

# PUBLIC_INTERFACE
class NoteCreate(NoteBase):
    """Model for creating a new note."""
    pass

# PUBLIC_INTERFACE
class NoteUpdate(BaseModel):
    """Model for updating an existing note."""
    title: Optional[str] = Field(None, description="The updated title of the note", min_length=1)
    content: Optional[str] = Field(None, description="The updated content of the note")

# PUBLIC_INTERFACE
class Note(NoteBase):
    """Response model representing a note."""
    id: str = Field(..., description="Unique identifier for the note")
    created_at: datetime = Field(..., description="Time the note was created")
    updated_at: datetime = Field(..., description="Time the note was last updated")

    class Config:
        orm_mode = True

# Utility function to generate unique IDs
def generate_note_id() -> str:
    return str(uuid.uuid4())
