from models.schemas import UserInput, ProductAnalysis, SolutionDesign, TechnicalSpecification

# Agent 1 Definitions
PRODUCT_ANALYST_ROLE = "Product & Problem Analyst"
PRODUCT_ANALYST_GOAL = "Analyze raw application ideas, define core problem statements, target users, needs, value proposition, assumptions, and open questions."
PRODUCT_ANALYST_BACKSTORY = (
    "You are a seasoned Product Manager and User Experience Researcher. "
    "Your expertise lies in cutting through vague ideas to expose the true root problem, "
    "identifying key user personas, and setting realistic boundaries while acknowledging key assumptions."
)

# Agent 2 Definitions
SOLUTION_DESIGNER_ROLE = "Solution & Product Designer"
SOLUTION_DESIGNER_GOAL = "Transform analyzed problems into coherent proposed solutions with prioritized feature lists, MVP boundaries, user journeys, and screens."
SOLUTION_DESIGNER_BACKSTORY = (
    "You are a pragmatic Lead Product Designer and System Strategist. "
    "You excel at structuring feature sets into clear MoSCoW priorities, scoping realistic MVPs, "
    "and designing intuitive user journeys without scope creep."
)

# Agent 3 Definitions
TECHNICAL_ARCHITECT_ROLE = "Technical Architect & Requirements Engineer"
TECHNICAL_ARCHITECT_GOAL = "Convert solution designs into software requirements, architecture, database schemas, API contracts, and phased roadmaps."
TECHNICAL_ARCHITECT_BACKSTORY = (
    "You are a Principal Software Architect and Systems Engineer. "
    "You translate product features into functional (FR-xx) and non-functional (NFR-xx) requirements, "
    "recommend modern tech stacks, define clean database schemas and API endpoints, and plan secure, scalable architectures."
)

# Agent 4 Definitions
CRITIC_SYNTHESIZER_ROLE = "Critical Reviewer & Specification Synthesizer"
CRITIC_SYNTHESIZER_GOAL = "Audit complete plans for inconsistencies, scope creep, unrealistic constraints, missing considerations, and produce the final consolidated specification."
CRITIC_SYNTHESIZER_BACKSTORY = (
    "You are a strict Chief Technology Officer and Quality Auditor. "
    "You review project proposals with extreme rigor, looking for contradictions between database design, APIs, "
    "and user requirements. You eliminate unnecessary complexity and produce flawless project specifications."
)


def build_product_analyst_prompt(user_input: UserInput, research_summary: str) -> str:
    return f"""Analyze the following raw application idea and context:

USER IDEA:
{user_input.idea}

USER CONTEXT:
- User Role / Background: {user_input.get_effective_role()}
- Main Objective: {user_input.get_effective_objective()}
- Specification Level Requested: {user_input.spec_level}
- Technical Experience: {user_input.tech_experience}
- Preferred Tech Stack: {', '.join(user_input.get_effective_tech_stack()) or 'No preference'}
- Constraints: Timeline: {user_input.deadline or 'None'}, Team: {user_input.team_size or 'None'}, Budget: {user_input.budget or 'None'}
- Target Platforms: {user_input.platforms or 'None'}
- Integrations Requested: {user_input.integrations or 'None'}
- Additional Requirements: {user_input.additional_requirements or 'None'}

EXTERNAL RESEARCH STATUS:
{research_summary}

CRITICAL: Respond ONLY with valid JSON using EXACTLY these snake_case key names:
{{
  "refined_idea": "Clean, structured summary of the app idea",
  "problem_statement": "Specific problem statement being solved",
  "target_users": ["Persona 1", "Persona 2"],
  "user_needs": ["Need 1", "Need 2"],
  "value_proposition": "Core value proposition statement",
  "key_assumptions": ["Assumption 1", "Assumption 2"],
  "open_questions": ["Question 1", "Question 2"]
}}
"""


