import os
from PIL import Image
import torch
import torchvision.transforms as T

class ModelManager:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None   # lazy load

    def _load(self):
        if self.model is not None: return
        weights_path = os.getenv("CNN_WEIGHTS", "models/ui_detector.pt")
        if os.path.exists(weights_path):
            # Example: a Torch FasterRCNN or custom head
            # self.model = torch.load(weights_path, map_location=self.device)
            # self.model.eval()
            pass
        else:
            self.model = None

        self.transforms = T.Compose([
            T.Resize((640, 640)),
            T.ToTensor(),
        ])

    def detect(self, img: Image.Image):
        self._load()
        if self.model is None:
            return []  # clean fallback until you train/ship weights

        x = self.transforms(img).unsqueeze(0).to(self.device)
        with torch.no_grad():
            out = self.model(x)  # adapt to your model's output format
        # TODO: parse out → list of issues with bbox/severity/confidence
        return []