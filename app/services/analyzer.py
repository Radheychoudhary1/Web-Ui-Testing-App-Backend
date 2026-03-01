from .heuristics import run_heuristics
from .cnn_model import ModelManager
from PIL import Image
import io
import numpy as np

_model = ModelManager()  # lazy loads on first use

def analyze_images(image_bytes_list, filenames):
    screens = []
    for data, name in zip(image_bytes_list, filenames):
        img = Image.open(io.BytesIO(data)).convert("RGB")
        w, h = img.size

        # 1) Heuristics (instant, no training)
        issues = run_heuristics(img)

        # 2) CNN-based detections (optional if weights available)
        cnn_issues = _model.detect(img)
        issues.extend(cnn_issues)

        # build summary
        severity_rank = {"low":0,"medium":1,"high":2}
        summary = {
            "count": len(issues),
            "high": sum(1 for i in issues if i["severity"]=="high"),
            "medium": sum(1 for i in issues if i["severity"]=="medium"),
            "low": sum(1 for i in issues if i["severity"]=="low"),
        }
        screens.append({
            "filename": name,
            "size": {"w": w, "h": h},
            "issues": issues,
            "summary": summary
        })
    return {"screens": screens}