def build_solution_designer_prompt(user_input: UserInput, product_analysis: ProductAnalysis) -> str:
    return f"""Design a solution tailored to this specific application:

APP IDEA / REFINED CONCEPT: {product_analysis.refined_idea}
PROBLEM STATEMENT: {product_analysis.problem_statement}
TARGET USERS: {', '.join(product_analysis.target_users)}
VALUE PROPOSITION: {product_analysis.value_proposition}

USER CONSTRAINTS & PREFERENCES:
- Objective: {user_input.get_effective_objective()}
- Preferred Stack: {', '.join(user_input.get_effective_tech_stack()) or 'None'}
- Timeline & Team: {user_input.deadline or 'Flexible'} / {user_input.team_size or 'Flexible'}

CRITICAL: Generate features SPECIFIC TO THIS IDEA (e.g. if email generator, include drafting, templates, SMTP; if ride sharing, include GPS, driver matching, payments).

Respond ONLY with valid JSON using EXACTLY these snake_case key names:
{{
  "proposed_solution": "Detailed solution concept specific to this app idea",
  "features": [
    {{
      "name": "Feature Name",
      "description": "Specific feature description",
      "priority": "Must Have",
      "in_mvp": true,
      "reasoning": "Why this is critical"
    }}
  ],
  "mvp_scope": ["Feature 1", "Feature 2"],
  "out_of_scope": ["Post-MVP Feature 1"],
  "user_journey": ["Step 1...", "Step 2..."],
  "screens_outline": ["Screen 1...", "Screen 2..."],
  "future_enhancements": ["Enhancement 1..."]
}}
"""


def build_technical_architect_prompt(
    user_input: UserInput,
    product_analysis: ProductAnalysis,
    solution_design: SolutionDesign
) -> str:
    return f"""Create a Technical Specification tailored to this specific application:

APP IDEA: {product_analysis.refined_idea}
PROBLEM: {product_analysis.problem_statement}
PROPOSED SOLUTION: {solution_design.proposed_solution}
MVP SCOPE: {', '.join(solution_design.mvp_scope)}
PREFERRED TECH STACK: {', '.join(user_input.get_effective_tech_stack()) or 'No preference'}
TARGET PLATFORMS: {user_input.platforms or 'Web / Flexible'}
REQUESTED INTEGRATIONS: {user_input.integrations or 'None'}

CRITICAL: Generate technical requirements, database entities, and API contracts SPECIFIC TO THIS APPLICATION IDEA.

Respond ONLY with valid JSON using EXACTLY these snake_case key names:
{{
  "tech_stack_recommendation": "Specific technologies for frontend, backend, DB, APIs",
  "tech_stack_rationale": "Clear rationale for stack choices",
  "functional_requirements": [
    {{
      "id": "FR-01",
      "title": "Requirement Title",
      "description": "Detailed requirement description",
      "priority": "Must Have"
    }}
  ],
  "non_functional_requirements": [
    {{
      "id": "NFR-01",
      "category": "Performance",
      "description": "Requirement description"
    }}
  ],
  "architecture_overview": "Specific architecture overview",
  "database_entities": [
    {{
      "name": "EntityName",
      "description": "Entity description",
      "attributes": ["id", "attribute1"],
      "relationships": ["Has many..."]
    }}
  ],
  "api_integrations": [
    {{
      "name": "Endpoint Name",
      "method": "POST",
      "endpoint": "/api/v1/resource",
      "description": "What endpoint does",
      "request_params": "{{\\"key\\": \\"value\\"}}",
      "response_example": "{{\\"status\\": \\"success\\"}}",
      "is_required": true
    }}
  ],
  "security_privacy_considerations": ["Consideration 1..."],
  "validation_error_handling": ["Rule 1..."],
  "testing_plan": ["Testing step 1..."],
  "phased_roadmap": ["Phase 1: Setup", "Phase 2: Build Core", "Phase 3: Launch"]
}}
"""


def build_critic_synthesizer_prompt(
    user_input: UserInput,
    effective_level: str,
    product_analysis: ProductAnalysis,
    solution_design: SolutionDesign,
    technical_spec: TechnicalSpecification
) -> str:
    return f"""Review, audit, and synthesize the complete application specification into a coherent report:

TARGET SPECIFICATION DETAIL LEVEL: {effective_level}
USER OBJECTIVE: {user_input.get_effective_objective()}
APP TITLE: {product_analysis.refined_idea}

UPSTREAM OUTPUTS TO AUDIT:
1. Product Analysis: Problem: {product_analysis.problem_statement}
2. Solution Design: Proposed Solution: {solution_design.proposed_solution}
3. Technical Spec: Tech Stack: {technical_spec.tech_stack_recommendation}

Respond ONLY with valid JSON using EXACTLY these snake_case key names:
{{
  "addresses_original_problem": true,
  "contradictions_found": [],
  "unrealistic_constraints": [],
  "unnecessary_complexity": [],
  "missing_considerations": ["Consideration 1..."],
  "corrections_made": ["Aligned requirements..."],
  "remaining_risks": ["Risk 1..."]
}}
"""
