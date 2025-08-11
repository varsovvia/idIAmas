import os
from datetime import datetime

def save_image(image):
    folder = "subtitle_captures"
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(folder, f"sub_{timestamp}.png")
    image.save(path)
