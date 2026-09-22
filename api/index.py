from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json, os
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

class Payload(BaseModel):
    regions: List[str]
    threshold_ms: float = 180

# Load telemetry (adjust to how you stored it)
TELEMETRY = json.load(open(os.path.join(os.path.dirname(__file__), "telemetry.json")))
# If telemetry.json is a dict with a "records" or similar key, drill into it here.

@app.post("/analytics")
def analytics(payload: Payload):
    result = {}
    for region in payload.regions:
        rows = [r for r in TELEMETRY if r["region"] == region]
        if not rows:
            result[region] = {"avg_latency": None, "p95_latency": None,
                              "avg_uptime": None, "breaches": 0}
            continue
        lat = [r["latency_ms"] for r in rows]
        up  = [r["uptime"] for r in rows]
        result[region] = {
            "avg_latency": round(float(np.mean(lat)), 2),
            "p95_latency": round(float(np.percentile(lat, 95)), 2),
            "avg_uptime":  round(float(np.mean(up)), 2),
            "breaches":    sum(1 for x in lat if x > payload.threshold_ms),
        }
    return result