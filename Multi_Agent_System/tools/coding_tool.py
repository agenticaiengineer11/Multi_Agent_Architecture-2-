from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


MAX_ATTEMPTS = 3
DEFAULT_WORKSPACE = "generated_projects"


class CodingTool:
    """
    AI Coding Assistant / Project Builder.

    Responsibilities:
        1. Analyze the user's coding requirement.
        2. Design the project architecture.
        3. Create a file/folder plan.
        4. Generate code for each file.
        5. Write files to the workspace.
        6. Analyze the generated project.
        7. Execute/test the project.
        8. Analyze errors.
        9. Correct failed files.
        10. Retry until success or MAX_ATTEMPTS is reached.

    IMPORTANT:
        Generated projects are restricted to the configured workspace.
        Later, execution should be moved into a Docker sandbox.
    """

    def __init__(
        self,
        llm,
        workspace: str = DEFAULT_WORKSPACE,
    ):
        self.llm = llm
        self.parser = StrOutputParser()

        self.workspace = Path(workspace).resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)

    def _invoke(self, prompt, variables: Dict[str, Any]) -> str:
        """
        Execute an LLM chain and return a cleaned string.
        """

        chain = prompt | self.llm | self.parser

        return chain.invoke(variables).strip()


    def _parse_json(self, response: str) -> Dict[str, Any]:
        """
        Parse JSON returned by the LLM.

        Handles accidental Markdown code fences.
        """

        cleaned = response.strip()

        cleaned = re.sub(
            r"^```(?:json)?\s*",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

        cleaned = re.sub(
            r"\s*```$",
            "",
            cleaned,
        )

        try:
            return json.loads(cleaned)

        except json.JSONDecodeError as error:
            raise ValueError(
                f"LLM returned invalid JSON.\n\nResponse:\n{response}"
            ) from error


    def analyze_task(self, task: str) -> Dict[str, Any]:
        """
        Convert a natural-language requirement into structured
        software requirements.
        """

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are a senior software architect.

Analyze the user's software development requirement.

Determine:

1. Project purpose
2. Main features
3. Inputs
4. Outputs
5. Required technologies
6. Required components
7. Database requirements
8. API requirements
9. Testing requirements
10. Important constraints
11. Potential edge cases

Return ONLY valid JSON.

Use this structure:

{
    "project_name": "string",
    "purpose": "string",
    "features": [],
    "inputs": [],
    "outputs": [],
    "technologies": [],
    "components": [],
    "database_required": false,
    "api_required": false,
    "testing_required": true,
    "constraints": [],
    "edge_cases": []
}
                    """,
                ),
                (
                    "human",
                    """
USER REQUIREMENT:

{task}
                    """,
                ),
            ]
        )

        response = self._invoke(
            prompt,
            {"task": task},
        )

        return self._parse_json(response)

    def design_project(
        self,
        task: str,
        analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Design the software architecture and file structure.
        """

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are a senior software architect and project planner.

Based on the user's requirement and analysis, design a complete
software project.

Determine:

- Project architecture
- Directories
- Required files
- Purpose of every file
- Dependencies
- Entry point
- Testing structure

Rules:

- Do not create unnecessary files.
- Use professional project organization.
- Every generated file must have a clear purpose.
- Paths must be relative paths.
- Never use absolute paths.
- Never use paths containing "..".
- Include tests when appropriate.

Return ONLY valid JSON.

Format:

{
    "project_name": "string",
    "architecture": "string",
    "entry_point": "string",
    "dependencies": [],
    "directories": [],
    "files": [
        {
            "path": "main.py",
            "purpose": "Application entry point"
        }
    ]
}
                    """,
                ),
                (
                    "human",
                    """
USER REQUIREMENT:

{task}

REQUIREMENT ANALYSIS:

{analysis}
                    """,
                ),
            ]
        )

        response = self._invoke(
            prompt,
            {
                "task": task,
                "analysis": json.dumps(
                    analysis,
                    indent=2,
                ),
            },
        )

        return self._parse_json(response)


    def _safe_path(self, relative_path: str) -> Path:
        """
        Ensure the generated path stays inside the workspace.
        """

        if not relative_path:
            raise ValueError("File path cannot be empty.")

        path = Path(relative_path)

        if path.is_absolute():
            raise ValueError(
                f"Absolute paths are not allowed: {relative_path}"
            )

        if ".." in path.parts:
            raise ValueError(
                f"Parent-directory traversal is not allowed: {relative_path}"
            )

        destination = (self.workspace / path).resolve()

        try:
            destination.relative_to(self.workspace)

        except ValueError as error:
            raise ValueError(
                f"Unsafe file path: {relative_path}"
            ) from error

        return destination

    def create_directories(
        self,
        directories: List[str],
    ) -> None:
        """
        Create all planned directories.
        """

        for directory in directories:
            directory_path = self._safe_path(directory)
            directory_path.mkdir(
                parents=True,
                exist_ok=True,
            )

    def generate_file(
        self,
        task: str,
        analysis: Dict[str, Any],
        architecture: Dict[str, Any],
        file_path: str,
        file_purpose: str,
    ) -> str:
        """
        Generate the contents of one project file.
        """

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are a senior software engineer.

Generate the complete contents of the requested project file.

Rules:

- Return ONLY the file contents.
- Do not use Markdown code fences.
- Do not explain the code.
- Follow the project architecture.
- Follow the file's purpose.
- Write production-quality code.
- Use the selected technology stack.
- Keep imports correct.
- Make the file compatible with the other project files.
                    """,
                ),
                (
                    "human",
                    """
USER REQUIREMENT:

{task}

REQUIREMENT ANALYSIS:

{analysis}

PROJECT ARCHITECTURE:

{architecture}

FILE PATH:

{file_path}

FILE PURPOSE:

{file_purpose}

Generate the complete file.
                    """,
                ),
            ]
        )

        return self._invoke(
            prompt,
            {
                "task": task,
                "analysis": json.dumps(
                    analysis,
                    indent=2,
                ),
                "architecture": json.dumps(
                    architecture,
                    indent=2,
                ),
                "file_path": file_path,
                "file_purpose": file_purpose,
            },
        )

    def write_file(
        self,
        relative_path: str,
        content: str,
    ) -> str:
        """
        Write generated content to a file inside the workspace.
        """

        file_path = self._safe_path(relative_path)

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path.write_text(
            content,
            encoding="utf-8",
        )

        return str(file_path)


    def generate_project(
        self,
        task: str,
        analysis: Dict[str, Any],
        architecture: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate every file in the project.
        """

        project_name = architecture["project_name"]

        project_root = self._safe_path(project_name)

        project_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        generated_files = []

        for file_info in architecture.get("files", []):

            relative_file = file_info["path"]
            purpose = file_info["purpose"]

            project_relative_path = (
                Path(project_name) / relative_file
            )

            code = self.generate_file(
                task=task,
                analysis=analysis,
                architecture=architecture,
                file_path=str(project_relative_path),
                file_purpose=purpose,
            )

            written_path = self.write_file(
                str(project_relative_path),
                code,
            )

            generated_files.append(
                {
                    "path": str(project_relative_path),
                    "purpose": purpose,
                    "absolute_path": written_path,
                }
            )

        return {
            "project_name": project_name,
            "project_path": str(project_root),
            "files": generated_files,
        }


    def analyze_project(
        self,
        task: str,
        analysis: Dict[str, Any],
        architecture: Dict[str, Any],
        generated_project: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Review the generated project before execution.
        """

        project_content = {}

        for file_info in generated_project["files"]:

            file_path = Path(
                file_info["absolute_path"]
            )

            try:
                content = file_path.read_text(
                    encoding="utf-8"
                )

                project_content[
                    file_info["path"]
                ] = content

            except Exception as error:

                project_content[
                    file_info["path"]
                ] = f"Unable to read file: {error}"

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are a senior software engineer performing a
pre-execution project review.

Check:

- Architecture consistency
- Missing files
- Incorrect imports
- Syntax risks
- Logic problems
- Missing dependencies
- Broken references between files
- Requirement coverage
- Security concerns

Return ONLY valid JSON:

{
    "passed": true,
    "score": 0,
    "issues": [],
    "recommendations": []
}
                    """,
                ),
                (
                    "human",
                    """
USER REQUIREMENT:

{task}

ANALYSIS:

{analysis}

ARCHITECTURE:

{architecture}

GENERATED PROJECT:

{project}
                    """,
                ),
            ]
        )

        response = self._invoke(
            prompt,
            {
                "task": task,
                "analysis": json.dumps(
                    analysis,
                    indent=2,
                ),
                "architecture": json.dumps(
                    architecture,
                    indent=2,
                ),
                "project": json.dumps(
                    project_content,
                    indent=2,
                ),
            },
        )

        return self._parse_json(response)

    def find_entry_point(
        self,
        project_path: Path,
        architecture: Dict[str, Any],
    ) -> Path:
        """
        Determine the project entry point.
        """

        entry_point = architecture.get(
            "entry_point"
        )

        if entry_point:

            candidate = (
                project_path / entry_point
            ).resolve()

            try:
                candidate.relative_to(
                    project_path.resolve()
                )

            except ValueError:
                raise ValueError(
                    "Invalid entry point."
                )

            if candidate.exists():
                return candidate

        # Common Python fallbacks

        for filename in [
            "main.py",
            "app.py",
            "run.py",
        ]:

            candidate = (
                project_path / filename
            )

            if candidate.exists():
                return candidate

        raise FileNotFoundError(
            "Could not find a Python entry point."
        )


    def execute_project(
        self,
        project_path: str,
        architecture: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Execute the generated project.

        NOTE:
        This is the development version.

        Later this method will execute the project inside
        a Docker sandbox.
        """

        root = Path(project_path).resolve()

        entry_point = self.find_entry_point(
            root,
            architecture,
        )

        try:

            result = subprocess.run(
                [
                    sys.executable,
                    str(entry_point),
                ],
                cwd=str(root),
                capture_output=True,
                text=True,
                timeout=30,
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
            }

        except subprocess.TimeoutExpired:

            return {
                "success": False,
                "stdout": "",
                "stderr": "Project execution timed out.",
                "return_code": -1,
            }

        except Exception as error:

            return {
                "success": False,
                "stdout": "",
                "stderr": str(error),
                "return_code": -1,
            }

    def analyze_error(
        self,
        task: str,
        project: Dict[str, Any],
        execution_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Determine the root cause of a project execution error.
        """

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are a senior debugging engineer.

Analyze the project's execution failure.

Determine:

1. Root cause
2. Affected file
3. Exact problem
4. Required correction

Return ONLY valid JSON:

{
    "root_cause": "string",
    "affected_files": [],
    "problem": "string",
    "fix": "string"
}
                    """,
                ),
                (
                    "human",
                    """
TASK:

{task}

PROJECT:

{project}

EXECUTION ERROR:

{error}
                    """,
                ),
            ]
        )

        response = self._invoke(
            prompt,
            {
                "task": task,
                "project": json.dumps(
                    project,
                    indent=2,
                ),
                "error": execution_result.get(
                    "stderr",
                    "",
                ),
            },
        )

        return self._parse_json(response)

    def correct_file(
        self,
        task: str,
        analysis: Dict[str, Any],
        architecture: Dict[str, Any],
        file_path: str,
        current_code: str,
        error_analysis: Dict[str, Any],
    ) -> str:
        """
        Generate corrected contents for a failed file.
        """

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are a senior Python debugging engineer.

