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
        return f"Error: La línea '{linea}' no tiene el formato esperado (instrucción operandos)."
    
    instruccion = partes[0]
    operando = partes[1]
    
    return instruccion, operando

# Función para codificar la instrucción
def codificar_instruccion(instruccion, operando, opcodes):
    if instruccion in opcodes:
        if operando in opcodes[instruccion]:
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

# Ejemplo de uso
if __name__ == "__main__":
    # Cargar los opcodes desde el archivo JSON
    opcodes = cargar_opcodes()

    # Entrada del usuario (se puede cambiar por un input())
    entrada = "IMUL AX, BX" # Ejemplo de entrada
    
    # Procesar la instrucción y mostrar el código de máquina
    resultado = procesar_instruccion(entrada, opcodes)
    print(f"Resultado para '{entrada}': {resultado}")

