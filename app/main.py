from fastapi import FastAPI

from app.utils import check_grammar
from app.services import create_note_service,upload_note_service,list_note_service,get_note_service,render_note_service,delete_note_service,search_note_service,update_note_service,rename_note_service
from app.models import Note, GrammarCheckRequest, UpdateNoteRequest, RenameNoteRequest
from app.routers.notes import router
import os 
import markdown 


app = FastAPI()

app.include_router(router)


