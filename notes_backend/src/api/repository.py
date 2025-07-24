from typing import Dict, List, Optional
from .models import Note, NoteCreate, NoteUpdate, generate_note_id
from datetime import datetime

# Singleton in-memory note store
class NoteRepository:
    """Repository class for managing notes in-memory."""

    def __init__(self):
        self.notes: Dict[str, Note] = {}

    # PUBLIC_INTERFACE
    def create_note(self, note_create: NoteCreate) -> Note:
        """Create a new note and add it to the repository."""
        now = datetime.utcnow()
        note_id = generate_note_id()
        note = Note(
            id=note_id,
            title=note_create.title,
            content=note_create.content,
            created_at=now,
            updated_at=now,
        )
        self.notes[note_id] = note
        return note

    # PUBLIC_INTERFACE
    def get_note(self, note_id: str) -> Optional[Note]:
        """Retrieve a note by its unique ID."""
        return self.notes.get(note_id)

    # PUBLIC_INTERFACE
    def update_note(self, note_id: str, note_update: NoteUpdate) -> Optional[Note]:
        """Update an existing note."""
        note = self.notes.get(note_id)
        if note is None:
            return None
        updated = note.copy(update={
            "title": note_update.title if note_update.title is not None else note.title,
            "content": note_update.content if note_update.content is not None else note.content,
            "updated_at": datetime.utcnow(),
        })
        self.notes[note_id] = updated
        return updated

    # PUBLIC_INTERFACE
    def delete_note(self, note_id: str) -> bool:
        """Delete a note by its ID. Returns True if deleted, False if not found."""
        return self.notes.pop(note_id, None) is not None

    # PUBLIC_INTERFACE
    def list_notes(self) -> List[Note]:
        """Return a list of all notes."""
        return list(self.notes.values())


# Singleton repository instance
note_repository = NoteRepository()
