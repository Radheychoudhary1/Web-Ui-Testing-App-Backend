from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from app.services.analyzer import analyze_images
from app.schemas import AnalyzeResponse
from typing import List

app = FastAPI(title="Web UI Visual Analyzer", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(files: List[UploadFile] = File(...)):
    images = [await f.read() for f in files]
    filenames = [f.filename for f in files]
    result = analyze_images(images, filenames)
    return result