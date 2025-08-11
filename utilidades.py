import os
from datetime import datetime

def guardar_imagen(imagen):
    carpeta = "capturas_subtitulos"
    os.makedirs(carpeta, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta = os.path.join(carpeta, f"sub_{timestamp}.png")
    imagen.save(ruta)
