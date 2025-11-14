import asyncio
import sys
from pathlib import Path
import logging

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.coordinator_agent import CoordinatorAgent
from config.logging_config import setup_logging
from config.settings import settings

setup_logging(settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting Enterprise Risk Assessment Platform")
    logger.info("=" * 80)
    coordinator = CoordinatorAgent()
    result = await coordinator.run_assessment(
        company_name="Apple Inc.",
        ticker="AAPL",
        country="US",
        domain="apple.com",
        sectors=["Technology", "Consumer Electronics"]
    )
    print("\n" + result["report"])
    logger.info(f"\nAssessment ID: {result['assessment_id']}")
    logger.info(f"Status: {result['status']}")

if __name__ == "__main__":
    asyncio.run(main())
