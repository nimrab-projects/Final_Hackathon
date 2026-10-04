from models.schemas import UserInput
from workflows.specification_workflow import SpecificationWorkflow

def test_workflow_execution_mock():
    # Set up user input
    user_input = UserInput(
        idea="A smart study group matching platform for university students based on course schedules.",
        user_role="Student / university project team",
        main_objective="Prepare a hackathon MVP plan",
        spec_level="Recommend for me",
        tech_experience="Intermediate",
        tech_stack=["Python", "FastAPI", "React"],
        enable_research=False
    )

    progress_stages = []
    def progress_cb(stage, total, message):
        progress_stages.append((stage, total, message))

    workflow = SpecificationWorkflow(progress_callback=progress_cb)
    final_spec = workflow.execute(user_input)

    assert final_spec is not None
    assert final_spec.project_title != ""
    assert final_spec.effective_level in ["Basic", "Intermediate", "Advanced"]
    assert len(progress_stages) == 5
    assert progress_stages[0][0] == 1
    assert progress_stages[-1][0] == 5
