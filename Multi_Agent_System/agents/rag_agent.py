from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq

from tools.rag_tool import search_pdf


load_dotenv(Path(__file__).resolve().parents[1] / ".env")

model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


SYSTEM_PROMPT = """
You are a specialized RAG Agent.

Your responsibility is to answer questions using information
retrieved from the provided PDF document.

Rules:

1. Use the search_pdf tool whenever the user's question
   requires information from the PDF.

2. Do not invent information that is not supported by the
   retrieved document.

3. Base your answer primarily on the retrieved PDF content.

4. If the PDF does not contain relevant information, clearly
   state that the required information was not found.

5. When possible, mention the source page from the retrieved
   information.

6. Give concise but complete answers.

7. If the user asks something unrelated to the PDF, explain
   that you are the specialized RAG agent and are designed
   primarily for document-based questions.
"""

rag_agent = create_agent(
    model=model,
    tools=[search_pdf],
    system_prompt=SYSTEM_PROMPT
)



def run_rag_agent(query: str):
    """
    Run the RAG agent with a user query.

    Args:
        query: User's question.

    Returns:
        Agent response.
    """

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
if __name__ == "__main__":

    print("RAG Agent started.")
    print("Type 'exit' to quit.\n")

    while True:

        query = input("You: ")

        if query.lower() == "exit":
            print("RAG Agent stopped.")
            break

        response = run_rag_agent(query)

        print("\nRAG Agent:")
        print(response["messages"][-1].content)
        print()