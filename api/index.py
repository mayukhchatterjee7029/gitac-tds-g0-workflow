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
        uptimes = [r["uptime_pct"] for r in recs]   # <-- field name from the bundle
        result[region] = {
            "avg_latency": float(np.mean(latencies)),
            "p95_latency": float(np.percentile(latencies, 95)),
            "avg_uptime": float(np.mean(uptimes)),
            "breaches": int(sum(1 for x in latencies if x > threshold)),
        }
    return result


# Content-driven handler: ANY request carrying a JSON body with "regions"
# gets metrics back. Survives Vercel 308 trailing-slash redirects that
# downgrade POSTs to GETs.
@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "OPTIONS"])
async def analytics(request: Request, full_path: str):
    payload = None
    if request.method in ("POST", "PUT"):
        try:
            payload = await request.json()
        except Exception:
            payload = None
    if not isinstance(payload, dict) or "regions" not in payload:
        q = request.query_params
        if "regions" in q:
            payload = {
                "regions": q["regions"].split(","),
                "threshold_ms": float(q.get("threshold_ms", 180)),
            }
    if isinstance(payload, dict) and "regions" in payload:
        regions = payload.get("regions", [])
        threshold = payload.get("threshold_ms", 180)
        return compute_metrics(regions, threshold)
    return JSONResponse({
        "message": "Analytics endpoint is running. POST JSON: {\"regions\": [...], \"threshold_ms\": 180}"
    })