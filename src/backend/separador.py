from pathlib import Path

class separator:
    def __init__(self, name):
        self.name = name
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
                "stack": self.stakSegment,
                "data": self.dataSegment,
                "code": self.codeSegment,
            }
            
            # Variable para mantener el segmento actual
            current_segment = None

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

        
        print(self.stakSegment)
        print(self.dataSegment)
        print(self.codeSegment)
