import pytest
from utils.validation import validate_user_input, recommend_specification_level
from models.schemas import UserInput

def test_validate_user_input_empty():
    is_valid, user_input, errors = validate_user_input({"idea": "   "})
    assert not is_valid
    assert user_input is None
    assert any("empty or whitespace" in e for e in errors)

def test_validate_user_input_too_short():
    is_valid, user_input, errors = validate_user_input({"idea": "short"})
    assert not is_valid
    assert user_input is None
    assert any("at least 10 characters" in e for e in errors)

def test_validate_user_input_success():
    raw = {
        "idea": "An intelligent university food waste reduction platform matching surplus food with student organizations.",
        "user_role": "Student / university project team",
        "main_objective": "Prepare a hackathon MVP plan",
        "spec_level": "Intermediate",
        "tech_experience": "Intermediate",
        "tech_stack": ["Python", "Streamlit"],
        "deadline": "2 weeks"
    }
    is_valid, user_input, errors = validate_user_input(raw)
    assert is_valid
    assert errors == []
    assert user_input is not None
    assert user_input.idea.startswith("An intelligent university")
    assert user_input.get_effective_role() == "Student / university project team"

def test_recommend_specification_level():
    u_basic = UserInput(
        idea="A simple reminder app for academic tasks.",
        user_role="Beginner / non-technical user",
        main_objective="Understand and refine my idea",
        tech_experience="No coding experience"
    )
    rec_level, reason = recommend_specification_level(u_basic)
    assert rec_level == "Basic"
    assert "Basic level" in reason

    u_adv = UserInput(
        idea="A microservices-based real-time logistics dashboard.",
        user_role="Software developer",
        main_objective="Prepare a production-oriented technical plan",
        tech_experience="Advanced"
    )
    rec_level_adv, reason_adv = recommend_specification_level(u_adv)
    assert rec_level_adv == "Advanced"
    assert "Advanced level" in reason_adv
