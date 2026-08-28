from typing import Any, Dict, List, Optional

from typing_extensions import TypedDict


class AgentState(TypedDict, total=False):
    """
    Shared state used by the LangGraph workflow.
    """

    # User request
    user_query: str

    # Uploaded PDF for the current task
    pdf_path: Optional[str]

    # Agent selected by the router
    selected_agent: Optional[str]

    # Agent results
    rag_result: Optional[str]
    coding_result: Optional[Dict[str, Any]]
    web_search_result: Optional[str]

    # Final response
    final_response: Optional[str]

    # Execution status
    success: bool
    error: Optional[str]
    errors: List[str]

    # Additional information
    metadata: Dict[str, Any]