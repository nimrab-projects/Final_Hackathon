import os
import re
import json
import time
import logging
from typing import Type, TypeVar, Optional, Any
from pydantic import BaseModel
from config import Config

logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)

class LLMService:
    @staticmethod
    def get_crewai_llm():
        """Get CrewAI compatible LLM object based on active provider configuration."""
        provider = Config.get_llm_provider()
        
        if provider == "gemini":
            api_key = Config.get_gemini_api_key()
            model = Config.get_gemini_model()
            if not api_key:
                raise ValueError("GEMINI_API_KEY is not configured.")
            # Standard CrewAI LLM string format for Gemini
            from crewai import LLM
            return LLM(model=f"gemini/{model}", api_key=api_key)
            
        elif provider == "groq":
            api_key = Config.get_groq_api_key()
            model = Config.get_groq_model()
            if not api_key:
                raise ValueError("GROQ_API_KEY is not configured.")
            from crewai import LLM
            return LLM(model=f"groq/{model}", api_key=api_key)
            
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    @staticmethod
    def normalize_dict_keys(data: Any) -> Any:
        """Recursively normalize camelCase and alternate LLM output keys to match Pydantic schemas."""
        if not isinstance(data, dict):
            return data

        mapping = {
            # ProductAnalysis
            "refinedIdea": "refined_idea",
            "refinedConcept": "refined_idea",
            "productConcept": "refined_idea",
            "problemStatement": "problem_statement",
            "problemDescription": "problem_statement",
            "targetUsers": "target_users",
            "targetUserGroups": "target_users",
            "targetPersonas": "target_users",
            "userNeeds": "user_needs",
            "userNeedsAndPainPoints": "user_needs",
            "painPoints": "user_needs",
            "valueProposition": "value_proposition",
            "coreValueProposition": "value_proposition",
            "keyAssumptions": "key_assumptions",
            "openQuestions": "open_questions",
            "researchFindings": "research_findings",

            # SolutionDesign
            "solutionConcept": "proposed_solution",
            "proposedSolution": "proposed_solution",
            "coreFeatures": "features",
            "featuresList": "features",
            "mvpScope": "mvp_scope",
            "inScope": "mvp_scope",
            "outOfScope": "out_of_scope",
            "userJourney": "user_journey",
            "userJourneyFlow": "user_journey",
            "screensOutline": "screens_outline",
            "uiScreens": "screens_outline",
            "futureEnhancements": "future_enhancements",

            # TechnicalSpecification
            "technologyStack": "tech_stack_recommendation",
            "techStack": "tech_stack_recommendation",
            "recommendedTechStack": "tech_stack_recommendation",
            "techStackRationale": "tech_stack_rationale",
            "functionalRequirements": "functional_requirements",
            "nonFunctionalRequirements": "non_functional_requirements",
            "architectureOverview": "architecture_overview",
            "databaseEntities": "database_entities",
            "apiIntegrations": "api_integrations",
            "apiContracts": "api_integrations",
            "securityPrivacyConsiderations": "security_privacy_considerations",
            "validationErrorHandling": "validation_error_handling",
            "testingPlan": "testing_plan",
            "phasedRoadmap": "phased_roadmap",

            # ReviewFindings
            "addressesOriginalProblem": "addresses_original_problem",
            "contradictionsFound": "contradictions_found",
            "unrealisticConstraints": "unrealistic_constraints",
            "unnecessaryComplexity": "unnecessary_complexity",
            "missingConsiderations": "missing_considerations",
            "correctionsMade": "corrections_made",
            "remainingRisks": "remaining_risks",

            # FinalSpecification
            "projectTitle": "project_title",
            "effectiveLevel": "effective_level",
            "levelRecommendationReason": "level_recommendation_reason",
            "executiveSummary": "executive_summary",
            "productAnalysis": "product_analysis",
            "solutionDesign": "solution_design",
            "technicalSpecification": "technical_specification",
            "reviewFindings": "review_findings",
            "immediateNextSteps": "immediate_next_steps",
        }

        new_data = {}
        for k, v in data.items():
            key = mapping.get(k, k)
            if isinstance(v, dict):
                new_data[key] = LLMService.normalize_dict_keys(v)
            elif isinstance(v, list):
                new_data[key] = [LLMService.normalize_dict_keys(item) if isinstance(item, dict) else item for item in v]
            else:
                new_data[key] = v

        # Format technologyStack dictionary if LLM returned dict instead of string
        if "tech_stack_recommendation" in new_data and isinstance(new_data["tech_stack_recommendation"], dict):
            ts_dict = new_data["tech_stack_recommendation"]
            new_data["tech_stack_recommendation"] = ", ".join([f"{k.capitalize()}: {v}" if isinstance(v, str) else f"{k.capitalize()}: {json.dumps(v)}" for k, v in ts_dict.items()])

        return new_data

    @staticmethod
    def parse_json_to_pydantic(text: str, response_model: Type[T]) -> T:
        """Extract JSON from raw LLM output and parse into Pydantic model with key normalization."""
        clean_text = text.strip()
        json_match = re.search(r"```(?:json)?\s*(\{.*\}|\[.*\])\s*```", clean_text, re.DOTALL)
        if json_match:
            clean_text = json_match.group(1).strip()
        else:
            brace_match = re.search(r"(\{.*\})", clean_text, re.DOTALL)
            if brace_match:
                clean_text = brace_match.group(1).strip()

        # Attempt direct JSON load
        raw_data = None
        try:
            raw_data = json.loads(clean_text)
        except Exception:
            try:
                import json_repair
                repaired = json_repair.repair_json(clean_text)
                raw_data = json.loads(repaired)
            except Exception as parse_err:
                logger.error(f"Failed to parse raw LLM JSON: {parse_err}. Raw snippet: {clean_text[:300]}")
                raise ValueError(f"JSON parsing error for {response_model.__name__}: {str(parse_err)}")

        # Normalize key names (camelCase -> snake_case) before validation
        if isinstance(raw_data, dict):
            normalized_data = LLMService.normalize_dict_keys(raw_data)
        else:
            normalized_data = raw_data

        try:
            return response_model.model_validate(normalized_data)
        except Exception as val_err:
            logger.warning(f"Pydantic validation notice for {response_model.__name__}: {val_err}. Retrying with relaxed repair...")
            # Fallback repair if features or requirements are strings
            if isinstance(normalized_data, dict):
                if response_model.__name__ == "SolutionDesign" and "features" in normalized_data and isinstance(normalized_data["features"], list):
                    fixed_features = []
                    from models.schemas import FeatureItem
                    for f in normalized_data["features"]:
                        if isinstance(f, dict):
                            fixed_features.append(FeatureItem(
                                name=f.get("name") or f.get("feature") or "Core Feature",
                                description=f.get("description") or "Feature description",
                                priority=f.get("priority") or "Must Have",
                                in_mvp=bool(f.get("in_mvp", True)),
                                reasoning=f.get("reasoning") or ""
                            ))
                        elif isinstance(f, str):
                            fixed_features.append(FeatureItem(name=f, description=f, priority="Must Have", in_mvp=True))
                    normalized_data["features"] = fixed_features

            return response_model.model_validate(normalized_data)

    @classmethod
    def generate_structured(cls, prompt: str, response_model: Type[T], system_prompt: Optional[str] = None) -> T:
        """
        Generate structured output using active provider or fallback.
        """
        config_status = Config.validate()
        if not config_status["is_valid"]:
            logger.warning("No valid API key found. Falling back to mock structured response.")
            return cls.generate_mock(prompt, response_model)

        provider = config_status["provider"]
        full_system = (system_prompt or "") + (
            f"\n\nCRITICAL: You MUST respond ONLY with valid JSON matching the schema for {response_model.__name__}. "
            "Do not include any conversational intro or extra text outside JSON."
        )

        try:
            if provider == "gemini":
                api_key = Config.get_gemini_api_key()
                primary_model = Config.get_gemini_model()

                candidates = [primary_model, "gemini-flash-latest", "gemini-3.8-flash", "gemini-pro-latest"]
                candidate_models = []
                for m in candidates:
                    if m not in candidate_models:
                        candidate_models.append(m)

                last_err = None
                from google import genai
                from google.genai import types

                client = genai.Client(api_key=api_key)

                for model_name in candidate_models:
                    for attempt in range(3):
                        try:
                            res = client.models.generate_content(
                                model=model_name,
                                contents=prompt,
                                config=types.GenerateContentConfig(
                                    system_instruction=full_system,
                                    response_mime_type="application/json",
                                    response_schema=response_model,
                                    temperature=0.3
                                )
                            )
                            if res.text:
                                return cls.parse_json_to_pydantic(res.text, response_model)
                        except Exception as genai_err:
                            last_err = genai_err
                            err_str = str(genai_err)
                            if ("503" in err_str or "429" in err_str or "UNAVAILABLE" in err_str):
                                sleep_time = (attempt + 1) * 2
                                logger.warning(f"Gemini model '{model_name}' rate limit (attempt {attempt+1}/3). Retrying in {sleep_time}s...")
                                time.sleep(sleep_time)
                                continue
                            else:
                                break

                raise last_err or RuntimeError("All Gemini model API attempts failed.")

            elif provider == "groq":
                api_key = Config.get_groq_api_key()
                model_name = Config.get_groq_model()
                from groq import Groq
                client = Groq(api_key=api_key)
                completion = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": full_system},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.3
                )
                raw_json = completion.choices[0].message.content
                return cls.parse_json_to_pydantic(raw_json, response_model)

        except Exception as err:
            logger.warning(f"Primary provider '{provider}' failed ({str(err)[:100]}). Attempting automatic cross-provider fallback...")
            groq_key = Config.get_groq_api_key()
            if provider == "gemini" and groq_key:
                try:
                    from groq import Groq
                    model_name = Config.get_groq_model()
                    client = Groq(api_key=groq_key)
                    completion = client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": full_system},
                            {"role": "user", "content": prompt}
                        ],
                        response_format={"type": "json_object"},
                        temperature=0.3
                    )
                    raw_json = completion.choices[0].message.content
                    return cls.parse_json_to_pydantic(raw_json, response_model)
                except Exception as groq_err:
                    logger.warning(f"Groq fallback also failed: {groq_err}")

            return cls.generate_mock(prompt, response_model)

    @classmethod
    def generate_mock(cls, prompt: str, response_model: Type[T]) -> T:
        """
        Generate dynamic schema-compliant data tailored specifically to the user's app idea.
        """
        name = response_model.__name__

        # Extract user idea context from prompt
        idea_context = "Custom Application"
        if "USER IDEA:" in prompt:
            try:
                idea_context = prompt.split("USER IDEA:")[1].split("\n\n")[0].strip()
            except Exception:
                pass
        elif "APP IDEA / REFINED CONCEPT:" in prompt:
            try:
                idea_context = prompt.split("APP IDEA / REFINED CONCEPT:")[1].split("\n\n")[0].strip()
            except Exception:
                pass
        elif "APP IDEA:" in prompt:
            try:
                idea_context = prompt.split("APP IDEA:")[1].split("\n\n")[0].strip()
            except Exception:
                pass

        idea_lower = idea_context.lower()

        # Dynamic topic detection & custom feature generator
        if "email" in idea_lower:
            domain = "AI Email Generator & Outreach Suite"
            problem = "Users waste hours drafting professional emails, follow-ups, and marketing templates manually."
            value = "Automates email drafting, subject line optimization, and personalized bulk outreach in seconds."
            features_list = [
                ("AI Subject Line & Body Generator", "Generates high-converting email drafts based on user tone and goal", "Must Have", True, "Core user requirement"),
                ("Custom Template Library", "Save and reuse custom email templates for sales, support, and cold outreach", "Must Have", True, "Efficiency requirement"),
                ("SMTP & Email Service Integration", "Send emails directly via SendGrid, Mailgun, or custom SMTP servers", "Must Have", True, "Execution requirement"),
                ("Personalization Merge Tags", "Insert dynamic fields like {{first_name}} and {{company_name}}", "Should Have", True, "Personalization feature"),
                ("Automated Follow-up Sequences", "Schedule multi-step automated email drip sequences", "Could Have", False, "Advanced outreach feature")
            ]
            tech_stack = "Python, FastAPI, React, PostgreSQL, SendGrid API, OpenAI / Groq API"
            tech_rationale = "FastAPI handles high-throughput async email drafting; React provides an intuitive rich-text editor; SendGrid manages transactional delivery."
            db_entities = [
                ("UserAccount", "Stores user credentials and API preferences", ["id", "email", "api_key", "created_at"]),
                ("EmailTemplate", "Stores reusable email templates and prompt settings", ["id", "user_id", "title", "subject", "body_content"]),
                ("GeneratedEmail", "Tracks sent and generated email drafts", ["id", "user_id", "recipient", "status", "created_at"])
            ]
            apis = [
                ("Generate Email Draft API", "POST", "/api/v1/emails/generate", "Generates structured email subject and body"),
                ("Send Transactional Email API", "POST", "/api/v1/emails/send", "Dispatches email to target recipient via SMTP")
            ]
        elif "ride" in idea_lower or "cab" in idea_lower or "taxi" in idea_lower:
            domain = "On-Demand Ride Sharing Platform"
            problem = "Commuters and drivers need a real-time, transparent platform for matching rides and processing payments."
            value = "Connects riders with nearby drivers instantly with GPS tracking and automated fare estimation."
            features_list = [
                ("Real-time Driver Matching", "Locate nearby drivers based on current GPS location", "Must Have", True, "Core dispatch feature"),
                ("Interactive Map & Live GPS Tracking", "Track driver route and ETA on live interactive map", "Must Have", True, "Rider UX requirement"),
                ("Fare Estimator & Payment Gateway", "Calculate ride cost and process credit card payments via Stripe", "Must Have", True, "Financial transaction"),
                ("Driver & Passenger Rating System", "Two-way ratings to maintain safety and platform quality", "Should Have", True, "Trust & safety"),
                ("Scheduled Rides & Pool Matching", "Pre-book rides or share trips with nearby commuters", "Could Have", False, "Scale enhancement")
            ]
            tech_stack = "Flutter, Node.js (NestJS), PostgreSQL / PostGIS, WebSockets, Google Maps API, Stripe API"
            tech_rationale = "Flutter provides cross-platform mobile apps for Riders & Drivers; WebSockets handle real-time GPS coordinates; PostGIS processes geo-queries."
            db_entities = [
                ("UserProfile", "Stores rider and driver accounts", ["id", "name", "phone", "role", "rating"]),
                ("RideRequest", "Tracks ride requests, status, and route points", ["id", "rider_id", "driver_id", "origin_geo", "destination_geo", "fare"]),
                ("PaymentRecord", "Stores Stripe transaction logs", ["id", "ride_id", "amount", "payment_status", "created_at"])
            ]
            apis = [
                ("Request Ride API", "POST", "/api/v1/rides/request", "Submits new ride request and triggers driver matching"),
                ("Update GPS Coordinates API", "POST", "/api/v1/drivers/location", "Streams driver live GPS coordinates via WebSocket/HTTP")
            ]
        else:
            domain = f"Software Platform for '{idea_context[:60]}'"
            problem = f"Users require a modern, streamlined solution for '{idea_context[:70]}' without complex manual workflows."
            value = f"Delivers an automated, intuitive platform tailored to '{idea_context[:50]}'."
            features_list = [
                ("Interactive User Dashboard", "Centralized control panel for managing core operations", "Must Have", True, "Core interface"),
                ("Automated Workflow Processing Engine", f"Executes data processing and logic for '{idea_context[:40]}'", "Must Have", True, "Core functionality"),
                ("Export & Integration Gateway", "Export data reports and connect with third-party webhooks", "Must Have", True, "Integration requirement"),
                ("Advanced Analytics & Reporting", "Visual charts and performance insights", "Should Have", True, "Analytics feature"),
                ("Multi-user Collaboration & Team Roles", "Role-based access control for teams", "Could Have", False, "Team management")
            ]
            tech_stack = "Python, FastAPI, React (TypeScript), PostgreSQL, Redis, Docker"
            tech_rationale = "FastAPI & React provide rapid development with high performance, strong type safety, and seamless cloud deployment."
            db_entities = [
                ("UserAccount", "Stores user profile and authentication settings", ["id", "username", "email", "role"]),
                ("ProjectRecord", f"Stores main data entities for '{idea_context[:30]}'", ["id", "user_id", "title", "data_payload", "created_at"]),
                ("SystemAuditLog", "Logs system activity and background task status", ["id", "event_type", "details", "timestamp"])
            ]
            apis = [
                ("Create Record API", "POST", "/api/v1/records/create", "Creates new application record"),
                ("Fetch Dashboard Data API", "GET", "/api/v1/dashboard/summary", "Returns analytics and active records summary")
            ]

        if name == "ProductAnalysis":
            return response_model(
                refined_idea=f"Application Plan for {domain}",
                problem_statement=problem,
                target_users=["Software Developers", "End Users", "Domain Professionals", "Platform Administrators"],
                user_needs=["Step-by-step feature roadmap", "Modern technology stack recommendation", "Structured Database & API contracts"],
                value_proposition=value,
                key_assumptions=["Target platforms (Web/Mobile) are accessible to end users", "Required third-party APIs have active network connectivity"],
                open_questions=["What specific cloud hosting provider is preferred for deployment?", "Are there specific security compliance standards required?"],
                research_findings=[]
            )

        elif name == "SolutionDesign":
            from models.schemas import FeatureItem
            feats = [FeatureItem(name=f[0], description=f[1], priority=f[2], in_mvp=f[3], reasoning=f[4]) for f in features_list]
            return response_model(
                proposed_solution=f"An end-to-end software solution for {domain}, providing intuitive workflows, fast data processing, and seamless user interaction.",
                features=feats,
                mvp_scope=[f[0] for f in features_list if f[3]],
                out_of_scope=[f[0] for f in features_list if not f[3]],
                user_journey=[
                    "User accesses application and completes authentication",
                    f"User submits input/request for '{idea_context[:40]}'",
                    "System processes data via core engine and APIs",
                    "User views interactive results dashboard and exports output"
                ],
                screens_outline=[
                    "Home & Input Form Page",
                    "Interactive Processing Dashboard",
                    "Settings & API Integration View"
                ],
                future_enhancements=["Integration with cloud storage providers", "Automated deployment pipeline templates"]
            )

        elif name == "TechnicalSpecification":
            from models.schemas import FunctionalRequirement, NonFunctionalRequirement, DatabaseEntity, APIContract
            d_entities = [DatabaseEntity(name=d[0], description=d[1], attributes=d[2], relationships=[]) for d in db_entities]
            a_contracts = [APIContract(name=a[0], method=a[1], endpoint=a[2], description=a[3], request_params="{\"input\": \"data\"}", response_example="{\"status\": \"success\"}", is_required=True) for a in apis]
            
            return response_model(
                tech_stack_recommendation=tech_stack,
                tech_stack_rationale=tech_rationale,
                functional_requirements=[
                    FunctionalRequirement(id="FR-01", title=f"{features_list[0][0]} Requirement", description=features_list[0][1], priority="Must Have"),
                    FunctionalRequirement(id="FR-02", title=f"{features_list[1][0]} Requirement", description=features_list[1][1], priority="Must Have")
                ],
                non_functional_requirements=[
                    NonFunctionalRequirement(id="NFR-01", category="Performance", description="API endpoints must respond within 500ms under standard load."),
                    NonFunctionalRequirement(id="NFR-02", category="Security", description="All secret credentials and API tokens must be securely stored in environment variables.")
                ],
                architecture_overview=f"Modular 3-Tier Architecture: React/Mobile Client Layer -> FastAPI/Node.js Service Layer -> PostgreSQL Database & External API Integrations.",
                database_entities=d_entities,
                api_integrations=a_contracts,
                security_privacy_considerations=["Sanitize user input before processing", "Encrypt sensitive database columns and API tokens"],
                validation_error_handling=["Validate all payload data with schema validators", "Implement rate limiting and retry mechanisms"],
                testing_plan=["Unit tests for core services", "API endpoint integration tests", "Manual UI journey verification"],
                phased_roadmap=["Phase 1: Database & Core API Setup", "Phase 2: UI Dashboard & Features", "Phase 3: Testing & Deployment"]
            )

        elif name == "ReviewFindings":
            return response_model(
                addresses_original_problem=True,
                contradictions_found=[],
                unrealistic_constraints=[],
                unnecessary_complexity=[],
                missing_considerations=["Ensure rate limit retry mechanisms for API calls"],
                corrections_made=["Aligned technical stack recommendations with specified user constraints"],
                remaining_risks=["API availability or rate limits during peak usage"]
            )

        elif name == "FinalSpecification":
            return response_model(
                project_title=f"Specification Blueprint: {domain}",
                effective_level="Intermediate",
                level_recommendation_reason="Recommended Intermediate detail level based on developer target objective.",
                executive_summary=f"Comprehensive engineering blueprint transforming '{idea_context[:80]}' into an actionable application specification.",
                product_analysis=cls.generate_mock(prompt, response_model.__annotations__["product_analysis"]),
                solution_design=cls.generate_mock(prompt, response_model.__annotations__["solution_design"]),
                technical_specification=cls.generate_mock(prompt, response_model.__annotations__["technical_specification"]),
                review_findings=cls.generate_mock(prompt, response_model.__annotations__["review_findings"]),
                immediate_next_steps=[
                    f"Review recommended tech stack ({tech_stack}).",
                    "Set up project repository using provided database schemas and API contracts.",
                    "Implement Phase 1 MVP features based on functional requirements."
                ]
            )

        raise ValueError(f"No mock template for model: {name}")

