import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

class Config:
    @staticmethod
    def get(key: str, default: Optional[str] = None) -> Optional[str]:
        """Fetch config from Streamlit secrets or OS environment variables."""
        # Check Streamlit secrets if running inside streamlit
        try:
            import streamlit as st
            if hasattr(st, "secrets") and key in st.secrets:
                return str(st.secrets[key])
        except Exception:
            pass
        return os.getenv(key, default)

    @classmethod
    def get_llm_provider(cls) -> str:
        provider = cls.get("LLM_PROVIDER", "gemini").lower().strip()
        if provider not in ["gemini", "groq"]:
            return "gemini"
        return provider

    @classmethod
    def get_gemini_api_key(cls) -> Optional[str]:
        return cls.get("GEMINI_API_KEY") or cls.get("GOOGLE_API_KEY")

    @classmethod
    def get_gemini_model(cls) -> str:
        return cls.get("GEMINI_MODEL", "gemini-3.6-flash")

    @classmethod
    def get_groq_api_key(cls) -> Optional[str]:
        return cls.get("GROQ_API_KEY")

    @classmethod
    def get_groq_model(cls) -> str:
        return cls.get("GROQ_MODEL", "openai/gpt-oss-120b")

    @classmethod
    def get_tavily_api_key(cls) -> Optional[str]:
        return cls.get("TAVILY_API_KEY")

    @classmethod
    def validate(cls) -> Dict[str, Any]:
        """Validate configuration status and return a dictionary of settings."""
        provider = cls.get_llm_provider()
        gemini_key = cls.get_gemini_api_key()
        groq_key = cls.get_groq_api_key()
        tavily_key = cls.get_tavily_api_key()

        is_valid = False
        active_key = None

        if provider == "gemini" and gemini_key:
            is_valid = True
            active_key = gemini_key
        elif provider == "groq" and groq_key:
            is_valid = True
            active_key = groq_key
        elif gemini_key: # Fallback check
            provider = "gemini"
            is_valid = True
            active_key = gemini_key
        elif groq_key:
            provider = "groq"
            is_valid = True
            active_key = groq_key

        return {
            "provider": provider,
            "is_valid": is_valid,
            "has_gemini_key": bool(gemini_key),
            "has_groq_key": bool(groq_key),
            "has_tavily_key": bool(tavily_key),
            "gemini_model": cls.get_gemini_model(),
            "groq_model": cls.get_groq_model(),
            "active_key_preview": f"{active_key[:4]}...{active_key[-4:]}" if active_key and len(active_key) > 8 else ("Set" if active_key else "Missing")
        }
