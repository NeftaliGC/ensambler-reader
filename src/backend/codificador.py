import json
from pathlib import Path

class Codificador:
    def __init__(self):
        # Ruta al archivo JSON con las instrucciones
        self.json_path = Path(__file__).parent / "data" / "instrucciones_completas.json"
        # Cargar las instrucciones desde el archivo JSON
        self.instrucciones = self.cargar_instrucciones()

    def cargar_instrucciones(self):
        """
        Carga las instrucciones desde el archivo JSON y las devuelve.
        """
        with open(self.json_path, 'r', encoding='utf-8') as file:
            return json.load(file)["Instrucciones"]

    def procesar_linea(self, linea):
        """
        Recibe una línea de código en ensamblador, separa la instrucción y los operandos,
        y luego genera el código de máquina correspondiente.
        """
        # Normalizamos la línea eliminando espacios extra y comentarios
        linea = linea.strip()
        if ';' in linea:
            linea = linea.split(';')[0].strip()  # Elimina los comentarios

        # Dividimos la línea en la instrucción y los operandos
        partes = linea.split()
        if len(partes) == 0:
            raise ValueError("La línea está vacía o no es válida.")
        
        instruccion = partes[0].upper()  # La instrucción es la primera palabra
        operandos = [op.strip(',') for op in partes[1:]]  # Eliminar comas al final de cada operando

        # Codificamos la instrucción con los operandos
        return self.codificar_instruccion(instruccion, operandos)

    def obtener_instruccion(self, nombre_instruccion):
        """
        Devuelve la estructura de la instrucción con base en el nombre.
        """
        for instr_set in self.instrucciones:
            if nombre_instruccion in instr_set:
                return instr_set[nombre_instruccion]
        return None

    def codificar_instruccion(self, instruccion, operandos):
        """
        Recibe el nombre de una instrucción y sus operandos para generar el código de máquina.
        """
        # Se obtiene la estructura de la instrucción del JSON.
        instruccion_info = self.obtener_instruccion(instruccion)

        if not instruccion_info:
            raise ValueError(f"Instrucción '{instruccion}' no encontrada en el archivo JSON.")

        # Dependiendo del tipo de instrucción, procesamos los operandos
        for tipo_operando, detalles in instruccion_info.items():
            if ',' in tipo_operando:  # Instrucciones con 2 operandos
                if len(operandos) != 2:
                    raise ValueError(f"La instrucción '{instruccion}' requiere 2 operandos.")
                return self.codificar_reg_mem_reg(detalles, operandos)
            elif 'Sin operandos' in tipo_operando:  # Instrucciones sin operandos
                return self.bin_a_hex(detalles["base"])

        return None

    def codificar_reg_mem_reg(self, detalles, operandos):
        """
        Codifica una instrucción del tipo 'Reg/Mem, Reg'.
        """
        # Extraemos la información de la estructura del JSON
        base = detalles["base"]
        mod = "00"  # Suponemos 'Memoria sin desplazamiento' por defecto

        # Procesamos el primer operando (reg)
        reg = operandos[0]
        reg_bin = self.obtener_registro_bin(reg)

        # Procesamos el segundo operando (rm)
        rm = operandos[1]
        rm_bin = self.obtener_rm_bin(rm)

        # Codificación binaria completa
        codificacion_bin = base + mod + reg_bin + rm_bin

        # Convertimos la codificación binaria a hexadecimal
        return self.bin_a_hex(codificacion_bin)

    def obtener_registro_bin(self, reg):
        """
        Convierte el nombre de un registro a su valor binario correspondiente.
        """
        registros = {
            "AX": "000",
            "CX": "001",
            "DX": "010",
            "BX": "011",
            "SP": "100",
            "BP": "101",
            "SI": "110",
            "DI": "111"
        }

        if reg in registros:
            return registros[reg]
        else:
            raise ValueError(f"Registro '{reg}' no reconocido.")

    def obtener_rm_bin(self, rm):
        """
        Convierte el valor de un operando 'r/m' a su valor binario.
        """
        # Aquí definimos los operandos comunes para los registros y memoria
        r_m_values = {
            "BX+SI": "000",
            "BX+DI": "001",
            "BP+SI": "010",
            "BP+DI": "011",
            "SI": "100",
            "DI": "101",
            "BP": "110",
            "BX": "111"
        }

        if rm in r_m_values:
            return r_m_values[rm]
        else:
            raise ValueError(f"Operando 'r/m' '{rm}' no reconocido.")

    def bin_a_hex(self, binario):
        """
        Convierte una cadena binaria a su representación hexadecimal.
        """
        # Aseguramos que la longitud de la cadena binaria sea múltiplo de 4
        binario_completo = binario.zfill(len(binario) + (4 - len(binario) % 4) % 4)

        # Convertimos binario a hexadecimal
        hexadecimal = hex(int(binario_completo, 2))[2:].upper()  # Convertimos a hex y eliminamos el '0x' inicial
        return hexadecimal

# Ejemplo de uso
if __name__ == "__main__":
    codificador = Codificador()

    # Línea de código en ensamblador
    linea = "MOV AX, BX+SI"

    # Procesar la línea
    codigo_maquina = codificador.procesar_linea(linea)

    # Mostrar el código de máquina en hexadecimal
    print(f"Código de máquina para '{linea}': {codigo_maquina}")
