from agents.base_agent import BaseAgent
from tools.comprehensive_tools import (
    get_stock_price, get_sec_filings, get_financial_statements,
    get_gdp_growth, get_inflation_rate, get_unemployment_rate
)
from config.prompts import get_agent_prompt

def create_financial_agent() -> BaseAgent:
    """Financial risk assessment agent"""
    
    return BaseAgent(
        name="financial_agent",
        role="Financial Risk Specialist",
        goals=[
            "Assess stock performance and market sentiment",
            "Analyze financial statements and ratios",
            "Evaluate debt levels and credit risk",
            "Monitor liquidity and working capital",
            "Track commodity and currency exposure",
            "Identify bankruptcy and default risks",
            "Assess market volatility impacts"
        ],
        tools=[
            get_stock_price,
            get_sec_filings,
            get_financial_statements,
            get_gdp_growth,
            get_inflation_rate,
            get_unemployment_rate
        ],
        system_prompt=get_agent_prompt("financial")
    )
