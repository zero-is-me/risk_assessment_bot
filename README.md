# Enterprise Risk Assessment Platform

Advanced multi-agent system for comprehensive enterprise risk assessment.

## Features
- 7 specialized AI agents
- 40+ production tools (200+ parameters)
- Neo4j knowledge graph
- Advanced error recovery
- Zero-hallucination design
- FastAPI REST API
- Docker deployment

## Quick Start

1. Install: `pip install -r requirements.txt`
2. Configure: `cp .env.example .env` (add OPENAI_API_KEY)
3. Deploy: `docker-compose up -d`
4. Run: `python scripts/run_assessment.py`

## API Endpoints

- POST `/api/v1/assess` - Run assessment
- GET `/api/v1/health` - Check health
- GET `/api/v1/assessment/{id}` - Get status

## Complete Workflow

1. **Company Identification** → Verify entity via OpenCorporates/LEI
2. **Parallel Agents** → 7 agents run simultaneously
3. **Data Collection** → 40+ tools fetch 200+ parameters
4. **Knowledge Graph** → Neo4j builds risk relationships
5. **Aggregation** → Cross-validate findings
6. **Report** → Generate comprehensive assessment

## Documentation

See the uploaded documents for complete implementation details:
- COMPLETE-CODEBASE-FULL-PART1.md - Tools and configuration
- COMPLETE-CODEBASE-FULL-PART2.md - Agents and coordinator
- FINAL-DEPLOYMENT-GUIDE.md - Setup and deployment instructions