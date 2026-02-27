from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from risk_engine import analyze_slip

app = FastAPI()
@app.get("/")
def root():
    return {"status": "Slipcheck API running"}

class Leg(BaseModel):
    match: str
    market: str
    odds: float


class Slip(BaseModel):
    legs: List[Leg]


@app.post("/analyze-slip")
def analyze(slip: Slip):
    result = analyze_slip([leg.dict() for leg in slip.legs])

    return result
