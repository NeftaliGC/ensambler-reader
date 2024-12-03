import re
import json
from pathlib import Path

class ErrorLin():
    def __init__(self):
        self.lines = None
        self.segment = None
        self.error = "Correcto"
        self.errorType = ""
        self.segments = None
        self.readInstructions()
        self.declared_variables = set()  # Almacenará las variables ya declaradas

    def setError(self, error, errorType):
        self.error = error
        self.errorType = errorType

    def setLines(self, lines):
        self.lines = lines
    
    def setSegment(self, segment):
        self.segment = segment
    
    def setSegments(self, segments):
        self.segments = segments

    def getError(self):
        return f"{self.errorType}: {self.error}"

    def readInstructions(self):
        dataPath = Path(__file__).parent / "data/errors.json"
        with dataPath.open("r") as file:
            self.instructions = json.load(file)

    def identidyError(self):
        if self.segment == "stack":
            self.reviewStack()
            return self.lines
        elif self.segment == "data":
            self.reviewData()
            return self.lines
        elif self.segment == "code":
            self.reviewCode()
            return self.lines
        else:
            return "no se ha identificado el segmento"

#------------------- Revisión de segmento de pila -------------------
    def reviewStack(self):
        pila_encontrada = False
        segment_stack = False
        i = 0
        for line in self.lines:
            if re.match(r"\.stack\s*segment", line["complete"]):
                segment_stack = True  # Inicio de segmento de pila
            elif line["complete"].startswith("ends"):
                segment_stack = False  # Fin de segmento de pila

            if segment_stack:
                if re.match(r"\.stack", line["complete"]) and not re.match(r"\.stack\s*segment", line["complete"]):
                    self.setError("Instrucción de inicio del segmento de pila incorrecta", "Error")
                
                elif re.search(r"dw", line["complete"]) and not self.isValidDw(line["complete"]):
                    self.setError("Instrucción 'dw' no válida", "Error")
                
                elif re.search(r"dup", line["complete"]) and not self.isValidDup(line["complete"]):
                    self.setError("Instrucción 'dup' no válida", "Error")
                
                elif re.search(r"db", line["complete"]) and not self.isValidDb(line["complete"]):
                    self.setError("Instrucción 'db' no válida", "Error")
            
            if not segment_stack and not re.match(r"ends", line["complete"]):
                self.setError("Instrucción no reconocida", "Error")

            line["errores"] = self.getError()
            self.lines[i] = line
            i += 1
            self.setError("Correcto", "")


#------------------- Revisión de segmento de datos -------------------
    def reviewData(self):
        segment_data = False
        i = 0
        for line in self.lines:
            if re.match(r"\.data\s*segment", line["complete"]):
                segment_data = True  # Inicio del segmento de datos
            elif line["complete"].startswith("ends"):
                segment_data = False  # Fin del segmento de datos

            if segment_data:
                # Verifica si ya está declarada la variable
                if re.search(r"\b\w+\b", line["complete"]):  # Detecta posibles variables
                    var_name = re.findall(r"\b\w+\b", line["complete"])[0]  # Extrae el nombre de la variable
                    if var_name in self.declared_variables:
                        self.setError(f"La variable '{var_name}' ya ha sido declarada", "Error")
                    else:
                        self.declared_variables.add(var_name)  # Marca la variable como declarada

            # Asignar el error (si lo hay) a la línea
            line["errores"] = self.getError()
            self.lines[i] = line
            i += 1
            self.setError("Correcto", "")

#------------------- Revisión de segmento de código -------------------
    def reviewCode(self):
        segment_code = False
        i = 0
        for line in self.lines:
            if re.match(r"\.code\s*segment", line["complete"]):
                segment_code = True
            elif line["complete"].startswith("ends"):
                segment_code = False

            if segment_code:
                # Verifica si ya está declarada la variable o instrucción
                if re.search(r"\b\w+\b", line["complete"]):  # Detecta posibles etiquetas/variables
                    var_name = re.findall(r"\b\w+\b", line["complete"])[0]

                    # Comprobamos si el nombre es una instrucción válida
                    instruction = next((instr for instr in self.instructions if instr["name"] == var_name), None)
                    
                    if instruction:
                        # Si encontramos la instrucción, validamos su sintaxis
                        if not self.validateSyntax(line["complete"], instruction):
                            self.setError(f"Sintaxis incorrecta para la instrucción '{var_name}'", "Error")
                    elif var_name not in self.declared_variables:
                        self.declared_variables.add(var_name)  # Marca la etiqueta como declarada
                    else:
                        self.setError(f"La etiqueta '{var_name}' ya ha sido declarada", "Error")

            # Asignar el error (si lo hay) a la línea
            line["errores"] = self.getError()
            self.lines[i] = line
            i += 1
            self.setError("Correcto", "")





    # Función de validación de 'dup'
    def isValidDup(self, line):
        # Aceptar duplicados válidos como 'dup(0)', 'dup(10)'
        return bool(re.search(r"dup\(\d+\)", line))

    # Función de validación de 'db'
    def isValidDb(self, line):
        # Permitir cadenas de caracteres con 'db', como 'db "hola"'
        if re.search(r'"[^"]*"', line) or re.search(r"'[^']*'", line):
            return True
        # Permitir definiciones de valores hexadecimales o binarios
        elif re.search(r"db\s*([0-9A-Fa-f]+H|[01]+b)", line):
            return True
        # Permitir duplicados dentro de 'db'
        elif re.search(r"db\s*\d+\s*dup\(\d+\)", line):
            return True
        return False

    # Función de validación de 'dw'
    def isValidDw(self, line):
        # Permitir duplicados en 'dw'
        if re.search(r"dw\s*\d+\s*dup\(\d+\)", line):
            return True
        # Validar valores de 'dw' como números decimales o hexadecimales
        elif re.search(r"dw\s*([0-9A-Fa-f]+H|\d+)", line):
            return True
        return False

    # Función de validación de 'equ'
    def isValidEqu(self, line):
        parts = line.split()
        if len(parts) == 3 and parts[1].lower() == 'equ':
            # Verifica que el valor después de 'equ' sea un número
            try:
                int(parts[2], 0)  # Verifica que sea un número en cualquier base
                return True
            except ValueError:
                return False
        return False

    def validateSyntax(self, line, instruction):
        """
        Valida la sintaxis de la línea de acuerdo con la instrucción proporcionada.
        Esto es muy simplificado y puedes ampliarlo dependiendo de las reglas de sintaxis.
        """
        # Verifica que el operando en la línea coincida con los operandos de la instrucción
        operands = re.findall(r"<([A-Za-z0-9, ]+)>", instruction["syntax"])
        if operands:
            operands = operands[0].split(", ")
            # Asumiendo que la sintaxis será algo como "INSTRUCCION <operand>"
            operands_found = re.findall(r"\b([A-Za-z0-9]+)\b", line)
            if operands_found:
                operands_found = operands_found[1:]  # Descartar la instrucción
                for operand in operands_found:
                    if operand not in operands:
                        return False  # Si el operando no es válido, la sintaxis es incorrecta
        return True