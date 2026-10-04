import os
import json
import streamlit as st

# Configure Streamlit page layout
st.set_page_config(
    page_title="IdeaForge AI — Multi-Agent Application Architect",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# IdeaForge AI Vector Logo SVG definitions
LOGO_SVG_SIDEBAR = """<svg width="38" height="38" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; flex-shrink:0;">
  <defs>
    <linearGradient id="logo-grad-sb" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#818cf8"/>
      <stop offset="50%" stop-color="#c084fc"/>
      <stop offset="100%" stop-color="#f472b6"/>
    </linearGradient>
  </defs>
  <path d="M24 4L41.3205 14V34L24 44L6.67949 34V14L24 4Z" stroke="url(#logo-grad-sb)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="rgba(99, 102, 241, 0.12)"/>
  <path d="M24 12V20M24 28V36M14 18L20 22M28 26L34 30M34 18L28 22M20 26L14 30" stroke="url(#logo-grad-sb)" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="24" cy="24" r="4.5" fill="url(#logo-grad-sb)"/>
  <circle cx="14" cy="18" r="2.5" fill="#818cf8"/>
  <circle cx="34" cy="18" r="2.5" fill="#c084fc"/>
  <circle cx="14" cy="30" r="2.5" fill="#c084fc"/>
  <circle cx="34" cy="30" r="2.5" fill="#f472b6"/>
  <circle cx="24" cy="12" r="2.5" fill="#818cf8"/>
  <circle cx="24" cy="36" r="2.5" fill="#f472b6"/>
</svg>"""

LOGO_SVG_HERO = """<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; flex-shrink:0;">
  <defs>
    <linearGradient id="logo-grad-hero" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#818cf8"/>
      <stop offset="50%" stop-color="#c084fc"/>
      <stop offset="100%" stop-color="#f472b6"/>
    </linearGradient>
  </defs>
  <path d="M24 4L41.3205 14V34L24 44L6.67949 34V14L24 4Z" stroke="url(#logo-grad-hero)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="rgba(99, 102, 241, 0.15)"/>
  <path d="M24 12V20M24 28V36M14 18L20 22M28 26L34 30M34 18L28 22M20 26L14 30" stroke="url(#logo-grad-hero)" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="24" cy="24" r="4.5" fill="url(#logo-grad-hero)"/>
  <circle cx="14" cy="18" r="2.5" fill="#818cf8"/>
  <circle cx="34" cy="18" r="2.5" fill="#c084fc"/>
  <circle cx="14" cy="30" r="2.5" fill="#c084fc"/>
  <circle cx="34" cy="30" r="2.5" fill="#f472b6"/>
  <circle cx="24" cy="12" r="2.5" fill="#818cf8"/>
  <circle cx="24" cy="36" r="2.5" fill="#f472b6"/>
</svg>"""

# Custom CSS styling with theme-aware variables for Light and Dark modes
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* System Theme Variable Tokens (Default Dark Theme) */
    :root {
        --bg-app: #090d16;
        --bg-glow-1: rgba(99, 102, 241, 0.12);
        --bg-glow-2: rgba(168, 85, 247, 0.10);
        --bg-glow-3: rgba(15, 23, 42, 0.5);
        
        --card-bg: rgba(15, 23, 42, 0.75);
        --card-border: rgba(255, 255, 255, 0.08);
        --card-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        
        --subcard-bg: rgba(30, 41, 59, 0.45);
        --subcard-border: rgba(148, 163, 184, 0.15);
        --subcard-hover-bg: rgba(30, 41, 59, 0.7);
        --subcard-hover-border: rgba(99, 102, 241, 0.4);
        
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --accent-indigo: #818cf8;
        --accent-purple: #c084fc;
        --accent-pink: #f472b6;
        
        --title-gradient: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
        --tab-selected-bg: rgba(99, 102, 241, 0.15);
        --tab-selected-border: rgba(99, 102, 241, 0.3);
    }

    /* Light Theme Overrides (System preference or Streamlit light mode) */
    @media (prefers-color-scheme: light) {
        :root {
            --bg-app: #f8fafc;
            --bg-glow-1: rgba(99, 102, 241, 0.08);
            --bg-glow-2: rgba(168, 85, 247, 0.06);
            --bg-glow-3: rgba(241, 245, 249, 0.6);
            
            --card-bg: #ffffff;
            --card-border: rgba(99, 102, 241, 0.2);
            --card-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.08);
            
            --subcard-bg: #f1f5f9;
            --subcard-border: rgba(203, 213, 225, 0.8);
            --subcard-hover-bg: #e2e8f0;
            --subcard-hover-border: rgba(79, 70, 229, 0.5);
            
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --text-muted: #64748b;
            --accent-indigo: #4f46e5;
            --accent-purple: #7c3aed;
            --accent-pink: #db2777;
            
            --title-gradient: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #db2777 100%);
            --tab-selected-bg: rgba(79, 70, 229, 0.1);
            --tab-selected-border: rgba(79, 70, 229, 0.4);
        }
    }

    [data-theme="light"] {
        --bg-app: #f8fafc;
        --bg-glow-1: rgba(99, 102, 241, 0.08);
        --bg-glow-2: rgba(168, 85, 247, 0.06);
        --bg-glow-3: rgba(241, 245, 249, 0.6);
        
        --card-bg: #ffffff;
        --card-border: rgba(99, 102, 241, 0.2);
        --card-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.08);
        
        --subcard-bg: #f1f5f9;
        --subcard-border: rgba(203, 213, 225, 0.8);
        --subcard-hover-bg: #e2e8f0;
        --subcard-hover-border: rgba(79, 70, 229, 0.5);
        
        --text-primary: #0f172a;
        --text-secondary: #475569;
        --text-muted: #64748b;
        --accent-indigo: #4f46e5;
        --accent-purple: #7c3aed;
        --accent-pink: #db2777;
        
        --title-gradient: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #db2777 100%);
        --tab-selected-bg: rgba(79, 70, 229, 0.1);
        --tab-selected-border: rgba(79, 70, 229, 0.4);
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main App Container Background */
    .stApp {
        background-color: var(--bg-app);
        background-image: 
            radial-gradient(at 0% 0%, var(--bg-glow-1) 0px, transparent 50%),
            radial-gradient(at 100% 100%, var(--bg-glow-2) 0px, transparent 50%),
            radial-gradient(at 50% 50%, var(--bg-glow-3) 0px, transparent 100%);
        color: var(--text-primary);
    }
    
    /* Executive Hero Header Card */
    .hero-card {
        background: var(--card-bg);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 2.25rem 2.5rem;
        margin-bottom: 2rem;
        box-shadow: var(--card-shadow);
    }
    .hero-header-flex {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 0.5rem;
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        background: var(--title-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: var(--text-secondary);
        max-width: 850px;
        line-height: 1.6;
        font-weight: 400;
    }
    
    /* Agent Pipeline Grid Cards */
    .agent-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1rem;
        margin-top: 1.5rem;
    }
    .agent-card {
        background: var(--subcard-bg);
        border: 1px solid var(--subcard-border);
        border-radius: 12px;
        padding: 1.1rem;
        transition: all 0.2s ease-in-out;
    }
    .agent-card:hover {
        border-color: var(--subcard-hover-border);
        background: var(--subcard-hover-bg);
        transform: translateY(-2px);
    }
    .agent-step {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--accent-indigo);
        margin-bottom: 0.2rem;
    }
    .agent-name {
        font-weight: 700;
        color: var(--text-primary);
        font-size: 0.95rem;
        margin-bottom: 0.3rem;
    }
    .agent-desc {
        font-size: 0.82rem;
        color: var(--text-secondary);
        line-height: 1.4;
    }
    
    /* MoSCoW Priority Pill Badges */
    .badge-must {
        background: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    .badge-should {
        background: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.3);
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    .badge-could {
        background: rgba(59, 130, 246, 0.15);
        color: #3b82f6;
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    .badge-future {
        background: rgba(107, 114, 128, 0.15);
        color: var(--text-secondary);
        border: 1px solid rgba(107, 114, 128, 0.3);
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    .badge-mvp {
        background: rgba(16, 185, 129, 0.15);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
    }

    /* Section & Feature Display Cards */
    .section-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
    }
    .feature-card {
        background: var(--subcard-bg);
        border: 1px solid var(--subcard-border);
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
    }
    
    /* Code block styling */
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Dynamic theme-aware Subheaders */
    h1, h2, h3, h4 {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
    }
    
    /* Streamlit Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid var(--card-border);
        padding-bottom: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        background-color: transparent;
        border-radius: 8px;
        color: var(--text-secondary);
        font-weight: 600;
        font-size: 0.9rem;
        padding: 0px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--tab-selected-bg) !important;
        color: var(--accent-indigo) !important;
        border: 1px solid var(--tab-selected-border) !important;
    }
</style>
""", unsafe_allow_html=True)

# Imports after page config
from models.schemas import UserInput, FinalSpecification
from utils.validation import validate_user_input, recommend_specification_level
from services.export_service import ExportService
from workflows.specification_workflow import SpecificationWorkflow

# Initialize session state variables
if "generated_spec" not in st.session_state:
    st.session_state.generated_spec = None
if "workflow_in_progress" not in st.session_state:
    st.session_state.workflow_in_progress = False

# Sidebar Configuration
with st.sidebar:
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:4px;">
            {LOGO_SVG_SIDEBAR}
            <div>
                <h3 style="margin:0; padding:0; font-size:1.3rem; font-weight:800; color:var(--text-primary) !important;">IdeaForge AI</h3>
                <span style="font-size:0.8rem; color:var(--text-secondary);">Multi-Agent Engine</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.divider()
    st.markdown(
        "IdeaForge AI transforms raw application concepts into structured, developer-ready software specifications and architecture blueprints using collaborative AI agents."
    )
    st.divider()
    st.caption("IdeaForge AI • Production Specification System")

# Main Application Layout Header Card
st.markdown(f"""
<div class="hero-card">
    <div class="hero-header-flex">
        {LOGO_SVG_HERO}
        <div class="hero-title">IdeaForge AI</div>
    </div>
    <div class="hero-subtitle">
        Transform raw application visions into structured, personalized, and technically actionable engineering blueprints through collaborative multi-agent AI reasoning.
    </div>
    <div class="agent-grid">
        <div class="agent-card">
            <div class="agent-step">Stage 1</div>
            <div class="agent-name">Product Analyst</div>
            <div class="agent-desc">Extracts root problem statements, personas & core value proposition.</div>
        </div>
        <div class="agent-card">
            <div class="agent-step">Stage 2</div>
            <div class="agent-name">Solution Designer</div>
            <div class="agent-desc">Prioritizes MoSCoW features, outlines MVP scope & user journey.</div>
        </div>
        <div class="agent-card">
            <div class="agent-step">Stage 3</div>
            <div class="agent-name">Tech Architect</div>
            <div class="agent-desc">Defines tech stack, FR/NFR requirements, database & API contracts.</div>
        </div>
        <div class="agent-card">
            <div class="agent-step">Stage 4</div>
            <div class="agent-name">Critical Reviewer</div>
            <div class="agent-desc">Audits scope creep, eliminates contradictions & synthesizes report.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# View Toggle: Show Input Form or Show Specification Dashboard
if st.session_state.generated_spec is None:
    st.markdown("<h2 style='font-size:1.5rem; margin-bottom:0.5rem;'>Application Blueprint Generator</h2>", unsafe_allow_html=True)
    st.markdown("Provide your application vision and constraints below. The multi-agent pipeline will analyze and engineer your specification.")
    
    with st.form(key="idea_form"):
        # Section 1: Application Concept
        st.markdown("<h4 style='color:var(--accent-indigo) !important;'>1. Project Concept & Vision (Required)</h4>", unsafe_allow_html=True)
        idea_input = st.text_area(
            label="Describe your application idea, the problem it addresses, and target goals.",
            placeholder="e.g. An AI platform that matches university students with study partners based on course schedules, learning styles, and assignment deadlines...",
            height=130,
            help="Provide clear context for the AI agents to synthesize accurate requirements."
        )

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h4 style='color:var(--accent-indigo) !important;'>2. User Profile & Goal</h4>", unsafe_allow_html=True)
            user_role = st.selectbox(
                "Your Experience Level / Role",
                options=[
                    "Software developer",
                    "Beginner / non-technical user",
                    "Student / university project team",
                    "Hackathon team",
                    "Founder / entrepreneur",
                    "Product manager",
                    "Other"
                ],
                index=0
            )
            custom_role = ""
            if user_role == "Other":
                custom_role = st.text_input("Specify Your Role")

            main_objective = st.selectbox(
                "Primary Objective",
                options=[
                    "Prepare a developer-ready application specification",
                    "Understand and refine my idea",
                    "Prepare a university project plan",
                    "Prepare a hackathon MVP plan",
                    "Plan a prototype",
                    "Prepare a production-oriented technical plan",
                    "Explore feasibility, risks, and alternatives",
                    "Other"
                ],
                index=0
            )
            custom_objective = ""
            if main_objective == "Other":
                custom_objective = st.text_input("Specify Your Objective")

        with col2:
            st.markdown("<h4 style='color:var(--accent-indigo) !important;'>3. Detail Level & Technical Depth</h4>", unsafe_allow_html=True)
            spec_level = st.selectbox(
                "Specification Detail Level",
                options=["Recommend for me", "Basic", "Intermediate", "Advanced"],
                index=0,
                help="Select 'Recommend for me' to automatically determine depth based on user role and objective."
            )

            tech_experience = st.selectbox(
                "Your Technical Background",
                options=["Intermediate", "No coding experience", "Beginner", "Advanced"],
                index=0
            )

        st.markdown("<h4 style='color:var(--accent-indigo) !important;'>4. Technology Preferences & Constraints</h4>", unsafe_allow_html=True)
        col_tech1, col_tech2 = st.columns(2)
        
        with col_tech1:
            tech_stack = st.multiselect(
                "Preferred Technology Stack (Select multiple or leave empty)",
                options=[
                    "Python", "JavaScript / TypeScript", "React", "Streamlit",
                    "FastAPI", "Django", "Flask", ".NET", "Flutter",
                    "React Native", "SQL / relational databases", "No preference", "Other"
                ],
                default=["Python", "Streamlit"]
            )
            custom_tech_stack = ""
            if "Other" in tech_stack:
                custom_tech_stack = st.text_input("Specify Custom Technology")

            platforms = st.text_input("Target Platforms", placeholder="e.g. Web Browser, iOS, Android, Desktop")

        with col_tech2:
            deadline = st.text_input("Deadline / Timeline", placeholder="e.g. 48 hours hackathon, 2 weeks, 3 months")
            team_size = st.text_input("Team Size", placeholder="e.g. Solo developer, 3 students, 5 engineers")
            budget = st.text_input("Available Budget", placeholder="e.g. Free tier / $0, $500, Enterprise")

        st.markdown("<h4 style='color:var(--accent-indigo) !important;'>5. Additional Constraints & Research Options</h4>", unsafe_allow_html=True)
        additional_reqs = st.text_area(
            "Additional Requirements or Constraints (Optional)",
            placeholder="Specify any unique features, security needs, compliance requirements, or preferences...",
            height=80
        )

        enable_research = st.checkbox(
            "Enable Live Web Research & Market Source Collection (Requires Tavily API Key)",
            value=False,
            help="When checked, Agent 1 will perform public web searches for competitor applications."
        )

        submit_btn = st.form_submit_button("Generate Application Specification Blueprint", type="primary", use_container_width=True)

    if submit_btn:
        raw_form_data = {
            "idea": idea_input,
            "user_role": user_role,
            "custom_role": custom_role,
            "main_objective": main_objective,
            "custom_objective": custom_objective,
            "spec_level": spec_level,
            "tech_experience": tech_experience,
            "tech_stack": tech_stack,
            "custom_tech_stack": custom_tech_stack,
            "deadline": deadline,
            "team_size": team_size,
            "budget": budget,
            "platforms": platforms,
            "additional_requirements": additional_reqs,
            "enable_research": enable_research
        }

        is_valid, user_input_model, errors = validate_user_input(raw_form_data)
        
        if not is_valid:
            for err in errors:
                st.error(f"Validation Warning: {err}")
        else:
            st.divider()
            st.markdown("<h3 style='font-size:1.2rem;'>Multi-Agent Pipeline Executing</h3>", unsafe_allow_html=True)
            
            progress_bar = st.progress(0)
            status_text = st.empty()

            def update_ui_progress(stage: int, total: int, message: str):
                percent = int((stage / total) * 100)
                progress_bar.progress(percent)
                status_text.markdown(f"**Pipeline Step {stage}/{total}:** {message}")

            try:
                workflow = SpecificationWorkflow(progress_callback=update_ui_progress)
                spec_result = workflow.execute(user_input_model)
                st.session_state.generated_spec = spec_result
                st.success("Specification blueprint successfully generated.")
                st.rerun()
            except Exception as ex:
                st.error(f"Workflow execution note: {str(ex)}")
                st.info("Check system logs or provider settings.")

else:
    # Specification Dashboard Results View
    spec: FinalSpecification = st.session_state.generated_spec
    
    col_dash_title, col_dash_btn = st.columns([4, 1])
    with col_dash_title:
        st.markdown(f"<h1 style='font-size:2rem; margin-bottom:0.2rem;'>{spec.project_title}</h1>", unsafe_allow_html=True)
        st.markdown(f"**Detail Depth:** `{spec.effective_level}` | **Status:** Verified Specification Blueprint")
        if spec.level_recommendation_reason:
            st.caption(f"Recommendation Rationale: {spec.level_recommendation_reason}")
    with col_dash_btn:
        if st.button("Create New Blueprint", use_container_width=True):
            st.session_state.generated_spec = None
            st.rerun()

    # Executive Summary Box
    st.markdown(f"""
    <div class="section-card" style="border-left: 4px solid var(--accent-indigo);">
        <h4 style="margin:0 0 0.5rem 0; font-size:1.05rem; color:var(--accent-indigo) !important;">Executive Summary</h4>
        <p style="margin:0; color:var(--text-secondary); line-height:1.6;">{spec.executive_summary}</p>
    </div>
    """, unsafe_allow_html=True)

    # Export Controls Bar
    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        md_content = ExportService.to_markdown(spec)
        st.download_button(
            label="Export Specification Blueprint (.MD)",
            data=md_content,
            file_name=f"{spec.project_title.replace(' ', '_').lower()}.md",
            mime="text/markdown",
            use_container_width=True
        )
    with col_exp2:
        json_content = ExportService.to_json(spec)
        st.download_button(
            label="Export Structured Data (.JSON)",
            data=json_content,
            file_name=f"{spec.project_title.replace(' ', '_').lower()}.json",
            mime="application/json",
            use_container_width=True
        )

    st.divider()

    # Executive Specification Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Product & Problem",
        "Solution Design",
        "Technical Architecture",
        "Critical Audit & Risks",
        "Action Roadmap"
    ])

    # TAB 1: Product Analysis
    with tab1:
        st.markdown("<h3 style='font-size:1.3rem;'>Product & Problem Analysis</h3>", unsafe_allow_html=True)
        pa = spec.product_analysis
        
        st.markdown(f"#### Refined Product Concept\n{pa.refined_idea}")
        st.markdown(f"#### Problem Statement\n{pa.problem_statement}")
        st.markdown(f"#### Core Value Proposition\n{pa.value_proposition}")
        
        col_pa1, col_pa2 = st.columns(2)
        with col_pa1:
            st.subheader("Target User Personas")
            for user in pa.target_users:
                st.markdown(f"- **User:** {user}")
            
            st.subheader("Key Underlying Assumptions")
            for asm in pa.key_assumptions:
                st.markdown(f"- {asm}")

        with col_pa2:
            st.subheader("User Needs & Pain Points")
            for need in pa.user_needs:
                st.markdown(f"- {need}")
                
            if pa.open_questions:
                st.subheader("Open Clarification Questions")
                for q in pa.open_questions:
                    st.markdown(f"- {q}")

        if pa.research_findings:
            st.divider()
            st.subheader("Market Research & Supporting Sources")
            for item in pa.research_findings:
                st.markdown(f"**[{item.title}]({item.url})**  \n*{item.snippet}*")

    # TAB 2: Solution Design
    with tab2:
        st.markdown("<h3 style='font-size:1.3rem;'>Solution & Product Design</h3>", unsafe_allow_html=True)
        sd = spec.solution_design
        
        st.markdown(f"#### Proposed Solution Architecture\n{sd.proposed_solution}")
        
        st.subheader("Feature Categorization & MoSCoW Priorities")
        if sd.features:
            for feat in sd.features:
                p_lower = feat.priority.lower().replace(' ', '')
                badge_class = "badge-must" if "must" in p_lower else ("badge-should" if "should" in p_lower else ("badge-could" if "could" in p_lower else "badge-future"))
                mvp_class = "badge-mvp" if feat.in_mvp else "badge-future"
                mvp_label = "IN MVP" if feat.in_mvp else "FUTURE SCOPE"
                
                st.markdown(f"""
                <div class="feature-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                        <h4 style="margin:0; font-size:1.05rem; color:var(--text-primary) !important;">{feat.name}</h4>
                        <div>
                            <span class="{badge_class}">{feat.priority}</span>
                            <span class="{mvp_class}" style="margin-left:6px;">{mvp_label}</span>
                        </div>
                    </div>
                    <p style="margin:0 0 0.4rem 0; color:var(--text-secondary); font-size:0.9rem;">{feat.description}</p>
                    <p style="margin:0; color:var(--text-muted); font-size:0.82rem; font-style:italic;">Rationale: {feat.reasoning}</p>
                </div>
                """, unsafe_allow_html=True)

        col_sd1, col_sd2 = st.columns(2)
        with col_sd1:
            st.subheader("MVP Scope Boundaries")
            st.markdown("**In-Scope for Initial MVP Release:**")
            for item in sd.mvp_scope:
                st.markdown(f"- {item}")
                
            st.markdown("**Out of Scope (Post-MVP Enhancements):**")
            for item in sd.out_of_scope:
                st.markdown(f"- {item}")

        with col_sd2:
            st.subheader("Primary User Journey Flow")
            for idx, step in enumerate(sd.user_journey, 1):
                st.markdown(f"**Step {idx}:** {step}")
            
            if sd.screens_outline:
                st.subheader("UI Screen Layouts & Views")
                for screen in sd.screens_outline:
                    st.markdown(f"- {screen}")

    # TAB 3: Technical Architecture
    with tab3:
        st.markdown("<h3 style='font-size:1.3rem;'>Technical Architecture & Requirements</h3>", unsafe_allow_html=True)
        ts = spec.technical_specification
        
        st.markdown(f"#### Recommended Technology Stack\n`{ts.tech_stack_recommendation}`")
        st.markdown(f"**Rationale:** {ts.tech_stack_rationale}")
        st.markdown(f"#### Architecture Overview\n{ts.architecture_overview}")
        
        if ts.functional_requirements:
            st.subheader("Functional Requirements")
            fr_data = [{"ID": fr.id, "Requirement Title": fr.title, "Description": fr.description, "Priority": fr.priority} for fr in ts.functional_requirements]
            st.dataframe(fr_data, use_container_width=True)

        if ts.non_functional_requirements:
            st.subheader("Non-Functional Requirements")
            nfr_data = [{"ID": nfr.id, "Category": nfr.category, "Requirement Description": nfr.description} for nfr in ts.non_functional_requirements]
            st.dataframe(nfr_data, use_container_width=True)

        if ts.database_entities:
            st.subheader("Database Schema & Entities")
            for db in ts.database_entities:
                with st.expander(f"Data Entity: {db.name}", expanded=False):
                    st.markdown(f"**Description:** {db.description}")
                    st.markdown(f"**Attributes:** `{', '.join(db.attributes)}`")
                    st.markdown(f"**Relationships:** {', '.join(db.relationships)}")

        if ts.api_integrations:
            st.subheader("API Contracts & Endpoint Specifications")
            for api in ts.api_integrations:
                with st.expander(f"{api.method} {api.endpoint} — {api.name}", expanded=False):
                    st.markdown(f"**Description:** {api.description}")
                    st.json({"request_params": api.request_params, "response_example": api.response_example})

        st.subheader("Phased Development Roadmap")
        for phase in ts.phased_roadmap:
            st.markdown(f"- **{phase}**")

    # TAB 4: Critical Audit
    with tab4:
        st.markdown("<h3 style='font-size:1.3rem;'>Critical Technical Audit & Risk Analysis</h3>", unsafe_allow_html=True)
        rf = spec.review_findings
        
        if rf.addresses_original_problem:
            st.success("Validation Status: Architecture fully aligns with core problem statement.")
        else:
            st.warning("Validation Caution: Solution may contain scope deviations.")

        if rf.corrections_made:
            st.subheader("Automated Corrections Applied")
            for corr in rf.corrections_made:
                st.markdown(f"- {corr}")

        if rf.remaining_risks:
            st.subheader("Technical & Business Risk Matrix")
            for risk in rf.remaining_risks:
                st.markdown(f"- {risk}")

    # TAB 5: Action Roadmap
    with tab5:
        st.markdown("<h3 style='font-size:1.3rem;'>Immediate Implementation Steps</h3>", unsafe_allow_html=True)
        for idx, step in enumerate(spec.immediate_next_steps, 1):
            st.markdown(f"#### Step {idx}: {step}")