Correct the provided project file.

Rules:

- Preserve the intended functionality.
- Fix the actual error.
- Maintain compatibility with the project.
- Return the COMPLETE corrected file.
- Do not use Markdown code fences.
- Do not provide explanations.
                    """,
                ),
                (
                    "human",
                    """
USER TASK:

{task}

PROJECT ANALYSIS:

{analysis}

PROJECT ARCHITECTURE:

{architecture}

FILE:

{file_path}

CURRENT CODE:

{current_code}

ERROR ANALYSIS:

{error_analysis}

Return the complete corrected file.
                    """,
                ),
            ]
        )

        return self._invoke(
            prompt,
            {
                "task": task,
                "analysis": json.dumps(
                    analysis,
                    indent=2,
                ),
                "architecture": json.dumps(
                    architecture,
                    indent=2,
                ),
                "file_path": file_path,
                "current_code": current_code,
                "error_analysis": json.dumps(
                    error_analysis,
                    indent=2,
                ),
            },
        )

    def fix_project(
        self,
        task: str,
        analysis: Dict[str, Any],
        architecture: Dict[str, Any],
        generated_project: Dict[str, Any],
        error_analysis: Dict[str, Any],
    ) -> List[str]:
        """
        Correct affected files.
        """

        fixed_files = []

        for relative_path in error_analysis.get(
            "affected_files",
            [],
        ):

            file_path = self._safe_path(
                relative_path
            )

            if not file_path.exists():
                continue

            current_code = file_path.read_text(
                encoding="utf-8"
            )

            corrected_code = self.correct_file(
                task=task,
                analysis=analysis,
                architecture=architecture,
                file_path=relative_path,
                current_code=current_code,
                error_analysis=error_analysis,
            )

            self.write_file(
                relative_path,
                corrected_code,
            )

            fixed_files.append(relative_path)

        return fixed_files


    def build_project(
        self,
        task: str,
    ) -> Dict[str, Any]:
        """
        Main entry point for the Coding Assistant.

        Example:

            result = coding_tool.build_project(
                "Create a FastAPI student management API"
            )
        """

        # -----------------------------------------------------
        # STEP 1 — Understand the requirement
        # -----------------------------------------------------

        analysis = self.analyze_task(task)

        # -----------------------------------------------------
        # STEP 2 — Design project architecture
        # -----------------------------------------------------

        architecture = self.design_project(
            task=task,
            analysis=analysis,
        )

        # -----------------------------------------------------
        # STEP 3 — Create directories
        # -----------------------------------------------------

        self.create_directories(
            architecture.get(
                "directories",
                [],
            )
        )

        # -----------------------------------------------------
        # STEP 4 — Generate project
        # -----------------------------------------------------

        generated_project = self.generate_project(
            task=task,
            analysis=analysis,
            architecture=architecture,
        )

        # -----------------------------------------------------
        # STEP 5 — Analyze project
        # -----------------------------------------------------

        project_review = self.analyze_project(
            task=task,
            analysis=analysis,
            architecture=architecture,
            generated_project=generated_project,
        )

        # -----------------------------------------------------
        # STEP 6 — Execution + correction loop
        # -----------------------------------------------------

        attempts = 0
        execution_result = None
        error_analysis = None
        fixed_files = []

        project_path = generated_project[
            "project_path"
        ]

        while attempts < MAX_ATTEMPTS:

            attempts += 1

            execution_result = self.execute_project(
                project_path=project_path,
                architecture=architecture,
            )

            # ---------------------------------------------
            # SUCCESS
            # ---------------------------------------------

            if execution_result["success"]:

                return {
                    "success": True,
                    "project_name": architecture[
                        "project_name"
                    ],
                    "project_path": project_path,
                    "task_analysis": analysis,
                    "architecture": architecture,
                    "generated_files": generated_project[
                        "files"
                    ],
                    "project_review": project_review,
                    "execution": execution_result,
                    "fixed_files": fixed_files,
                    "attempts": attempts,
                }

            # ---------------------------------------------
            # ERROR ANALYSIS
            # ---------------------------------------------

            error_analysis = self.analyze_error(
                task=task,
                project=generated_project,
                execution_result=execution_result,
            )

            # ---------------------------------------------
            # CORRECT PROJECT
            # ---------------------------------------------

            corrected = self.fix_project(
                task=task,
                analysis=analysis,
                architecture=architecture,
                generated_project=generated_project,
                error_analysis=error_analysis,
            )

            fixed_files.extend(corrected)

        # -----------------------------------------------------
        # MAXIMUM ATTEMPTS REACHED
        # -----------------------------------------------------

        return {
            "success": False,
            "project_name": architecture[
                "project_name"
            ],
            "project_path": project_path,
            "task_analysis": analysis,
            "architecture": architecture,
            "generated_files": generated_project[
                "files"
            ],
            "project_review": project_review,
            "execution": execution_result,
            "error_analysis": error_analysis,
            "fixed_files": fixed_files,
            "attempts": attempts,
            "message": (
                "Maximum correction attempts reached."
            ),
        }
