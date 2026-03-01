from pydantic import BaseModel
from typing import List, Optional

class Issue(BaseModel):
    id: str
    type: str
    bbox: Optional[List[int]] = None  # [x1,y1,x2,y2]
    severity: str
    confidence: float
    evidence: Optional[str] = None
    message: str
    recommendation: str

class ScreenResult(BaseModel):
    filename: str
    size: dict
    issues: List[Issue]
    summary: dict

class AnalyzeResponse(BaseModel):
    screens: List[ScreenResult]