import logging
from typing import Callable, Optional
from models.schemas import UserInput, FinalSpecification
from utils.validation import validate_user_input, recommend_specification_level
from utils.report_formatter import filter_report_by_level
from services.research_service import ResearchService
from agents.product_analyst import run_product_analyst
from agents.solution_designer import run_solution_designer
from agents.technical_architect import run_technical_architect
from agents.critic_synthesizer import run_critic_synthesizer

logger = logging.getLogger(__name__)

class SpecificationWorkflow:
    def __init__(self, progress_callback: Optional[Callable[[int, int, str], None]] = None):
        self.progress_callback = progress_callback

    def _update_progress(self, stage: int, total: int, message: str):
        if self.progress_callback:
            self.progress_callback(stage, total, message)
        logger.info(f"[Stage {stage}/{total}] {message}")

    def execute(self, user_input: UserInput) -> FinalSpecification:
        """
        Execute the complete multi-agent workflow sequentially.
        """
        total_stages = 5

        # Determine effective detail level
        if user_input.spec_level == "Recommend for me":
            effective_level, level_reason = recommend_specification_level(user_input)
        else:
            effective_level = user_input.spec_level
            level_reason = f"User explicitly selected {effective_level} specification level."

        # Stage 1: Optional Web Research
        self._update_progress(1, total_stages, "Performing web research & source collection...")
        research_items, research_summary = ResearchService.perform_research(
            idea_summary=user_input.idea,
            enable_research=user_input.enable_research
        )

        # Stage 2: Agent 1 - Product & Problem Analyst
        self._update_progress(2, total_stages, "Agent 1: Analyzing problem, target users & value proposition...")
        product_analysis = run_product_analyst(user_input, research_items, research_summary)

        # Stage 3: Agent 2 - Solution & Product Designer
        self._update_progress(3, total_stages, "Agent 2: Designing solution, MoSCoW feature breakdown & MVP scope...")
        solution_design = run_solution_designer(user_input, product_analysis)

        # Stage 4: Agent 3 - Technical Architect & Requirements Engineer
        self._update_progress(4, total_stages, "Agent 3: Engineering software requirements, tech stack & architecture...")
        technical_spec = run_technical_architect(user_input, product_analysis, solution_design)

        # Stage 5: Agent 4 - Critical Reviewer & Synthesizer
        self._update_progress(5, total_stages, "Agent 4: Auditing specification consistency & synthesizing final report...")
        raw_final_spec = run_critic_synthesizer(
            user_input=user_input,
            effective_level=effective_level,
            level_reason=level_reason,
            product_analysis=product_analysis,
            solution_design=solution_design,
            technical_spec=technical_spec
        )

        # Apply level-specific formatting filters
        final_spec = filter_report_by_level(raw_final_spec)
        return final_spec
