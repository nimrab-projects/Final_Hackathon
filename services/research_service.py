import logging
from typing import List, Tuple
from config import Config
from models.schemas import ResearchItem

logger = logging.getLogger(__name__)

class ResearchService:
    @staticmethod
    def perform_research(idea_summary: str, enable_research: bool = False) -> Tuple[List[ResearchItem], str]:
        """
        Perform web research via Tavily API if enabled and configured.
        Returns a tuple of (List[ResearchItem], summary_text).
        """
        if not enable_research:
            return [], "External web research was disabled by user request."

        tavily_key = Config.get_tavily_api_key()
        if not tavily_key:
            logger.warning("Tavily API key is missing. Skipping external web research.")
            return [], "External research was requested, but no TAVILY_API_KEY is configured. Proceeding with existing model knowledge."

        try:
            from tavily import TavilyClient
            client = TavilyClient(api_key=tavily_key)
            query = f"Application solution competitors market analysis: {idea_summary[:150]}"
            response = client.search(query=query, search_depth="basic", max_results=4)
            
            results: List[ResearchItem] = []
            raw_results = response.get("results", [])
            for item in raw_results:
                results.append(
                    ResearchItem(
                        title=item.get("title", "Web Source"),
                        url=item.get("url", "#"),
                        snippet=item.get("content", "")[:300] + "...",
                        relevance="High" if item.get("score", 0) > 0.7 else "Medium"
                    )
                )

            if results:
                summary = f"Retrieved {len(results)} relevant external web sources via Tavily Search API."
            else:
                summary = "Tavily search completed, but no relevant public web sources were found."
            
            return results, summary

        except Exception as e:
            logger.error(f"Error performing Tavily research: {str(e)}")
            return [], f"External research attempted but encountered an error: {str(e)}. Proceeding without live search data."
