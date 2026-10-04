from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class UserInput(BaseModel):
    idea: str = Field(..., description="Application idea description provided by the user.")
    user_role: str = Field(default="Software developer", description="Role or experience level of user.")
    custom_role: Optional[str] = Field(default=None, description="Custom role if 'Other' selected.")
    main_objective: str = Field(default="Prepare a developer-ready application specification", description="Primary goal.")
    custom_objective: Optional[str] = Field(default=None, description="Custom objective if 'Other' selected.")
    spec_level: str = Field(default="Recommend for me", description="Specification detail level.")
    tech_experience: str = Field(default="Intermediate", description="Technical background level.")
    tech_stack: List[str] = Field(default_factory=list, description="Preferred technologies.")
    custom_tech_stack: Optional[str] = Field(default=None, description="Custom tech stack if specified.")
    deadline: Optional[str] = Field(default=None, description="Project timeline or deadline.")
    team_size: Optional[str] = Field(default=None, description="Team size or headcount.")
    budget: Optional[str] = Field(default=None, description="Available budget.")
    platforms: Optional[str] = Field(default=None, description="Target platforms (web, mobile, etc.).")
    integrations: Optional[str] = Field(default=None, description="Required external integrations.")
    additional_constraints: Optional[str] = Field(default=None, description="Other constraints.")
    additional_requirements: Optional[str] = Field(default=None, description="Free-text additional requirements.")
    enable_research: bool = Field(default=False, description="Enable Tavily web research.")

    @field_validator("idea")
    @classmethod
    def validate_idea(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Application idea must not be empty or whitespace-only.")
        if len(v.strip()) < 10:
            raise ValueError("Please provide a more descriptive application idea (at least 10 characters).")
        return v.strip()

    def get_effective_role(self) -> str:
        if self.user_role == "Other" and self.custom_role:
            return self.custom_role
        return self.user_role

    def get_effective_objective(self) -> str:
        if self.main_objective == "Other" and self.custom_objective:
            return self.custom_objective
        return self.main_objective

    def get_effective_tech_stack(self) -> List[str]:
        stack = list(self.tech_stack)
        if "Other" in stack and self.custom_tech_stack:
            stack.remove("Other")
            stack.append(self.custom_tech_stack)
        return stack


class ResearchItem(BaseModel):
    title: str
    url: str
    snippet: str
    relevance: str = "Medium"


class ProductAnalysis(BaseModel):
    refined_idea: str
    problem_statement: str
    target_users: List[str] = Field(default_factory=list)
    user_needs: List[str] = Field(default_factory=list)
    value_proposition: str
    key_assumptions: List[str] = Field(default_factory=list)
    open_questions: List[str] = Field(default_factory=list)
    research_findings: List[ResearchItem] = Field(default_factory=list)


class FeatureItem(BaseModel):
    name: str
    description: str
    priority: str = Field(default="Must Have", description="Must Have, Should Have, Could Have, or Future Scope")
    in_mvp: bool = True
    reasoning: str = ""


class SolutionDesign(BaseModel):
    proposed_solution: str
    features: List[FeatureItem] = Field(default_factory=list)
    mvp_scope: List[str] = Field(default_factory=list)
    out_of_scope: List[str] = Field(default_factory=list)
    user_journey: List[str] = Field(default_factory=list)
    screens_outline: List[str] = Field(default_factory=list)
    future_enhancements: List[str] = Field(default_factory=list)


class FunctionalRequirement(BaseModel):
    id: str = Field(..., description="Unique ID e.g. FR-01")
    title: str
    description: str
    priority: str = "Must Have"


class NonFunctionalRequirement(BaseModel):
    id: str = Field(..., description="Unique ID e.g. NFR-01")
    category: str = Field(..., description="Category like Security, Performance, Usability")
    description: str


class DatabaseEntity(BaseModel):
    name: str
    description: str
    attributes: List[str] = Field(default_factory=list)
    relationships: List[str] = Field(default_factory=list)


class APIContract(BaseModel):
    name: str
    method: str = "POST"
    endpoint: str
    description: str
    request_params: str = "{}"
    response_example: str = "{}"
    is_required: bool = True


class TechnicalSpecification(BaseModel):
    tech_stack_recommendation: str
    tech_stack_rationale: str
    functional_requirements: List[FunctionalRequirement] = Field(default_factory=list)
    non_functional_requirements: List[NonFunctionalRequirement] = Field(default_factory=list)
    architecture_overview: str
    database_entities: List[DatabaseEntity] = Field(default_factory=list)
    api_integrations: List[APIContract] = Field(default_factory=list)
    security_privacy_considerations: List[str] = Field(default_factory=list)
    validation_error_handling: List[str] = Field(default_factory=list)
    testing_plan: List[str] = Field(default_factory=list)
    phased_roadmap: List[str] = Field(default_factory=list)


class ReviewFindings(BaseModel):
    addresses_original_problem: bool = True
    contradictions_found: List[str] = Field(default_factory=list)
    unrealistic_constraints: List[str] = Field(default_factory=list)
    unnecessary_complexity: List[str] = Field(default_factory=list)
    missing_considerations: List[str] = Field(default_factory=list)
    corrections_made: List[str] = Field(default_factory=list)
    remaining_risks: List[str] = Field(default_factory=list)


class FinalSpecification(BaseModel):
    project_title: str
    effective_level: str = "Intermediate"  # Basic, Intermediate, Advanced
    level_recommendation_reason: Optional[str] = None
    executive_summary: str
    product_analysis: ProductAnalysis
    solution_design: SolutionDesign
    technical_specification: TechnicalSpecification
    review_findings: ReviewFindings
    immediate_next_steps: List[str] = Field(default_factory=list)
