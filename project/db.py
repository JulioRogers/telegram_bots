import json
import os


# Función para cargar o inicializar la base de datos
def load_or_initialize_db(db_path):
    if os.path.exists(db_path):
        with open(db_path, "r") as file:
            return json.load(file)
    else:
        return {}

# Función para guardar la base de datos
def save_db(db, db_path):
    with open(db_path, "w") as file:
        json.dump(db, file, indent=4)

def cargar_ultimo_identificador(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            if data:  # Verifica si el archivo JSON tiene datos
                # Asume que el último identificador está en la última entrada agregada
                last_id = list(data.values())[-1]  # Asumiendo que los identificadores están almacenados como valores
                return int(last_id)  # Convierte el identificador a entero
            else:
                return 0
    except FileNotFoundError:
        return 0  # Si el archivo no existe, comienza desde 0
    except json.JSONDecodeError:
        return 0  # Si el archivo está corrupto o mal formateado, comienza desde 0

def generador_identificador(filename):
    start_id = cargar_ultimo_identificador(filename) + 1
    for i in range(start_id, 10000):  # Comienza desde el último + 1
        yield f"{i:04d}"
