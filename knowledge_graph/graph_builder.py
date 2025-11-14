import logging
from typing import Dict, Any
from datetime import datetime

try:
    from neo4j import GraphDatabase
except ImportError:
    GraphDatabase = None

from config.settings import settings

logger = logging.getLogger(__name__)

class GraphBuilder:
    """Neo4j knowledge graph builder"""

    def __init__(self):
        if GraphDatabase is None:
            logger.warning("Neo4j is not available. Graph operations disabled.")
            self.driver = None
        else:
            try:
                self.driver = GraphDatabase.driver(
                    settings.NEO4J_URI,
                    auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
                    max_connection_lifetime=1000
                )
                logger.info("Connected to Neo4j")
            except Exception as e:
                logger.error(f"Failed to connect to Neo4j: {e}")
                self.driver = None

    async def create_company_node(self, company_data: Dict[str, Any]):
        if not self.driver:
            return
        with self.driver.session() as session:
            session.run(
                "MERGE (c:Company {name: $name}) SET c += $props RETURN c",
                name=company_data.get("name"),
                props={
                    "ticker": company_data.get("ticker"),
                    "country": company_data.get("country"),
                    "domain": company_data.get("domain"),
                    "updated": datetime.now().isoformat()
                }
            )

    async def create_risk_node(self, company_name: str, risk_type: str, risk_data: Dict[str, Any]):
        if not self.driver:
            return
        with self.driver.session() as session:
            session.run(
                """
                MATCH (c:Company {name: $company_name})
                CREATE (r:Risk {type: $risk_type, score: $score, confidence: $confidence, description: $description, timestamp: datetime()})
                CREATE (c)-[:HAS_RISK]->(r)
                RETURN r
                """,
                company_name=company_name,
                risk_type=risk_type,
                score=risk_data.get("score", 0),
                confidence=risk_data.get("confidence", "MEDIUM"),
                description=risk_data.get("description", "")
            )

    def close(self):
        if self.driver:
            self.driver.close()
