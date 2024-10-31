from pathlib import Path
import re

class separator:
    def __init__(self, name):
        self.name = name
        self.metaSegment = []
        self.stakSegment = []
        self.dataSegment = []
        self.codeSegment = []

    def readASM(self):
        # Construir la ruta relativa al archivo desde el script actual
        ruta = Path(__file__).parent / "archives" / self.name

        # Abre el archivo usando la ruta construida
        with ruta.open("r", encoding="utf-8") as file:
            lines = file.readlines()  # Llamada correcta a `readlines()`
            
            # Diccionario para mapear segmentos
            segment_map = {
                "meta": self.metaSegment,
                "stack": self.stakSegment,
                "data": self.dataSegment,
                "code": self.codeSegment,
            }
            
            # Variable para mantener el segmento actual
            current_segment = "meta"

            for line in lines:
                # Verifica si la línea indica un nuevo segmento
                for segment in segment_map.keys():
                    if f".{segment} segment" in line or f".{segment}" in line:
                        if "ends" not in line:
                            current_segment = segment
                        break  # Salir del bucle al encontrar un segmento

                
                # Agregar la línea al segmento correspondiente
                if current_segment:
                    segment_map[current_segment].append(line)
    
    def normalice(self):
        # Diccionario para mapear segmentos
        segment_map = {
            "meta": self.metaSegment,
            "stack": self.stakSegment,
            "data": self.dataSegment,
            "code": self.codeSegment,
        }

        for segment_name, segment_lines in segment_map.items():
            normalized_lines = []  # Lista para almacenar líneas normalizadas
            for line in segment_lines:
                # Elimina comentarios de una línea
                line = re.sub(r";.*", "", line)
                # Elimina tabuladores y espacios en blanco
                line = re.sub(r"\s+", " ", line)
                # Elimina saltos de línea
                line = line.strip()  # Quita espacios al inicio y al final
                # Si la línea no está vacía, la añadimos a la lista de líneas normalizadas
                if line:
                    normalized_lines.append(line)
            
            # Actualiza el segmento con las líneas normalizadas
            segment_map[segment_name] = normalized_lines

        # Actualiza los segmentos con las líneas normalizadas
        self.metaSegment = segment_map["meta"]
        self.stakSegment = segment_map["stack"]
        self.dataSegment = segment_map["data"]
        self.codeSegment = segment_map["code"]

    def getStackSegment(self):
        return self.stakSegment

    def getDataSegment(self):
        return self.dataSegment

    def getCodeSegment(self):
        return self.codeSegment

    def getMetaSegment(self):
        return self.metaSegment