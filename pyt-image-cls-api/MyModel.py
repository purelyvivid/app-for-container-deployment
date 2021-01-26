import torch
import torchvision
from PIL import Image
from torchvision import transforms
import numpy as np
from io import BytesIO

class MyModel:
    def __init__(self):
        
        self.model = torch.hub.load('pytorch/vision:v0.5.0', 'mobilenet_v2', pretrained=True)# Load 模型在這裡
        self.model.eval()
        with open("imagenet1000_clsidx_to_labels.txt","r") as f:
            self.classes = eval(f.read().replace("\n",""))

        self.preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        
        # move the input and model to GPU for speed if available
        if torch.cuda.is_available():
            self.model.to('cuda')

    def predict(self, request, names=None, meta=None): # 此函數會被呼叫
        
        print('calling predict()...')
        imageStream = BytesIO(request)
        input_image = Image.open(imageStream).convert('RGB')
        
        input_tensor = self.preprocess(input_image)
        input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model
        # move the input and model to GPU for speed if available
        if torch.cuda.is_available():
            input_batch = input_batch.to('cuda')
            
        with torch.no_grad():
            output = self.model(input_batch)
            # Tensor of shape 1000, with confidence scores over Imagenet's 1000 classes
            #print(output[0].shape)
            # The output has unnormalized scores. To get probabilities, you can run a softmax on it.
        logits = torch.nn.functional.softmax(output[0], dim=0)
        idx = np.argmax(logits.cpu().data.numpy())
        #print("預測結果：",classes[idx])
        return {"prediction": self.classes[idx]}

    def tags(self):
        return {}

    def metrics(self):
        return []