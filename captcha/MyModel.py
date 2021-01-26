import muggle_ocr
from PIL import Image
from io import BytesIO
import numpy as np

class MyModel:
    def __init__(self):
        self.sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)# Load 模型在這裡
        #self._model = tf.keras.models.load_model('tf-mnist-model.h5') # Load 模型在這裡

    def predict(self, request, names=None, meta=None): # 此函數會被呼叫
        print('calling predict()...')
        img_path = "tmp.png"
        imageStream = BytesIO(request)
        image = Image.open(imageStream).convert('RGB')
        image.save(img_path)
        
        with open(img_path, "rb") as f:
            captcha_bytes = f.read()
        
        text = self.sdk.predict(image_bytes=captcha_bytes)
        return {"prediction": text}

    def tags(self):
        return {}

    def metrics(self):
        return []