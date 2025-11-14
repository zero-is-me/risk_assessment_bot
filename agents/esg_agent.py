from agents.base_agent import BaseAgent
from tools.comprehensive_tools import (
    get_carbon_footprint,
    get_esg_score,
    get_water_stress_risk,
    get_diversity_metrics
)
from config.prompts import get_agent_prompt

def create_esg_agent() -> BaseAgent:
    """ESG and sustainability analyst agent"""
    
    return BaseAgent(
        name="esg_agent",
        role="ESG & Sustainability Analyst",
        goals=[
            "Assess carbon emissions and climate exposure",
            "Calculate ESG scores and ratings",
            "Evaluate water stress and scarcity",
            "Monitor diversity and inclusion metrics",
            "Track sustainability commitments",
            "Assess climate disaster risks",
            "Monitor environmental compliance"
        ],
        tools=[
            get_carbon_footprint,
            get_esg_score,
            get_water_stress_risk,
            get_diversity_metrics
        ],
        system_prompt=get_agent_prompt("esg")
    )
