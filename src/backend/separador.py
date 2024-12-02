from pathlib import Path
import re
import json

class separator:
    def __init__(self, name):
        self.name = name
        self.dataPath = Path(__file__).parent / "data/description.json"
        self.metaSegment = []
        self.stakSegment = []
        self.dataSegment = []
        self.codeSegment = []
        self.completeSegments = []
        self.segment_map = {
            "meta": self.metaSegment,
            "stack": self.stakSegment,
            "data": self.dataSegment,
            "code": self.codeSegment,
        }

    def readASM(self):
        # Construir la ruta relativa al archivo desde el script actual
        ruta = Path(__file__).parent / "archives" / self.name

        # Abre el archivo usando la ruta construida
        with ruta.open("r", encoding='latin-1') as file:
            lines = file.readlines()  # Llamada correcta a `readlines()`
            
            # Variable para mantener el segmento actual
            current_segment = "meta"

            for line in lines:
                # Verifica si la línea indica un nuevo segmento
                for segment in self.segment_map.keys():
                    if f".{segment} segment" in line or f".{segment}" in line:
                        if "ends" not in line:
                            current_segment = segment
                        break  # Salir del bucle al encontrar un segmento

                
                # Agregar la línea al segmento correspondiente
                if current_segment:
                    self.segment_map[current_segment].append(line)
    
    def normalice(self):

        for segment_name, segment_lines in self.segment_map.items():
            normalized_lines = []  # Lista para almacenar líneas normalizadas
            for line in segment_lines:
                # Elimina comentarios de una línea
                line = re.sub(r";.*", "", line)
                # Elimina tabuladores y espacios en blanco
                line = re.sub(r"\s+", " ", line)
                # Elimina saltos de línea
                line = line.strip()  # Quita espacios al inicio y al final
                # elimina las comas
                line = line.replace(",", "")
                # Si la línea no está vacía, la añadimos a la lista de líneas normalizadas
                if line:
                    normalized_lines.append(line)
            
            # Actualiza el segmento con las líneas normalizadas
            self.segment_map[segment_name] = normalized_lines

        # Actualiza los segmentos con las líneas normalizadas
        self.metaSegment = self.segment_map["meta"]
        self.stakSegment = self.segment_map["stack"]
        self.dataSegment = self.segment_map["data"]
        self.codeSegment = self.segment_map["code"]
        self.completeSegments = [self.metaSegment.copy(), self.stakSegment.copy(), self.dataSegment.copy(), self.codeSegment.copy()]

    def indentificador(self):
        for segment in self.segment_map:
            i = 0  # Explicit index counter, as we'll be modifying the list in-place
            while i < len(self.segment_map[segment]):
                line = self.segment_map[segment][i]
                
                # Check if the whole line is a pseudo instruction
                if self.isPsuedoInstruction(line):
                    classification = "Pseudo Instrucción"
                    self.segment_map[segment][i] = {"cp": "","complete": line, "line": line, "classification": classification, "codificacion": "", "errores": ""}
                    i += 1  # Move to the next line
                else:
                    # Remove the original line at index i
                    del self.segment_map[segment][i]
                    
                    j = 0  # Index counter for words in the line
                    # Process each word individually and insert it at position i
                    
                    for word in line.split():
                        # Inicializamos el diccionario afuera del bucle
                        if j == 0:  # Solo inicializamos el diccionario una vez por línea
                            segment_data = {
                                "cp": "",          # Contador de programa
                                "complete": line,  # La línea completa
                                "line": [],        # Una lista para almacenar las palabras (words)
                                "classification": [],  # Lista de clasificaciones
                                "codificacion": "",  # Código de máquina
                                "errores": "",      # Errores
                            }

                        # Clasificamos la palabra
                        if self.isPsuedoInstruction(word):
                            classification = "Pseudo Instrucción"
                        elif self.isInstruction(word):
                            classification = "Instrucción"
                        elif self.isSimbol(word):
                            classification = "Simbolo"
                        else:
                            classification = "No se reconoce"

                        # Agregamos la palabra a la lista 'line' y la clasificación a 'classification'
                        segment_data["line"].append(word)
                        segment_data["classification"].append(classification)

                        j += 1
                    # Una vez procesada la línea, insertamos el diccionario completo
                    self.segment_map[segment].insert(i, segment_data)
                    i += 1  # Move to the next position for the next word


    def isPsuedoInstruction(self, instruction):
        isPsuedoInstructions = self.readDescription("pseudoinstrucciones")
        return instruction in isPsuedoInstructions

    def isInstruction(self, instruction):
        # Obtiene la lista de instrucciones del JSON
        instructions_list = self.readDescription("Instrucciones")
        
        # Convierte la lista de objetos JSON a un diccionario con claves en minúsculas
        normalized_instructions = {list(item.keys())[0].lower(): list(item.values())[0] for item in instructions_list}
        
        # Normaliza la instrucción ingresada a minúsculas
        instruction_lower = instruction.lower()
        
        # Verifica si la instrucción en minúsculas está en el diccionario normalizado
        return instruction_lower in normalized_instructions

    def isSimbol(self, component):
        isDirectives = self.readDescription("regexSimbol")
        for directive in isDirectives:
            if re.match(directive, component):
                return True

    def readDescription(self, indentificador):
        with open(self.dataPath, "r") as file:
            data = json.load(file)
            return data[indentificador]

    def getStackSegment(self):
        return self.stakSegment

    def getDataSegment(self):
        return self.dataSegment

    def getCodeSegment(self):
        return self.codeSegment

    def getMetaSegment(self):
        return self.metaSegment

    def getCompleteSegments(self):
        return self.completeSegments