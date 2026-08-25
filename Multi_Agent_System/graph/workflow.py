from langgraph.graph import END, START, StateGraph

from graph.nodes import (
    rag_node,
    coding_node,
    web_search_node,
)

from graph.state import AgentState

def create_workflow():
    """
    Create and compile the LangGraph workflow.

    This function is responsible only for defining
    the graph structure.

    Agent logic remains inside the agent and node layers.
    """

    workflow = StateGraph(AgentState)

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


    workflow.add_edge(
        START,
        "rag",
    )


    workflow.add_edge(
        "rag",
        END,
    )


    return workflow.compile()