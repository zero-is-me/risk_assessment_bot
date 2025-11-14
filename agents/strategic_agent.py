from agents.base_agent import BaseAgent
from tools.comprehensive_tools import (
    get_competitive_landscape,
    get_ma_activity,
    get_patent_trends
)
from config.prompts import get_agent_prompt

def create_strategic_agent() -> BaseAgent:
    """Strategic risk analyst agent"""
    
    return BaseAgent(
        name="strategic_agent",
        role="Strategic Risk Analyst",
        goals=[
            "Analyze competitive landscape and positioning",
            "Monitor M&A activity and consolidation",
            "Track innovation and patent trends",
            "Assess technology disruption risks",
            "Identify regulatory change impacts",
            "Evaluate market share dynamics",
            "Monitor competitive threats and new entrants"
        ],
        tools=[
            get_competitive_landscape,
            get_ma_activity,
            get_patent_trends
        ],
        system_prompt=get_agent_prompt("strategic")
    )
