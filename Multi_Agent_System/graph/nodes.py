from typing import Any, Dict
from agents.web_search_agent import run_web_search_agent
from agents.coding_agent import create_coding_agent
from agents.rag_agent import run_rag_agent
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv(
    Path(__file__).resolve().parents[1] / ".env"
)
router_model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
)

from graph.state import AgentState

# ============================================================
# ROUTER NODE
# ============================================================

def router_node(state: AgentState) -> Dict[str, Any]:
    """
    Determine which specialized agent should handle
    the user's request.

    Possible routes:

        - rag
        - coding
        - web_search
    """

    query = state.get("user_query", "").strip()

    if not query:
        return {
            "selected_agent": "",
            "error": "User query cannot be empty.",
            "success": False,
        }

    prompt = f"""
You are the routing system of a professional Multi-Agent AI system.

Your job is to select the ONE specialized agent that should
handle the user's request.

Available agents:

1. rag
   Use when the question requires information from the
   PDF/document uploaded by the user.

2. coding
   Use when the user wants to create, modify, debug,
   explain, or generate software/code.

3. web_search
   Use when the user needs current, external, online,
   or web-based information.

USER QUERY:

{query}

Return ONLY one of these exact values:

rag
coding
web_search
"""

    try:

        response = router_model.invoke(prompt)

        route = response.content.strip().lower()

        if route not in {
            "rag",
            "coding",
            "web_search",
        }:
            return {
                "selected_agent": "",
                "error": (
                    f"Router returned invalid route: {route}"
                ),
                "success": False,
            }

        return {
            "selected_agent": route,
            "success": True,
        }

    except Exception as error:

        return {
            "selected_agent": "",
            "error": str(error),
            "errors": [str(error)],
            "success": False,
        }


def rag_node(state: AgentState) -> Dict[str, Any]:
    """
    Execute the RAG Agent using the PDF uploaded
    for the current task.
    """

    query = state.get("user_query", "").strip()
    pdf_path = state.get("pdf_path")

    if not query:
        return {
            "rag_result": "",
            "error": "User query cannot be empty.",
            "success": False,
        }

    if not pdf_path:
        return {
            "rag_result": "",
            "error": "Please upload a PDF document before using the RAG agent.",
            "success": False,
        }

    try:

        response = run_rag_agent(
            query,
            pdf_path
        )

        final_message = response[
            "messages"
        ][-1].content

        return {
            "rag_result": final_message,
            "final_response": final_message,
            "selected_agent": "rag_agent",
            "success": True,
        }

    except Exception as error:

        return {
            "rag_result": "",
            "error": str(error),
            "errors": [str(error)],
            "success": False,
        }

def coding_node(state: AgentState) -> Dict[str, Any]:
    """
    Execute the Coding Agent.

    The node receives the user's coding requirement,
    passes it to CodingAgent, and stores the structured
    coding result in the graph state.
    """

    query = state.get("user_query", "").strip()

    if not query:
        return {
            "coding_result": {},
            "error": "User query cannot be empty.",
            "success": False,
        }

    try:

        coding_agent = create_coding_agent(router_model)

        result = coding_agent.run(query)

        summary = coding_agent.get_summary(result)

        return {
            "coding_result": result,
            "final_response": summary,
            "selected_agent": "coding_agent",
            "success": result.get(
                "success",
                False,
            ),
        }

    except Exception as error:

        return {
            "coding_result": {},
            "error": str(error),
            "errors": [str(error)],
            "success": False,
        }


def web_search_node(state: AgentState) -> Dict[str, Any]:
    """
    Execute the Web Search Agent.
    """

    query = state.get("user_query", "").strip()

    if not query:
        return {
            "web_search_result": "",
            "error": "User query cannot be empty.",
            "success": False,
        }

    try:

        response = run_web_search_agent(query)

        final_message = response[
            "messages"
        ][-1].content

        return {
            "web_search_result": final_message,
            "final_response": final_message,
            "selected_agent": "web_search_agent",
            "success": True,
        }

    except Exception as error:

        return {
            "web_search_result": "",
            "error": str(error),
            "errors": [str(error)],
            "success": False,
        }