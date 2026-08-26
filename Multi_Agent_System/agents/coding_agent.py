from typing import Any, Dict

from tools.coding_tool import CodingTool


class CodingAgent:
    """
    AI Coding Agent.

    This agent uses CodingTool to:
    - understand software requirements
    - design projects
    - generate files
    - execute generated projects
    - diagnose errors
    - correct failed files
    - retry execution

    The agent acts as the interface between the
    LangGraph system and CodingTool.
    """

    def __init__(self, llm):
        self.llm = llm
        self.coding_tool = CodingTool(llm=llm)

    # =========================================================
    # MAIN AGENT METHOD
    # =========================================================

    def run(self, task: str) -> Dict[str, Any]:
        """
        Execute a complete coding task.

        Example:

            result = agent.run(
                "Create a FastAPI student management API"
            )
        """

        if not task or not task.strip():
            return {
                "success": False,
                "error": "Coding task cannot be empty.",
            }

        try:
            result = self.coding_tool.build_project(
                task=task.strip()
            )

            return {
                "agent": "coding_agent",
                "success": result.get(
                    "success",
                    False,
                ),
                "task": task,
                "result": result,
            }

        except Exception as error:

            return {
                "agent": "coding_agent",
                "success": False,
                "task": task,
                "error": str(error),
            }

    def build_project(
        self,
        task: str,
    ) -> Dict[str, Any]:
        """
        Explicit project-building interface.

        This is useful when another agent or the Meta-Agent
        specifically wants to request software generation.
        """

        return self.run(task)

    def get_summary(
        self,
        result: Dict[str, Any],
    ) -> str:
        """
        Convert the structured coding result into a
        human-readable summary.
        """

        if not result.get("success"):

            error = result.get(
                "error",
                result.get(
                    "result",
                    {},
                ).get(
                    "message",
                    "Unknown coding failure.",
                ),
            )

            return (
                "Coding task failed.\n"
                f"Reason: {error}"
            )

        project = result.get(
            "result",
            {},
        )

        project_name = project.get(
            "project_name",
            "Unknown",
        )

        project_path = project.get(
            "project_path",
            "Unknown",
        )

        attempts = project.get(
            "attempts",
            0,
        )

        files = project.get(
            "generated_files",
            [],
        )

        return (
            "Coding task completed successfully.\n\n"
            f"Project: {project_name}\n"
            f"Location: {project_path}\n"
            f"Files created: {len(files)}\n"
            f"Execution attempts: {attempts}"
        )


def create_coding_agent(llm) -> CodingAgent:
    """
    Create and return a CodingAgent instance.

    Keeping construction in a factory function makes it easier
    to integrate the agent into LangGraph later.
    """

    return CodingAgent(llm=llm)