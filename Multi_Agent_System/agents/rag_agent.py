from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq

from tools.rag_tool import create_search_pdf_tool


load_dotenv(
    Path(__file__).resolve().parents[1] / ".env"
)


model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


SYSTEM_PROMPT = """
You are a general-purpose PDF question-answering agent.

The user has provided a PDF document for this task.

Rules:

1. Use the search_pdf tool whenever the user's question
   requires information from the uploaded PDF.

2. Answer using information retrieved from the uploaded PDF.

3. Do not invent information that is not supported by
   the uploaded PDF.

4. If the requested information cannot be found in the
   uploaded PDF, clearly say that it was not found.

5. Do not assume that the document is about any particular
   subject or organization.

6. Treat the currently uploaded PDF as the only document
   knowledge source for this task.

7. When possible, mention the source page.

8. Give concise but complete answers.
"""


def create_rag_agent(pdf_path: str):

    search_pdf = create_search_pdf_tool(pdf_path)

    return create_agent(
        model=model,
        tools=[search_pdf],
        system_prompt=SYSTEM_PROMPT
    )


def run_rag_agent(query: str, pdf_path: str):

    rag_agent = create_rag_agent(pdf_path)

    response = rag_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ]
        }
    )

    return response