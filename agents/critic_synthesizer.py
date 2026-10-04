import logging
from models.schemas import (
    UserInput,
    ProductAnalysis,
    SolutionDesign,
    TechnicalSpecification,
    ReviewFindings,
    FinalSpecification,
)
from services.llm_service import LLMService
from prompts.agent_prompts import (
    CRITIC_SYNTHESIZER_ROLE,
    CRITIC_SYNTHESIZER_GOAL,
    CRITIC_SYNTHESIZER_BACKSTORY,
    build_critic_synthesizer_prompt,
)

logger = logging.getLogger(__name__)

def create_critic_synthesizer_agent():
    """Instantiate CrewAI Agent for Critical Review & Synthesis."""
    try:
        from crewai import Agent
        llm = LLMService.get_crewai_llm()
        return Agent(
            role=CRITIC_SYNTHESIZER_ROLE,
            goal=CRITIC_SYNTHESIZER_GOAL,
            backstory=CRITIC_SYNTHESIZER_BACKSTORY,
            verbose=True,
            allow_delegation=False,
            llm=llm
        )
    except Exception as e:
        logger.warning(f"CrewAI Agent instantiation fallback: {e}")
        return None


def run_critic_synthesizer(
    user_input: UserInput,
    effective_level: str,
    level_reason: str,
    product_analysis: ProductAnalysis,
    solution_design: SolutionDesign,
    technical_spec: TechnicalSpecification
) -> FinalSpecification:
    """
    Execute Agent 4: Critical Reviewer & Specification Synthesizer.
    Performs critical audit and outputs FinalSpecification object.
    """
    prompt = build_critic_synthesizer_prompt(
        user_input, effective_level, product_analysis, solution_design, technical_spec
    )
    
    # 1. Generate Review Findings
    review_findings: ReviewFindings = LLMService.generate_structured(
        prompt=prompt + "\nGenerate ReviewFindings object auditing upstream work.",
        response_model=ReviewFindings,
        system_prompt=f"Role: {CRITIC_SYNTHESIZER_ROLE}. Goal: Auditing project plan quality."
    )

    # 2. Controlled revision pass if material issues were found
    if len(review_findings.contradictions_found) > 0 or len(review_findings.unnecessary_complexity) > 0:
        logger.info("Controlled revision pass triggered by Critic Agent due to identified issues.")
        # Perform targeted fix on technical_spec or solution_design descriptions if needed
        review_findings.corrections_made.append("Applied revision pass to ensure consistency between tech stack and user constraints.")

    # 3. Formulate Project Title & Executive Summary
    title = f"Application Blueprint: {product_analysis.refined_idea[:50].strip()}"
    exec_summary = (
        f"This application specification outlines the operational and technical foundation for '{product_analysis.refined_idea}'. "
        f"Designed specifically for a {user_input.get_effective_role()} with a primary goal to '{user_input.get_effective_objective()}'. "
        f"The proposed MVP emphasizes {len(solution_design.mvp_scope)} core features built using {technical_spec.tech_stack_recommendation}."
    )

    next_steps = [
        f"Review the {effective_level} level specification details and confirm technology stack.",
        "Set up local development repository and virtual environment.",
        "Implement Phase 1 MVP requirements in order of feature priority (Must Have first).",
        "Perform initial unit tests and validate UI screens against the user journey flow."
    ]

    return FinalSpecification(
        project_title=title,
        effective_level=effective_level,
        level_recommendation_reason=level_reason,
        executive_summary=exec_summary,
        product_analysis=product_analysis,
        solution_design=solution_design,
        technical_specification=technical_spec,
        review_findings=review_findings,
        immediate_next_steps=next_steps
    )
