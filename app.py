from fastapi import FastAPI, File, UploadFile, HTTPException
import os 
import markdown 

from fastapi.responses import HTMLResponse

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
    





