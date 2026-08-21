import os

from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_core.tools import tool


load_dotenv()


TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


tavily_client = TavilyClient(
    api_key=TAVILY_API_KEY
)


@tool
def web_search(query: str) -> str:
    """
    Search the web for current and relevant information.
    Use this tool when up-to-date web information is required.
    """

    response = tavily_client.search(
        query=query,
        max_results=5
    )

    results = response.get("results", [])

    if not results:
        return "No search results found."

    formatted_results = []

    for result in results:

        title = result.get("title", "No title")
        content = result.get("content", "")
        url = result.get("url", "")

        formatted_results.append(
            f"Title: {title}\n"
            f"Content: {content}\n"
            f"URL: {url}"
        )

    return "\n\n".join(formatted_results)