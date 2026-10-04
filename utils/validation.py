from typing import Tuple, List, Optional
from pydantic import ValidationError
from models.schemas import UserInput

def validate_user_input(raw_data: dict) -> Tuple[bool, Optional[UserInput], List[str]]:
    """
    Validate raw input dictionary against UserInput schema.
    Returns (is_valid, UserInput_model, error_messages).
    """
    errors: List[str] = []
    
    # Check idea manually for quick clear error message
    idea = str(raw_data.get("idea", "")).strip()
    if not idea:
        errors.append("Application idea description is required and cannot be empty or whitespace.")
    elif len(idea) < 10:
        errors.append("Please provide a more descriptive application idea (at least 10 characters).")

    if errors:
        return False, None, errors

    try:
        user_input = UserInput(**raw_data)
        return True, user_input, []
    except ValidationError as ve:
        for err in ve.errors():
            field = err.get("loc", ["field"])[0]
            msg = err.get("msg", "Invalid value")
            errors.append(f"{field}: {msg}")
        return False, None, errors


def recommend_specification_level(user_input: UserInput) -> Tuple[str, str]:
    """
    Infer suitable specification detail level based on user role, objective, experience, and constraints.
    Returns (recommended_level, explanation_reason).
    """
    role = user_input.get_effective_role().lower()
    obj = user_input.get_effective_objective().lower()
    exp = user_input.tech_experience.lower()

    # Rule 1: Advanced level criteria
    if "developer" in role or "production" in obj or "advanced" in exp or "developer-ready" in obj:
        return (
            "Advanced",
            "Selected Advanced level because your profile indicates developer-ready / production planning with technical experience."
        )

    # Rule 2: Basic level criteria
    if "beginner" in role or "understand and refine" in obj or "no coding" in exp:
        return (
            "Basic",
            "Recommended Basic level to focus on conceptual clarity, core problem definition, and simple feature roadmaps without technical overload."
        )

    # Rule 3: Default to Intermediate
    return (
        "Intermediate",
        "Recommended Intermediate level for student/hackathon prototype planning, offering clear requirement tables and architecture outlines."
    )
