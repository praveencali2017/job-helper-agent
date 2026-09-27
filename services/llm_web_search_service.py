
from tools.ports.llm_web_search import LLMWebSearch
from langchain_core.tools import StructuredTool


class LLMWebSearchService:
    """
    Service that uses a provided LLMWebSearch implementation to perform web searches.
    """
    
    def __init__(self, llm_web_searcher: LLMWebSearch):
        self.llm_web_searcher = llm_web_searcher

    def search(self, url: str):
        """
        Perform a web search using the provided URL.

        Args:
            url (str): The URL to search.

        Returns:
            The result of the web search.
        """
        return self.llm_web_searcher.search(url)

    def as_tools(self) -> list[StructuredTool]:
        """
        Return the LLMWebSearchService as a list of StructuredTool instances.

        Returns:
            A list containing a single StructuredTool instance for web search.
        """
        return [
            StructuredTool.from_function(
                func=self.search,
                name="job_posting_tool",
                description="Look up a job posting URL and return a structured summary of the job details.",
            )
        ]