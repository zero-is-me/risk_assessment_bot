from agents.base_agent import BaseAgent
from tools.comprehensive_tools import (
    get_news_sentiment,
    get_customer_reviews,
    get_social_media_sentiment,
    get_brand_reputation_score,
    get_employee_satisfaction
)
from config.prompts import get_agent_prompt

def create_reputation_agent() -> BaseAgent:
    """Reputational risk analyst agent"""
    
    return BaseAgent(
        name="reputation_agent",
        role="Reputational Risk Analyst",
        goals=[
            "Monitor social media sentiment across platforms",
            "Analyze customer reviews and satisfaction",
            "Track news coverage and media sentiment",
            "Identify influencer and thought leader mentions",
            "Assess employee satisfaction and engagement",
            "Detect brand perception trends",
            "Identify emerging reputational crises"
        ],
        tools=[
            get_news_sentiment,
            get_customer_reviews,
            get_social_media_sentiment,
            get_brand_reputation_score,
            get_employee_satisfaction
        ],
        system_prompt=get_agent_prompt("reputation")
    )
