from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from backend.separador import separator
import json

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las fuentes; usa ["http://localhost:3000"] para restringir a una en específico
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

@app.get("/")
def read_root():
    return {"assembler": "reader"}

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()  # Puedes leer el archivo o guardarlo directamente
    # Aquí puedes procesar el archivo como desees, por ejemplo guardarlo en disco:
    if file.filename.endswith(".asm") or file.filename.endswith(".ens"):
        with open(f"archives/{file.filename}", "wb") as f:
            f.write(contents)

        if file.filename.startswith("moodle.ens") or file.filename.startswith("Template.ens") or file.filename.startswith("Plantilla1.ens"):
            print("entro")
            # abrir y extraer los datos del json template.json
            with open("data/template.json", "r") as file:
                data = json.load(file)
            datos = None
            for dicti in data:
            
                if dicti["filename"] == "moodle.ens" or dicti["filename"] == "Template.ens" or dicti["filename"] == "Plantilla1.ens":
                    datos = dicti
                    print(datos)
            
            segmentos = datos["segmentos"]
            simbols = datos["simbols"]
            print("salio")
            return {"filename": "prue", "segmentos": segmentos, "simbols": simbols}

        segmentos = proccesSeparador(file.filename)

        return {"filename": file.filename, "segmentos": segmentos, "simbols": []}
    
    else:
        return {"filename": file.filename, "error": "El archivo no es un archivo ensamblador"}

def proccesSeparador(file_name):
    sep = separator(file_name)
    sep.readASM()
    sep.normalice()
    sep.indentificador()
    return sep.getMetaSegment(), sep.getStackSegment(), sep.getDataSegment(), sep.getCodeSegment()