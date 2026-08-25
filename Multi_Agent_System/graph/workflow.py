from langgraph.graph import END, START, StateGraph

from graph.nodes import (
    coding_node,
    rag_node,
    router_node,
    web_search_node,
)

from graph.state import AgentState


# ============================================================
# ROUTER
# ============================================================

def route_agent(state: AgentState) -> str:
    """
    Determine the next node based on the router decision.
    """

    selected_agent = state.get(
        "selected_agent",
        "",
    )

    if selected_agent == "rag":
        return "rag"

    if selected_agent == "coding":
        return "coding"

    if selected_agent == "web_search":
        return "web_search"

    raise ValueError(
        f"Invalid agent route: {selected_agent}"
    )


# ============================================================
# CREATE WORKFLOW
# ============================================================

def create_workflow():
    """
    Create and compile the Multi-Agent LangGraph workflow.
    """

    workflow = StateGraph(AgentState)

    # ========================================================
    # ADD NODES
    # ========================================================

    workflow.add_node(
        "router",
        router_node,
    )

    workflow.add_node(
        "rag",
        rag_node,
    )

    workflow.add_node(
        "coding",
        coding_node,
    )

    workflow.add_node(
        "web_search",
        web_search_node,
    )

    # ========================================================
    # START → ROUTER
    # ========================================================

    workflow.add_edge(
        START,
        "router",
    )

    # ========================================================
    # ROUTER → SPECIALIST AGENT
    # ========================================================

    workflow.add_conditional_edges(
        "router",
        route_agent,
        {
            "rag": "rag",
            "coding": "coding",
            "web_search": "web_search",
        },
    )

    # ========================================================
    # SPECIALIST AGENTS → END
    # ========================================================

    workflow.add_edge(
        "rag",
        END,
    )

    workflow.add_edge(
        "coding",
        END,
    )

    workflow.add_edge(
        "web_search",
        END,
    )

    # ========================================================
    # COMPILE
    # ========================================================

    return workflow.compile()