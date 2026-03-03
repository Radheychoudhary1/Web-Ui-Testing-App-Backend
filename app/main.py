# app/main.py (top-level)
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from app.services.analyzer import analyze_images
from app.schemas import AnalyzeResponse

app = FastAPI(title="Web UI Visual Analyzer", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # keep wide-open until you set your Pages domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(files: List[UploadFile] = File(...)):
    images = [await f.read() for f in files]
    filenames = [f.filename for f in files]
    return analyze_images(images, filenames)

@app.get("/health")
def health():
    return {"ok": True}