from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse

from pydantic import BaseModel

import os 
import markdown 
import language_tool_python


class GrammarRequest(BaseModel):
    text: str

class UpdateNoteRequest(BaseModel):
    content: str

class RenameNoteRequest(BaseModel):
    new_name: str

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI Note Taking Application!"}


@app.post("/upload")
async def upload_note(file:UploadFile = File(...)):
    contents = await file.read()
    
    with open(f"uploads/{file.filename}","wb") as f:
        f.write(contents)
    
    return {"message": f"{file.filename} uploaded successfully!"}


@app.get("/notes")
def list_notes():
    notes = []
    count=0
    for filename in os.listdir("uploads"):
        if filename.endswith(".md"):
            notes.append(filename)
            count+=1
    return {"notes": notes,"count":count}

@app.get("/notes/{note_name}")
def get_note(note_name:str):
    try:
        with open(f"uploads/{note_name}", "r",encoding="utf-8-sig") as f:
            text = f.read()
        return text
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Note not found")


@app.get("/notes/{note_name}/render",response_class=HTMLResponse)
def render_note(note_name:str):


    try:
        with open(f"uploads/{note_name}", "r",encoding="utf-8-sig") as f:
            text = f.read()
        html = markdown.markdown(text)
        return html 
    except FileNotFoundError:
        raise HTTPException(status_code=404,detail="Note not found")

@app.delete("/notes/{note_name}")
def delete_note(note_name:str):
    try:
        os.remove(f"uploads/{note_name}")
        return {"message": f"{note_name} deleted successfully!"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Note not found")


@app.post("/grammar-check")
def grammar_check(request: GrammarRequest):
    errors = check_grammar(request.text)
    return {"original_text": request.text, "error_count": len(errors), "errors": errors}

def check_grammar(text: str):
    errors = []
    tool = language_tool_python.LanguageTool('en-US')
    
    matches = tool.check(text)
    for match in matches:

        errors.append({
            "message": match.message,
            "replacements": match.replacements,
            "rule_id": match.rule_id,
            "matched_text": match.matched_text
        })
    return errors

@app.get("/search")
def search_notes(query: str):
    results = []
    for filename in os.listdir("uploads"):
        if filename.endswith(".md"):
            with open(f"uploads/{filename}", "r",encoding="utf-8-sig") as f:
                text = f.read()
                print(text)
                if query.lower() in text.lower():
                    results.append(filename)
    return {"query": query, "results": results}
    

@app.put("/notes/{note_name}")
def update_note(request: UpdateNoteRequest, note_name: str):
    if(os.path.exists(f"uploads/{note_name}")==False):
        raise HTTPException(status_code=404, detail="Note not found")
    if(request.content.strip()==""):
        raise HTTPException(status_code=400, detail="Note content cannot be empty")
    with open(f"uploads/{note_name}","w",encoding="utf-8-sig") as f:
        f.write(request.content)
    return {"message": f"{note_name} updated successfully!"}

@app.patch("/note/{note_name}/rename")
def rename_note(request:RenameNoteRequest,note_name:str):
    if(os.path.isfile(f"uploads/{note_name}")==False):
        raise HTTPException(status_code=404,detail="Note not found")
    
    if(request.new_name.strip()==""):
        raise HTTPException(status_code=400,detail="New name cannot be empty")

    new_name=request.new_name.strip()
    if(os.path.isfile(f"uploads/{new_name}")==True):
        raise HTTPException(status_code=400,detail="A note with the new name already exists")

    os.rename(f"uploads/{note_name}",f"uploads/{new_name}")
    return {"message": f"{note_name} renamed to {new_name} successfully!"}



