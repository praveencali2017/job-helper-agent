from tools.ports.llm_web_search import LLMWebSearch
from openai import OpenAI
from config import settings
from prompt_templates import job_search_sys_prompt, job_search_user_prompt
import re
from loguru import logger
class OpenAIWebSearch(LLMWebSearch):
    """Web search implementation backed by the OpenAI Responses API.

    Uses an LLM with web-search tooling to look up a job posting URL and
    return a cleaned, citation-free summary of the results.
    """

    def __init__(self, model: str = "gpt-4o"):
        """Initialize the OpenAI-backed web search.

        Args:
            model: The OpenAI model name to use for the search.
                Defaults to "gpt-4o".

        Note:
            The API key is read from ``OPENAI_API_KEY`` via ``config.settings``
            (environment variable or ``.env``).
        """
        self.client = OpenAI(api_key=settings.openai_api_key.get_secret_value())
        self.model = model
        self.system_prompt = job_search_sys_prompt
        self.user_prompt_template = job_search_user_prompt

    def search(self, url: str) -> str:
        """Perform a web search for the given job posting URL.

        Sends the system prompt and a formatted user prompt (with the job
        link) to the OpenAI Responses API, then strips any markdown
        citations/source links from the returned text.

        Args:
            url: The job posting link to search for.

        Returns:
            The cleaned response text with citations and source links removed.
        """
        logger.info(f"Searching for '{url}' using OpenAI API")
        response = self.client.responses.create(
            model=self.model,
            tools = [{"type": "web_search", "search_context_size": "medium"}],
            tool_choice = "required",
            input=[
                self.system_prompt,
                {
                    "role": "user",
                    "content": self.user_prompt_template["content"].format(job_link_url=url)
                }
            ]
        )
        # Clear citations and source links from the response text
        cleaned = re.sub(r"\s*\(\[[^\]]+\]\([^)]+\)\)", "", response.output_text)
        return cleaned.strip()
