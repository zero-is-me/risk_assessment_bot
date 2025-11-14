import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agents.coordinator_agent import CoordinatorAgent
from config.logging_config import setup_logging
from config.settings import settings
from datetime import datetime

setup_logging(settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Multi-agent enterprise risk assessment platform"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

coordinator = CoordinatorAgent()

@app.get("/")
async def root():
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/v1/assess")
async def create_assessment(
    company_name: str,
    ticker: str = None,
    country: str = "US",
    domain: str = None,
    sectors: list = None
):
    result = await coordinator.run_assessment(
        company_name=company_name,
        ticker=ticker,
        country=country,
        domain=domain,
        sectors=sectors or ["Technology"]
    )
    return result

@app.get("/api/v1/health")
async def health_check():
    agent_health = await coordinator.health_check()
    return {
        "status": "healthy",
        "agents": agent_health,
        "coordinator_status": coordinator.status,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/assessment/{assessment_id}")
async def get_assessment(assessment_id: str):
    return {
        "assessment_id": assessment_id,
        "status": "pending",
        "message": "Use /api/v1/assess to run assessment"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
