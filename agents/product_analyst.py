import logging
from typing import List
from models.schemas import UserInput, ProductAnalysis, ResearchItem
from services.llm_service import LLMService
from prompts.agent_prompts import (
    PRODUCT_ANALYST_ROLE,
    PRODUCT_ANALYST_GOAL,
    PRODUCT_ANALYST_BACKSTORY,
    build_product_analyst_prompt,
)

logger = logging.getLogger(__name__)

def create_product_analyst_agent():
    """Instantiate CrewAI Agent for Product Analysis."""
    try:
        from crewai import Agent
        llm = LLMService.get_crewai_llm()
        return Agent(
            role=PRODUCT_ANALYST_ROLE,
            goal=PRODUCT_ANALYST_GOAL,
            backstory=PRODUCT_ANALYST_BACKSTORY,
            verbose=True,
            allow_delegation=False,
            llm=llm
        )
    except Exception as e:
        logger.warning(f"CrewAI Agent instantiation fallback: {e}")
        return None


def run_product_analyst(user_input: UserInput, research_items: List[ResearchItem], research_summary: str) -> ProductAnalysis:
    """
    Execute Agent 1: Product & Problem Analyst.
    Returns structured ProductAnalysis.
    """
    prompt = build_product_analyst_prompt(user_input, research_summary)
    
    # Generate structured Pydantic object
    analysis: ProductAnalysis = LLMService.generate_structured(
        prompt=prompt,
        response_model=ProductAnalysis,
        system_prompt=f"Role: {PRODUCT_ANALYST_ROLE}. Goal: {PRODUCT_ANALYST_GOAL}"
    )

    # Attach verified research findings if present
    if research_items:
        analysis.research_findings = research_items

    return analysis
