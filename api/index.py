import json
import os
from typing import List
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import numpy as np

app = FastAPI()

# CORS – allow POST from any origin (restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # or specific origins like ["https://your-dashboard.com"]
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Load telemetry bundle once at cold start
TELEMETRY_PATH = os.path.join(os.path.dirname(__file__), "telemetry.json")
with open(TELEMETRY_PATH, "r") as f:
    TELEMETRY = json.load(f)      # expected: list of dicts with "region", "latency_ms", "uptime"

@app.post("/analytics")
async def analytics(request: Request):
    body = await request.json()
    regions: List[str] = body.get("regions", [])
    threshold_ms: float = body.get("threshold_ms", 180)

    # Filter telemetry for requested regions
    filtered = [r for r in TELEMETRY if r["region"] in regions]

    result = {}
    for region in regions:
        region_data = [r for r in filtered if r["region"] == region]
        if not region_data:
            result[region] = {
                "avg_latency": None,
                "p95_latency": None,
                "avg_uptime": None,
                "breaches": 0,
            }
            continue

        latencies = [r["latency_ms"] for r in region_data]
        uptimes   = [r["uptime"] for r in region_data]

        avg_latency = float(np.mean(latencies))
        p95_latency = float(np.percentile(latencies, 95))
        avg_uptime  = float(np.mean(uptimes))
        breaches    = sum(1 for l in latencies if l > threshold_ms)

        result[region] = {
            "avg_latency": round(avg_latency, 2),
            "p95_latency": round(p95_latency, 2),
            "avg_uptime": round(avg_uptime, 2),
            "breaches": breaches,
        }

    return JSONResponse(content=result)