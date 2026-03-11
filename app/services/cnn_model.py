import os
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

class ModelManager:
    def __init__(self):
        self.model = None
        self.class_names = [
            "Alignment_Issue",
            "Color_Issue",
            "Hidden_Content",
            "Overlapping_Elements",
            "Correct_UI"
        ]

    def _load(self):
        if self.model is not None:
            return

        model_path = os.path.join(
            os.path.dirname(__file__),
            "../models/ui_bug_detection_cnn_model.keras"
        )

        model_path = os.path.abspath(model_path)

        if os.path.exists(model_path):
            self.model = load_model(model_path)
            print("CNN Model Loaded")
        else:
            print("CNN model not found")

    def detect(self, img: Image.Image):
        self._load()

        if self.model is None:
            return []

        img = img.resize((224,224))
        img_array = np.array(img)/255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = self.model.predict(img_array)

        class_index = np.argmax(prediction)
        confidence = float(np.max(prediction))

        predicted_class = self.class_names[class_index]

        # Unknown detection condition
        if confidence < 0.60:
            return [{
                "type": "Unknown_UI_Defect",
                "severity": "medium",
                "description": "Unknown type of UI defect detected by AI",
                "confidence": confidence
            }]

        if predicted_class == "Correct_UI":
            return []

        return [{
            "type": predicted_class,
            "severity": "medium",
            "description": f"{predicted_class} detected by CNN model",
            "confidence": confidence
        }]