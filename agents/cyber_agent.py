from agents.base_agent import BaseAgent
from tools.comprehensive_tools import (
    check_data_breaches,
    check_cve_vulnerabilities,
    check_domain_reputation,
    check_ransomware_risk
)
from config.prompts import get_agent_prompt

def create_cyber_agent() -> BaseAgent:
    """Cybersecurity risk officer agent"""
    
    return BaseAgent(
        name="cyber_agent",
        role="Cybersecurity Risk Officer",
        goals=[
            "Check data breach history and exposure",
            "Scan for CVEs and security vulnerabilities",
            "Monitor domain reputation",
            "Assess ransomware and malware threats",
            "Evaluate API and application security",
            "Track insider threat risks",
            "Monitor third-party security incidents"
        ],
        tools=[
            check_data_breaches,
            check_cve_vulnerabilities,
            check_domain_reputation,
            check_ransomware_risk
        ],
        system_prompt=get_agent_prompt("cyber")
    )
