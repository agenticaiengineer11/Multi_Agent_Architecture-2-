from graph.workflow import create_workflow


def main():
    """
    Main entry point for the Multi-Agent System.
    """

    print("=" * 60)
    print("MULTI-AGENT SYSTEM")
    print("=" * 60)

    query = input("\nEnter your query: ").strip()

    if not query:
        print("\nError: Query cannot be empty.")
        return

    # --------------------------------------------------------
    # Create graph
    # --------------------------------------------------------

    graph = create_workflow()

    # --------------------------------------------------------
    # Initial state
    # --------------------------------------------------------

    initial_state = {
        "user_query": query,
        "selected_agent": "",
        "rag_result": "",
        "coding_result": {},
        "web_search_result": "",
        "final_response": "",
        "success": False,
        "error": None,
        "errors": [],
        "metadata": {},
    }

    # --------------------------------------------------------
    # Execute graph
    # --------------------------------------------------------

    try:

        result = graph.invoke(
            initial_state
        )

    except Exception as error:

        print("\nSystem Error:")
        print(error)

        return

    # --------------------------------------------------------
    # Display result
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("MULTI-AGENT RESPONSE")
    print("=" * 60)

    if result.get("final_response"):

        print(result["final_response"])

    elif result.get("error"):

        print(
            "Error:",
            result["error"],
        )

    else:

        print(
            "No response was generated."
        )

    # --------------------------------------------------------
    # Agent information
    # --------------------------------------------------------

    selected_agent = result.get(
        "selected_agent"
    )

    if selected_agent:

        print("\n" + "-" * 60)
        print(
            f"Agent Used: {selected_agent}"
        )


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()