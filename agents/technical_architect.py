import logging
from models.schemas import UserInput, ProductAnalysis, SolutionDesign, TechnicalSpecification
from services.llm_service import LLMService
from prompts.agent_prompts import (
    TECHNICAL_ARCHITECT_ROLE,
    TECHNICAL_ARCHITECT_GOAL,
    TECHNICAL_ARCHITECT_BACKSTORY,
    build_technical_architect_prompt,
)

logger = logging.getLogger(__name__)

def create_technical_architect_agent():
    """Instantiate CrewAI Agent for Technical Architecture."""
    try:
        from crewai import Agent
        llm = LLMService.get_crewai_llm()
        return Agent(
            role=TECHNICAL_ARCHITECT_ROLE,
            goal=TECHNICAL_ARCHITECT_GOAL,
            backstory=TECHNICAL_ARCHITECT_BACKSTORY,
            verbose=True,
            allow_delegation=False,
            llm=llm
        )
    except Exception as e:
        logger.warning(f"CrewAI Agent instantiation fallback: {e}")
        return None


def run_technical_architect(
    user_input: UserInput,
    product_analysis: ProductAnalysis,
    solution_design: SolutionDesign
) -> TechnicalSpecification:
    """
    Execute Agent 3: Technical Architect & Requirements Engineer.
    Returns structured TechnicalSpecification.
    """
    prompt = build_technical_architect_prompt(user_input, product_analysis, solution_design)
    
    tech_spec: TechnicalSpecification = LLMService.generate_structured(
        prompt=prompt,
        response_model=TechnicalSpecification,
        system_prompt=f"Role: {TECHNICAL_ARCHITECT_ROLE}. Goal: {TECHNICAL_ARCHITECT_GOAL}"
    )

    return tech_spec
