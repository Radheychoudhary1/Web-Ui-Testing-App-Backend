# app/services/cnn_model.py
import os
from PIL import Image

try:
    import torch
    import torchvision.transforms as T
    TORCH_AVAILABLE = True
except Exception:
    TORCH_AVAILABLE = False
    T = None

class ModelManager:
    def __init__(self):
        self.device = "cuda" if TORCH_AVAILABLE and hasattr(torch, "cuda") and torch.cuda.is_available() else "cpu"
        self.model = None
        self.transforms = None

    def _load(self):
        if self.model is not None:
            return
        if not TORCH_AVAILABLE:
            return  # Skip CNN if torch is not installed
        weights_path = os.getenv("CNN_WEIGHTS", "models/ui_detector.pt")
        if os.path.exists(weights_path):
            # self.model = torch.load(weights_path, map_location=self.device)
            # self.model.eval()
            pass
        self.transforms = T.Compose([T.Resize((640, 640)), T.ToTensor()])

    def detect(self, img: Image.Image):
        self._load()
        if not TORCH_AVAILABLE or self.model is None:
            return []
        # TODO: run model, parse detections
        return []