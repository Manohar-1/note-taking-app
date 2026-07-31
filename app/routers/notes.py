from fastapi import APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/")
def home():
    return {"message": "Welcome to the FastAPI Note Taking Application!"}


@router.post("/notes")
def create_note(note: Note):
    return create_note_service(note)

@router.post("/upload")
async def upload_note(file:UploadFile = File(...)): 
    if not file.filename.endswith(".md"):
        raise HTTPException(status_code=400,detail="Only .md Markdown files are allowed")

    if os.path.exists(f"uploads/{file.filename}"):
        raise HTTPException(status_code=400,detail="Uploaded File Already Exists")

    if(file.filename.strip()==""):
        raise HTTPException(status_code=400,detail="Filename cannot be empty")
    contents = await file.read()

    return upload_note_service(file.filename,contents)
    
    


@router.get("/notes")
def list_notes():
    return list_note_service()
    

@router.get("/notes/{note_name}")
def get_note(note_name:str):
    return get_note_service(note_name)


@router.get("/notes/{note_name}/render",response_class=HTMLResponse)
def render_note(note_name:str):
    return render_note_service(note_name)

@router.delete("/notes/{note_name}")
def delete_note(note_name:str):
    return delete_note_service(note_name)


@router.post("/grammar-check")
def grammar_check(request: GrammarCheckRequest):
    errors = check_grammar(request.text)
    return {"original_text": request.text, "error_count": len(errors), "errors": errors}


@router.get("/search")
def search_notes(query: str):
    return search_note_service(query)
    

@router.put("/notes/{note_name}")
def update_note(request: UpdateNoteRequest, note_name: str):
    return update_note_service(request,note_name)

@router.patch("/note/{note_name}/rename")
def rename_note(request:RenameNoteRequest,note_name:str):
    return rename_note_service(request.new_name.strip(),note_name)






