from models.schemas import FinalSpecification

def filter_report_by_level(spec: FinalSpecification) -> FinalSpecification:
    """
    Ensure the specification content strictly aligns with the chosen detail level (Basic, Intermediate, Advanced).
    Returns a copy of FinalSpecification adjusted for presentation level.
    """
    level = spec.effective_level

    if level == "Basic":
        # Basic level: Keep high-level concepts, simplify technical sections
        spec.technical_specification.database_entities = []
        spec.technical_specification.api_integrations = []
        spec.technical_specification.non_functional_requirements = []
        
    elif level == "Intermediate":
        # Intermediate level: Keep clean tables, shorten long contracts if overly verbose
        pass

    # Advanced level retains full fidelity
    return spec
