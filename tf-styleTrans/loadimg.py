import numpy as np
from PIL import Image
import requests
from io import BytesIO

def load_img_rgb(img_file_pth):
    if img_file_pth[:4]=="http":
        response = requests.get(img_file_pth)
        img_rgb = Image.open(BytesIO(response.content)).convert("RGB")
    else:
        img_rgb = Image.open(img_file_pth).convert("RGB")   
    return img_rgb
    
    
