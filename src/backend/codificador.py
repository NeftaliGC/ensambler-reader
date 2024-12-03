import json
import os

# Función para cargar el diccionario de opcodes desde un archivo JSON
def cargar_opcodes():
    current_directory = os.path.dirname(__file__) 
    data = os.path.join(current_directory, "data")
    archivo_json = os.path.join(data, "instrucciones.json")
    # Leer el archivo JSON
    with open(archivo_json, "r") as archivo:
        opcodes = json.load(archivo)
    
    return opcodes

# Función para procesar la línea de entrada y extraer la instrucción y operandos
def procesar_linea(linea):
    # Quitar espacios adicionales y separar la instrucción de los operandos
    partes = linea.strip().split(" ", 1)
    
    if len(partes) != 2:
        return partes[0], ""  # Si no hay operandos, devolvemos una cadena vacía
    
    instruccion = partes[0]
    operando = partes[1]
    
    return instruccion, operando

# Función para codificar la instrucción
def codificar_instruccion(instruccion, operando, opcodes):
    if instruccion in opcodes:
        if operando == "" and instruccion in ["JNS", "JG", "JMP", "JNBE"]:
            # Instrucciones como JMP, JNS, JG y JNBE no requieren operandos explícitos
            return opcodes[instruccion][""]  # En el JSON, estos opcodes tienen la clave vacía
        elif operando in opcodes[instruccion]:
            return opcodes[instruccion][operando]
        else:
            return f"Error: Operando '{operando}' no soportado para la instrucción '{instruccion}'."
    else:
        return f"Error: Instrucción '{instruccion}' no soportada."

# Función principal para procesar la línea y generar el código de máquina
def procesar_instruccion(linea, opcodes):
    instruccion, operando = procesar_linea(linea)
    if "Error" in instruccion:
        return instruccion  # Si hubo un error al procesar la línea
    
    codigo_maquina = codificar_instruccion(instruccion, operando, opcodes)
    return codigo_maquina
import json
import os

class InstructionEncoder:
    def __init__(self, instruction_data):
        self.mapper = OpcodeMapper(instruction_data)

    def encode_instruction(self, instruction_line):
        """
        Codifica la instrucción recibida en el formato requerido, en hexadecimal.
        """
        # Parseamos la instrucción y operandos
        instruction, operands = self.parse_instruction(instruction_line)
        
        # Obtenemos el código binario
        bin_opcode = self.mapper.get_opcode(instruction, operands)
        
        # Convertimos el código binario a hexadecimal (Little Endian)
        hex_opcode = self.bin_to_hex(bin_opcode)
        
        return hex_opcode
    class InstructionParser:
        def __init__(self):
            # Ruta fija al archivo JSON con las instrucciones
            self.json_file_path = '/backend/data/instrucciones.json'  # Asegúrate de que esta ruta sea correcta
            
            # Cargar el archivo JSON
            self.instruction_data = self.load_json_data()
            self.encoder = InstructionEncoder(self.instruction_data)

        def load_json_data(self):
            """
            Carga los datos del archivo JSON.
            """
            if not os.path.exists(self.json_file_path):
                raise FileNotFoundError(f"El archivo {self.json_file_path} no fue encontrado.")
            
            with open(self.json_file_path, 'r') as file:
                data = json.load(file)
            
            return data["Instrucciones"]
        def process_instruction(self, instruction_line):
            """
            Procesa una línea de instrucción y devuelve su codificación en hexadecimal.
            """
            return self.encoder.encode_instruction(instruction_line)


        def parse_instruction(self, instruction_line):
            """
            Parsea la línea de la instrucción, dividiéndola en el nombre de la instrucción y los operandos.
            Ejemplo: "MOV AX, BX" -> ("MOV", ["AX", "BX"])
            """
            instruction_parts = instruction_line.split(' ')
            instruction = instruction_parts[0]
            operands = instruction_parts[1].split(',')
            operands = [operand.strip() for operand in operands]  # Limpiar espacios
            return instruction, operands

class OpcodeMapper:
    def __init__(self, instruction_data):
        self.instruction_data = instruction_data

    def get_opcode(self, instruction, operands):
        """
        Dado el nombre de la instrucción y los operandos, devuelve el código de operación en binario.
        """
        if instruction not in self.instruction_data:
            raise ValueError(f"Instrucción {instruction} no encontrada en el archivo JSON.")
        
        instruction_details = self.instruction_data[instruction]
        
        # Ahora analizamos los operandos de la instrucción
        # Las claves de los operandos serán del tipo 'Reg/Mem, Reg', 'Reg, Reg/Mem', etc.
        for operand_pattern, details in instruction_details.items():
            # Verificar si la instrucción y los operandos coinciden
            # Simplemente tomamos la codificación binaria de ejemplo
            # Aquí necesitarás un mapeo más sofisticado dependiendo de la instrucción.
            if self.match_operands(operand_pattern, operands):
                return details['codigo']
        
        raise ValueError(f"No se encontró un código para los operandos {operands} con la instrucción {instruction}.")

    def match_operands(self, pattern, operands):
        """
        Función simple para comprobar si el patrón de operandos se ajusta a los operandos dados.
        Este es un lugar donde puedes implementar reglas más complejas si es necesario.
        """
        # Comprobamos de manera muy sencilla si los operandos coinciden (esto es simplificable).
        operand_parts = pattern.split(', ')
        return all(operand in operands for operand in operand_parts)


def bin_to_hex( bin_string):
        """
        Convierte una cadena binaria en su representación hexadecimal, asegurando que esté en Little Endian.
        """
        # Convertimos de binario a entero
        bin_value = int(bin_string, 2)
        
        # Convertimos el valor entero a hexadecimal
        hex_value = hex(bin_value)[2:].upper()
        
        # Aseguramos que la longitud del hexadecimal sea correcta (dos dígitos por byte)
        if len(hex_value) % 2 != 0:
            hex_value = '0' + hex_value
        
        return hex_value

