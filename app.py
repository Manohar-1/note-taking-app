from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse

from pydantic import BaseModel

import os 
import markdown 
import language_tool_python


class GrammarRequest(BaseModel):
    text: str



app = FastAPI()


@app.get("/")
def home():

    
    # matches = tool.check(text)
    # match = matches[0]

    # print(match.message)
    # print(match.replacements)
    # print(match.rule_id)
    # print(match.matched_text)

    

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



