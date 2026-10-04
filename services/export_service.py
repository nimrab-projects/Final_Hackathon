import json
from models.schemas import FinalSpecification

class ExportService:
    @staticmethod
    def to_json(spec: FinalSpecification) -> str:
        """Convert FinalSpecification object to clean JSON string."""
        return spec.model_dump_json(indent=2)

    @staticmethod
    def to_markdown(spec: FinalSpecification) -> str:
        """Convert FinalSpecification object to a formatted Markdown report."""
        pa = spec.product_analysis
        sd = spec.solution_design
        ts = spec.technical_specification
        rf = spec.review_findings

        md = []
        md.append(f"# 🚀 {spec.project_title}")
        md.append(f"**Specification Detail Level:** `{spec.effective_level}`  ")
        if spec.level_recommendation_reason:
            md.append(f"*> Note on level:* {spec.level_recommendation_reason}  ")
        md.append("\n---\n")

        # Executive Summary
        md.append("## 📋 Executive Summary")
        md.append(spec.executive_summary)
        md.append("\n")

        # Product & Problem Analysis
        md.append("## 💡 1. Product & Problem Analysis")
        md.append(f"### Refined Idea\n{pa.refined_idea}\n")
        md.append(f"### Problem Statement\n{pa.problem_statement}\n")
        md.append(f"### Value Proposition\n{pa.value_proposition}\n")

        if pa.target_users:
            md.append("### Target Users")
            for user in pa.target_users:
                md.append(f"- {user}")
            md.append("\n")

        if pa.user_needs:
            md.append("### User Needs & Pain Points")
            for need in pa.user_needs:
                md.append(f"- {need}")
            md.append("\n")

        if pa.key_assumptions:
            md.append("### Key Assumptions")
            for asm in pa.key_assumptions:
                md.append(f"- {asm}")
            md.append("\n")

        if pa.open_questions:
            md.append("### Open Questions")
            for q in pa.open_questions:
                md.append(f"- ❓ {q}")
            md.append("\n")

        if pa.research_findings:
            md.append("### External Research Findings & Sources")
            for res in pa.research_findings:
                md.append(f"- **[{res.title}]({res.url})**: {res.snippet}")
            md.append("\n")

        # Proposed Solution & Design
        md.append("## 🎨 2. Solution & Product Design")
        md.append(f"### Proposed Solution\n{sd.proposed_solution}\n")

        if sd.features:
            md.append("### Feature Breakdown & Priorities")
            md.append("| Feature | Description | Priority | In MVP? |")
            md.append("| --- | --- | --- | --- |")
            for feat in sd.features:
                mvp_str = "✅ Yes" if feat.in_mvp else "❌ No"
                md.append(f"| **{feat.name}** | {feat.description} | `{feat.priority}` | {mvp_str} |")
            md.append("\n")

        if sd.mvp_scope:
            md.append("### Minimum Viable Product (MVP) Scope")
            for item in sd.mvp_scope:
                md.append(f"- ✅ {item}")
            md.append("\n")

        if sd.out_of_scope:
            md.append("### Out of Scope (Initial Phase)")
            for item in sd.out_of_scope:
                md.append(f"- 🚫 {item}")
            md.append("\n")

        if sd.user_journey:
            md.append("### Main User Journey")
            for idx, step in enumerate(sd.user_journey, 1):
                md.append(f"{idx}. {step}")
            md.append("\n")

        if sd.screens_outline:
            md.append("### Key UI Screens / Pages")
            for screen in sd.screens_outline:
                md.append(f"- 🖥️ {screen}")
            md.append("\n")

        if sd.future_enhancements:
            md.append("### Future Enhancements")
            for enh in sd.future_enhancements:
                md.append(f"- 🔮 {enh}")
            md.append("\n")

        # Technical Architecture & Requirements
        md.append("## 🛠️ 3. Technical Architecture & Requirements")
        md.append(f"### Recommended Technology Stack\n`{ts.tech_stack_recommendation}`\n")
        md.append(f"**Rationale:** {ts.tech_stack_rationale}\n")
        md.append(f"### System Architecture Overview\n{ts.architecture_overview}\n")

        if ts.functional_requirements:
            md.append("### Functional Requirements")
            md.append("| ID | Title | Description | Priority |")
            md.append("| --- | --- | --- | --- |")
            for fr in ts.functional_requirements:
                md.append(f"| `{fr.id}` | **{fr.title}** | {fr.description} | `{fr.priority}` |")
            md.append("\n")

        if ts.non_functional_requirements:
            md.append("### Non-Functional Requirements")
            md.append("| ID | Category | Description |")
            md.append("| --- | --- | --- |")
            for nfr in ts.non_functional_requirements:
                md.append(f"| `{nfr.id}` | {nfr.category} | {nfr.description} |")
            md.append("\n")

        if ts.database_entities:
            md.append("### Database Entities & Data Design")
            for db in ts.database_entities:
                md.append(f"#### Entity: `{db.name}`")
                md.append(f"{db.description}")
                if db.attributes:
                    md.append(f"- **Attributes:** {', '.join(db.attributes)}")
                if db.relationships:
                    md.append(f"- **Relationships:** {', '.join(db.relationships)}")
                md.append("")

        if ts.api_integrations:
            md.append("### External APIs & API Contracts")
            for api in ts.api_integrations:
                req_str = "Required" if api.is_required else "Optional"
                md.append(f"#### `{api.method}` `{api.endpoint}` ({api.name}) [{req_str}]")
                md.append(f"{api.description}")
                md.append(f"```json\n// Request Params\n{api.request_params}\n\n// Response Example\n{api.response_example}\n```\n")

        if ts.security_privacy_considerations:
            md.append("### Security & Privacy Considerations")
            for sec in ts.security_privacy_considerations:
                md.append(f"- 🔒 {sec}")
            md.append("\n")

        if ts.validation_error_handling:
            md.append("### Input Validation & Error Recovery")
            for err in ts.validation_error_handling:
                md.append(f"- ⚠️ {err}")
            md.append("\n")

        if ts.testing_plan:
            md.append("### Testing Strategy")
            for test in ts.testing_plan:
                md.append(f"- 🧪 {test}")
            md.append("\n")

        if ts.phased_roadmap:
            md.append("### Phased Implementation Roadmap")
            for phase in ts.phased_roadmap:
                md.append(f"- 📅 {phase}")
            md.append("\n")

        # Critical Review & Audit
        md.append("## 🔍 4. Critical Audit & Review Findings")
        status_icon = "✅ Passed" if rf.addresses_original_problem else "⚠️ Attention Required"
        md.append(f"**Addresses Original Problem:** {status_icon}\n")

        if rf.corrections_made:
            md.append("### Synthesizer Corrections Applied")
            for corr in rf.corrections_made:
                md.append(f"- 🛠️ {corr}")
            md.append("\n")

        if rf.remaining_risks:
            md.append("### Remaining Technical & Business Risks")
            for risk in rf.remaining_risks:
                md.append(f"- ⚡ {risk}")
            md.append("\n")

        # Immediate Next Steps
        if spec.immediate_next_steps:
            md.append("## 🎯 Immediate Next Steps")
            for step in spec.immediate_next_steps:
                md.append(f"1. {step}")
            md.append("\n")

        return "\n".join(md)
