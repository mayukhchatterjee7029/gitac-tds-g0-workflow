import os
import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "telemetry.json")
with open(DATA_PATH) as f:
    RECORDS = json.load(f)


def compute_metrics(regions, threshold):
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


# Handle GET and POST on every possible path (/, /api, /api/index, anything).
# This makes the endpoint immune to vercel.json routing quirks.
@app.api_route("/{full_path:path}", methods=["GET", "POST"])
async def analytics(request: Request, full_path: str):
    if request.method == "POST":
        try:
            payload = await request.json()
        except Exception:
            payload = {}
        regions = payload.get("regions", [])
        threshold = payload.get("threshold_ms", 180)
        return compute_metrics(regions, threshold)
    return JSONResponse({"message": "Analytics endpoint is running. POST JSON: {\"regions\": [...], \"threshold_ms\": 180}"})