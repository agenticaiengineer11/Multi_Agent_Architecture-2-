from typing import Any, Dict
from agents.web_search_agent import run_web_search_agent
from agents.coding_agent import create_coding_agent
from agents.rag_agent import run_rag_agent

from graph.state import AgentState


def rag_node(state: AgentState) -> Dict[str, Any]:
    """
    Execute the RAG Agent.

    The node receives the user's query from the shared state,
    sends it to the RAG Agent, and stores the final response
    in the graph state.
    """

    query = state.get("user_query", "").strip()

    if not query:
        return {
            "rag_result": "",
            "error": "User query cannot be empty.",
            "success": False,
        }

    try:
        response = run_rag_agent(query)

        final_message = response["messages"][-1].content

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


def coding_node(
    state: AgentState,
    llm,
) -> Dict[str, Any]:
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

        coding_agent = create_coding_agent(llm)

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