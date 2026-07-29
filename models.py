from pydantic import BaseModel


class Note(BaseModel):
    title: str
    content: str

class GrammarCheckRequest(BaseModel):
    text: str

class UpdateNoteRequest(BaseModel):
    content: str

class RenameNoteRequest(BaseModel):
    new_name: str