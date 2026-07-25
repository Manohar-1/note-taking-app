from fastapi import FastAPI, File, UploadFile

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


