from fastapi import FastAPI, HTTPException, Path, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List

from .models import Note, NoteCreate, NoteUpdate
from .repository import note_repository

openapi_tags = [
    {"name": "Notes", "description": "Operations to create, read, update, and delete notes."},
    {"name": "Health", "description": "Service health check endpoint."}
]

app = FastAPI(
    title="Notes Backend API",
    description="API for managing notes via CRUD operations.",
    version="1.0.0",
    openapi_tags=openapi_tags
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# PUBLIC_INTERFACE
@app.get("/", tags=["Health"], summary="Health Check", response_description="Health status")
def health_check():
    """
    Endpoint to check the health of the service.

    Returns:
        JSON message indicating health status.
    """
    return {"message": "Healthy"}


# PUBLIC_INTERFACE
@app.post(
    "/notes/",
    response_model=Note,
    status_code=status.HTTP_201_CREATED,
    summary="Create a note",
    description="Create a new note with title and content.",
    tags=["Notes"],
)
def create_note(note: NoteCreate):
    """
    Create a new note.

    Args:
        note (NoteCreate): The note to create.

    Returns:
        Note: The created note.
    """
    new_note = note_repository.create_note(note)
    return new_note


# PUBLIC_INTERFACE
@app.get(
    "/notes/",
    response_model=List[Note],
    summary="List all notes",
    description="Get a list of all stored notes.",
    tags=["Notes"],
)
def list_notes():
    """
    Retrieve a list of all notes.

    Returns:
        List[Note]: All notes.
    """
    return note_repository.list_notes()


# PUBLIC_INTERFACE
@app.get(
    "/notes/{note_id}",
    response_model=Note,
    responses={
        404: {
            "description": "Note not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Note not found"}
                }
            }
        }
    },
    summary="Get a note by ID",
    description="Retrieve a note by its unique ID.",
    tags=["Notes"],
)
def get_note(
    note_id: str = Path(..., description="The unique identifier of the note")
):
    """
    Fetch a specific note by ID.

    Args:
        note_id (str): Unique ID of the note.

    Raises:
        HTTPException: If note not found.

    Returns:
        Note: The requested note.
    """
    note = note_repository.get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


# PUBLIC_INTERFACE
@app.put(
    "/notes/{note_id}",
    response_model=Note,
    responses={
        404: {
            "description": "Note not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Note not found"}
                }
            }
        }
    },
    summary="Update a note",
    description="Update an existing note's title or content.",
    tags=["Notes"],
)
def update_note(
    note_id: str = Path(..., description="The unique identifier of the note"),
    note_update: NoteUpdate = ...,
):
    """
    Update a note.

    Args:
        note_id (str): The ID of the note to update.
        note_update (NoteUpdate): The updated note fields.

    Raises:
        HTTPException: If note not found.

    Returns:
        Note: The updated note.
    """
    note = note_repository.update_note(note_id, note_update)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


# PUBLIC_INTERFACE
@app.delete(
    "/notes/{note_id}",
    response_class=JSONResponse,
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Note deleted successfully"},
        404: {
            "description": "Note not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Note not found"}
                }
            }
        }
    },
    summary="Delete a note",
    description="Delete a note by its unique ID.",
    tags=["Notes"],
)
def delete_note(
    note_id: str = Path(..., description="The unique identifier of the note")
):
    """
    Delete a note by ID.

    Args:
        note_id (str): The ID of the note to delete.

    Raises:
        HTTPException: If note not found.

    Returns:
        Empty response (204) if deleted successfully.
    """
    deleted = note_repository.delete_note(note_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found")
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
