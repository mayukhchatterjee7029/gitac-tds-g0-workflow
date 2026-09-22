import os
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

app = FastAPI()

# Allow POST (and anything else) from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the bundled telemetry data once, at cold start
DATA_PATH = os.path.join(os.path.dirname(__file__), "telemetry.json")
with open(DATA_PATH) as f:
    RECORDS = json.load(f)

@app.get("/")
def read_root():
    return {"message": "Analytics endpoint is running. POST JSON: {\"regions\": [...], \"threshold_ms\": 180}"}

@app.post("/")
def analytics(payload: dict):
    regions = payload.get("regions", [])
    threshold = payload.get("threshold_ms", 180)

    result = {}
    for region in regions:
        recs = [r for r in RECORDS if r.get("region") == region]
        latencies = [r["latency_ms"] for r in recs]
        uptimes = [r["uptime"] for r in recs]

        result[region] = {
            "avg_latency": float(np.mean(latencies)),
            "p95_latency": float(np.percentile(latencies, 95)),
            "avg_uptime": float(np.mean(uptimes)),
            "breaches": int(sum(1 for x in latencies if x > threshold)),
        }
    return result