import threading
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from pipeline import run_research_pipeline

app = FastAPI(
    title="Agent Research API",
    version="1.0.0",
    description="Run the multi-agent AI research pipeline on a topic and get a report plus critic feedback.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory job store. Each research task runs in a background thread so the
# HTTP request returns immediately and the frontend polls for the result.
JOBS: dict[str, dict] = {}
JOBS_LOCK = threading.Lock()
MAX_JOBS = 200


class ResearchRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=500, description="Research topic")


def _prune_jobs() -> None:
    while len(JOBS) > MAX_JOBS:
        oldest = next(iter(JOBS))
        if JOBS[oldest]["status"] == "pending":
            break
        JOBS.pop(oldest, None)


def _run_job(job_id: str, topic: str) -> None:
    try:
        result = run_research_pipeline(topic)
        with JOBS_LOCK:
            JOBS[job_id] = {"status": "done", "result": result}
    except Exception as exc:  # noqa: BLE001
        with JOBS_LOCK:
            JOBS[job_id] = {"status": "error", "error": str(exc)}


@app.get("/", tags=["system"])
def root():
    return {
        "service": "Agent Research API",
        "status": "ok",
        "docs": "/docs",
        "endpoints": {
            "start_research": "POST /research",
            "get_result": "GET /research/{job_id}",
        },
    }


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}


@app.post("/research", tags=["research"])
def start_research(req: ResearchRequest):
    job_id = uuid.uuid4().hex
    with JOBS_LOCK:
        JOBS[job_id] = {"status": "pending", "topic": req.topic}
        _prune_jobs()
    threading.Thread(target=_run_job, args=(job_id, req.topic), daemon=True).start()
    return {"job_id": job_id}


@app.get("/research/{job_id}", tags=["research"])
def get_research(job_id: str):
    with JOBS_LOCK:
        job = JOBS.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="job not found")
    return job