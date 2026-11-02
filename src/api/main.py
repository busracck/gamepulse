from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes.stats import router as stats_router

app = FastAPI(
    title="GamePulse API",
    description="Mobile Game Analytics REST API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(stats_router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "GamePulse API"}