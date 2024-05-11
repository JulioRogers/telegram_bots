import json
import os

# Definir la ruta del archivo JSON que actuará como base de datos
db_path = "nomoreslavery/datasets/chat_threads.json"

# Función para cargar o inicializar la base de datos
def load_or_initialize_db():
    if os.path.exists(db_path):
        with open(db_path, "r") as file:
            return json.load(file)
    else:
        return {}

# Función para guardar la base de datos
def save_db(db):
    with open(db_path, "w") as file:
        json.dump(db, file, indent=4)