from fastapi import FastAPI, File, UploadFile
from backend.separador import separator

app = FastAPI()

@app.get("/")
def read_root():
    return {"assembler": "reader"}

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()  # Puedes leer el archivo o guardarlo directamente
    # Aquí puedes procesar el archivo como desees, por ejemplo guardarlo en disco:
    if file.filename.endswith(".asm"):
        with open(f"archives/{file.filename}", "wb") as f:
            f.write(contents)

        segmentos = proccesSeparador(file.filename)

        return {"filename": file.filename, "segmentos": segmentos}
    
    else:
        return {"filename": file.filename, "error": "El archivo no es un archivo .asm"}

def proccesSeparador(file_name):
    sep = separator(file_name)
    sep.readASM()
    sep.normalice()
    sep.indentificador()
    return sep.getMetaSegment(), sep.getStackSegment(), sep.getDataSegment(), sep.getCodeSegment()