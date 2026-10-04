import logging
from models.schemas import UserInput, ProductAnalysis, SolutionDesign
from services.llm_service import LLMService
from prompts.agent_prompts import (
    SOLUTION_DESIGNER_ROLE,
    SOLUTION_DESIGNER_GOAL,
    SOLUTION_DESIGNER_BACKSTORY,
    build_solution_designer_prompt,
)

logger = logging.getLogger(__name__)

def create_solution_designer_agent():
    """Instantiate CrewAI Agent for Solution Design."""
    try:
        from crewai import Agent
        llm = LLMService.get_crewai_llm()
        return Agent(
            role=SOLUTION_DESIGNER_ROLE,
            goal=SOLUTION_DESIGNER_GOAL,
            backstory=SOLUTION_DESIGNER_BACKSTORY,
            verbose=True,
            allow_delegation=False,
            llm=llm
        )
    except Exception as e:
        logger.warning(f"CrewAI Agent instantiation fallback: {e}")
        return None


def run_solution_designer(user_input: UserInput, product_analysis: ProductAnalysis) -> SolutionDesign:
    """
    Execute Agent 2: Solution & Product Designer.
    Returns structured SolutionDesign.
    """
    prompt = build_solution_designer_prompt(user_input, product_analysis)
    
    solution: SolutionDesign = LLMService.generate_structured(
        prompt=prompt,
        response_model=SolutionDesign,
        system_prompt=f"Role: {SOLUTION_DESIGNER_ROLE}. Goal: {SOLUTION_DESIGNER_GOAL}"
    )

    return solution
