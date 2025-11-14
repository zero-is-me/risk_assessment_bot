from agents.base_agent import BaseAgent
from tools.comprehensive_tools import (
    check_sanctions_ofac,
    check_pep_status,
    check_export_controls,
    check_aml_compliance,
    get_regulatory_violations
)
from config.prompts import get_agent_prompt

def create_compliance_agent() -> BaseAgent:
    """Compliance and regulatory risk agent"""
    
    return BaseAgent(
        name="compliance_agent",
        role="Compliance & Regulatory Officer",
        goals=[
            "Screen against OFAC, UN, EU sanctions lists",
            "Check PEP (Politically Exposed Persons) status",
            "Verify export control compliance",
            "Monitor AML regulatory requirements",
            "Track regulatory violations and enforcement",
            "Assess data protection compliance",
            "Monitor industry-specific regulations"
        ],
        tools=[
            check_sanctions_ofac,
            check_pep_status,
            check_export_controls,
            check_aml_compliance,
            get_regulatory_violations
        ],
        system_prompt=get_agent_prompt("compliance")
    )
