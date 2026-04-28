from fastapi import FastAPI
import csv
import os
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://portafolio-nextjs-neon.vercel.app",
    "https://portafolio-20-eta.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # solo estos dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
archivo = "contador.csv"

# Inicializar archivo si no existe
if not os.path.exists(archivo):
    with open(archivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "fecha"])

def obtener_ultimo_id():
    with open(archivo, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        filas = list(reader)
        if len(filas) > 1:
            return int(filas[-1][0])
        return 0

@app.get("/visita")
def registrar_visita():
    ultimo_id = obtener_ultimo_id()
    nuevo_id = ultimo_id + 1
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(archivo, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([nuevo_id, fecha])

    return {"mensaje": "Visita registrada", "id": nuevo_id, "fecha": fecha}

@app.get("/visitas")
def leer_visitas():
    with open(archivo, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)
