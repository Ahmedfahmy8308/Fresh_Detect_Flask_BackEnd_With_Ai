import os
from PIL import Image
import torch
import torchvision.transforms as transforms
import torchvision.models as models

class PredictService:
    def __init__(self):
        self.target_classes = [
            "FreshApple", "FreshBanana", "FreshMango", "FreshOrange", "FreshStrawberry",
            "RottenApple", "RottenBanana", "RottenMango", "RottenOrange", "RottenStrawberry",
            "FreshCarrot", "FreshPotato", "FreshTomato", "FreshCucumber", "FreshBellpepper",
            "RottenCarrot", "RottenPotato", "RottenTomato", "RottenCucumber", "RottenBellpepper"
        ]
        self.upload_folder = 'static/uploads'
        self.model = self.load_model()

    def load_model(self):
        model = models.resnet18(pretrained=True)
        num_ftrs = model.fc.in_features
        model.fc = torch.nn.Linear(num_ftrs, len(self.target_classes))
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = model.to(device)
        model.load_state_dict(torch.load("Model/best_model.pth", map_location=device))
        model.eval()
        return model

    def predict(self, image_path):
        if not os.path.exists(image_path):
            return "Error: Image path does not exist."

        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        image = Image.open(image_path).convert('RGB')
        image = transform(image).unsqueeze(0)

        with torch.no_grad():
            outputs = self.model(image)
            _, predicted = torch.max(outputs, 1)

        return self.target_classes[predicted.item()]