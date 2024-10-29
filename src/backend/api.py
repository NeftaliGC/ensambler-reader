from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.get("/")
def read_root():
    return {"assembler": "reader"}

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()  # Puedes leer el archivo o guardarlo directamente
    # Aquí puedes procesar el archivo como desees, por ejemplo guardarlo en disco:
    with open(f"archives/{file.filename}", "wb") as f:
        f.write(contents)
    return {"filename": file.filename}