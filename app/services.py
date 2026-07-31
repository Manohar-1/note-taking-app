from app.models import Note
from app.models import UpdateNoteRequest, RenameNoteRequest
from fastapi import HTTPException

import os
import markdown

def create_note_service(note: Note):
    filename = f"{note.title.strip()}.md"

    if(note.title.strip()==""):
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    if(os.path.exists(f"uploads/{filename}")==True):
        raise HTTPException(status_code=400, detail="Note with this name already exists")


    with open(f"uploads/{filename}", "w", encoding="utf-8-sig") as f:
        f.write(note.content)

    return {"message": f"{filename} created successfully!"}

def upload_note_service(filename:str, contents:bytes):
    with open(f"uploads/{filename}","wb") as f:
        f.write(contents)
    
    return {"message": f"{filename} uploaded successfully!"}


def list_note_service():
    notes = []
    count=0
    for filename in os.listdir("uploads"):
            notes.append(filename)
            count+=1
    return {"notes": notes,"count":count}


def get_note_service(note_name:str):
    try:
        with open(f"uploads/{note_name}", "r",encoding="utf-8-sig") as f:
            text = f.read()
        return {"content":text}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Note not found")

def render_note_service(note_name:str):
    try:
        with open(f"uploads/{note_name}", "r",encoding="utf-8-sig") as f:
            text = f.read()
        html = markdown.markdown(text)
        return html
    except FileNotFoundError:
        raise HTTPException(status_code=404,detail="Note not found")


def delete_note_service(note_name:str):
    try:
        os.remove(f"uploads/{note_name}")
        return {"message": f"{note_name} deleted successfully!"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Note not found")

def search_note_service(query:str):
    results = []
    for filename in os.listdir("uploads"):
            with open(f"uploads/{filename}", "r",encoding="utf-8-sig") as f:
                text = f.read()
            print(text)
            if query.lower() in text.lower():
                results.append(filename)
    return {"query": query, "results": results}

def update_note_service(request:UpdateNoteRequest,note_name:str):
    if(os.path.exists(f"uploads/{note_name}")==False):
        raise HTTPException(status_code=404, detail="Note not found")
    if(request.content.strip()==""):
        raise HTTPException(status_code=400, detail="Note content cannot be empty")
    with open(f"uploads/{note_name}","w",encoding="utf-8-sig") as f:
        f.write(request.content)
    return {"message": f"{note_name} updated successfully!"}


def rename_note_service(new_name:str,note_name:str):
    print(new_name)
    print(note_name)

    if(os.path.isfile(f"uploads/{note_name}")==False):
        raise HTTPException(status_code=404,detail="Note not found")
    
    if(new_name==""):
        raise HTTPException(status_code=400,detail="New name cannot be empty")

    

    if(new_name.endswith(".md")==False):
        new_name=new_name+".md"
    
    if(new_name.lower()!=note_name.lower() and os.path.exists(f"uploads/{new_name}")==True):
        raise HTTPException(status_code=400,detail="new name already exists")

    

    os.rename(f"uploads/{note_name}",f"uploads/{new_name}")
    return {"message": f"{note_name} renamed to {new_name} successfully!"}