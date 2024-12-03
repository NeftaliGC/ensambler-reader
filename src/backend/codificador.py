import json
import os

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

    def bin_to_hex(self, bin_string):
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


def main():
    # Crear el objeto que maneja las instrucciones
    parser = InstructionParser()
    
    # Instrucción que deseas codificar
    instruction_line = "MOV AX, BX"
    
    # Procesamos la instrucción y obtenemos la codificación hexadecimal
    hex_output = parser.process_instruction(instruction_line)
    
    print(f"Codificación hexadecimal: {hex_output}")

if __name__ == "__main__":
    main()
