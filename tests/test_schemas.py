import pytest
from models.schemas import (
    UserInput,
    ProductAnalysis,
    SolutionDesign,
    TechnicalSpecification,
    ReviewFindings,
    FinalSpecification,
    FeatureItem,
    FunctionalRequirement,
    NonFunctionalRequirement,
)

def test_user_input_custom_fields():
    inp = UserInput(
        idea="A custom agricultural disease identification app.",
        user_role="Other",
        custom_role="Agricultural Researcher",
        main_objective="Other",
        custom_objective="Field deployment analysis",
        tech_stack=["Python", "Other"],
        custom_tech_stack="PyTorch"
    )
    assert inp.get_effective_role() == "Agricultural Researcher"
    assert inp.get_effective_objective() == "Field deployment analysis"
    assert "PyTorch" in inp.get_effective_tech_stack()

def test_final_specification_schema():
    pa = ProductAnalysis(
        refined_idea="Agricultural plant disease diagnostic tool.",
        problem_statement="Farmers suffer crop yield losses due to delayed disease identification.",
        target_users=["Farmers", "Agronomists"],
        user_needs=["Rapid diagnosis from photos", "Treatment advice"],
        value_proposition="Real-time AI plant disease detection.",
        key_assumptions=["Farmers have mobile smartphones with cameras."],
        open_questions=[]
    )

    sd = SolutionDesign(
        proposed_solution="Mobile application analyzing leaf photos via computer vision.",
        features=[
            FeatureItem(name="Photo Capture & Upload", description="Capture leaf images", priority="Must Have", in_mvp=True)
        ],
        mvp_scope=["Photo Capture & Upload"],
        out_of_scope=["Drones automation"],
        user_journey=["Take photo", "View diagnosis result"],
        screens_outline=["Camera Screen", "Diagnosis Result Screen"]
    )

    ts = TechnicalSpecification(
        tech_stack_recommendation="Flutter, FastAPI, PyTorch",
        tech_stack_rationale="Flutter supports cross-platform mobile UI; FastAPI offers lightweight ML model serving.",
        functional_requirements=[
            FunctionalRequirement(id="FR-01", title="Image Upload", description="User can upload image.", priority="Must Have")
        ],
        non_functional_requirements=[
            NonFunctionalRequirement(id="NFR-01", category="Performance", description="Inference result within 2 seconds.")
        ],
        architecture_overview="Mobile client -> REST API backend -> ML inference engine.",
        database_entities=[],
        api_integrations=[]
    )

    rf = ReviewFindings(addresses_original_problem=True)

    spec = FinalSpecification(
        project_title="AgriShield AI",
        effective_level="Intermediate",
        executive_summary="Mobile plant disease diagnosis platform.",
        product_analysis=pa,
        solution_design=sd,
        technical_specification=ts,
        review_findings=rf,
        immediate_next_steps=["Setup Flutter app"]
    )

    json_data = spec.model_dump_json()
    assert "AgriShield AI" in json_data
    assert "FR-01" in json_data
