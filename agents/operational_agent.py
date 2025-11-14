from agents.base_agent import BaseAgent
from tools.comprehensive_tools import (
    check_supplier_health,
    get_supply_chain_risk,
    get_logistics_status,
    get_raw_material_availability,
    get_business_continuity_status
)
from config.prompts import get_agent_prompt

def create_operational_agent() -> BaseAgent:
    """Operational risk manager agent"""
    
    return BaseAgent(
        name="operational_agent",
        role="Operational Risk Manager",
        goals=[
            "Assess supplier financial health",
            "Evaluate supply chain resilience",
            "Monitor logistics and distribution risks",
            "Track raw material availability",
            "Evaluate business continuity readiness",
            "Identify single points of failure",
            "Assess geographic concentration risks"
        ],
        tools=[
            check_supplier_health,
            get_supply_chain_risk,
            get_logistics_status,
            get_raw_material_availability,
            get_business_continuity_status
        ],
        system_prompt=get_agent_prompt("operational")
    )
