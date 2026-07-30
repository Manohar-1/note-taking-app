from models import Note

def create_note_service(note: Note):
    filename = f"{note.title.strip()}.md"

    if(note.title.strip()==""):
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    if(os.path.exists(f"uploads/{filename}")==True):
        raise HTTPException(status_code=400, detail="Note with this name already exists")


    with open(f"uploads/{filename}", "w", encoding="utf-8-sig") as f:
        f.write(note.content)

    return {"message": f"{filename} created successfully!"}
