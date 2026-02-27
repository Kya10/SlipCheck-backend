from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from risk_engine import analyze_slip
from fastapi.middleware.cors import CORSMiddleware

def normalize_market(market: str):
    m = market.lower().strip()

    if "over" in m:
        return {"category": "goals_over", "line": m}
    if "under" in m:
        return {"category": "goals_under", "line": m}
    if "1x" in m or "double chance" in m:
        return {"category": "double_chance", "line": m}
    if "btts" in m or "both teams" in m:
        return {"category": "btts", "line": m}
    if "handicap" in m or "ah" in m:
        return {"category": "handicap", "line": m}
    if "corner" in m:
        return {"category": "corners", "line": m}
    if "card" in m:
        return {"category": "cards", "line": m}

    return {"category": "other", "line": m}
    
app = FastAPI()
@app.get("/")
def root():
    return {"status": "Slipcheck API running"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # simple fix for MVP
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Leg(BaseModel):
    match: str
    market: str
    odds: float


class Slip(BaseModel):
    legs: List[Leg]


def analyze_slip(legs):
    risk_score = 0
    warnings = []
    suggestions = []
    flagged_legs = []

    for leg in legs:
        # normalization
        category = normalize_market(leg["market"])
        leg["category"] = category

        print("Normalized:", leg["market"], "→", category)

        # example scoring logic (keep your real logic)
        if category == "goals_over":
            warnings.append("Goals markets carry higher variance due to late scoring swings")

        # continue existing scoring logic here...

    return {
        "risk_score": risk_score,
        "warnings": warnings,
        "suggestions": suggestions,
        "flagged_legs": flagged_legs
    }


