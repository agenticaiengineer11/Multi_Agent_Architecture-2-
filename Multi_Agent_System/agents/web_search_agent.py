from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq

from tools.web_search_tool import web_search


# ============================================================
# Environment
# ============================================================

load_dotenv(
    Path(__file__).resolve().parents[1] / ".env"
)


# ============================================================
# Model
# ============================================================

model = ChatGroq(
    model="whisper-large-v3",
    temperature=0,
)


# ============================================================
# System Prompt
# ============================================================

SYSTEM_PROMPT = """
You are a professional Web Research Agent.

Your responsibility is to research information from the web.

Rules:

1. Use the web_search tool when current or external
   information is required.

2. Do not invent information.

3. Base your answer on the search results.

4. Provide a clear and concise answer.

5. When useful, mention the source URLs.
"""


# ============================================================
# Web Search Agent
# ============================================================

web_search_agent = create_agent(
    model=model,
    tools=[web_search],
    system_prompt=SYSTEM_PROMPT,
)


# ============================================================
# Runner
# ============================================================

def run_web_search_agent(query: str):
    """
    Run the Web Search Agent with a user query.
    """

    if not query or not query.strip():
        raise ValueError(
            "Web search query cannot be empty."
        )

    response = web_search_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query.strip(),
                }
            ]
        }
    )

    return response


# ============================================================
# CLI TEST
# ============================================================

if __name__ == "__main__":

    query = input(
        "Ask the Web Search Agent: "
    )

    result = run_web_search_agent(query)

    print("\n" + "=" * 60)
    print("WEB SEARCH AGENT")
    print("=" * 60)

    print(
        result["messages"][-1].content
    )