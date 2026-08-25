from langchain_core.tools import tool

from rag.loader import load_pdf
from rag.splitter import split_documents
from rag.embeddings import create_embeddings
from rag.vector_store import create_vector_store
from rag.retriever import create_retriever


# ============================================================
# Build RAG system
# ============================================================

PDF_PATH = "Multi_Agent_System/data/documents/University_Departments_Network_Documentation.pdf"


documents = load_pdf(PDF_PATH)

chunks = split_documents(documents)

embeddings = create_embeddings()

vector_store = create_vector_store(
    chunks,
    embeddings
)

retriever = create_retriever(
    vector_store
)


# ============================================================
# RAG Tool
# ============================================================

@tool
def search_pdf(query: str) -> str:
    """
    Search the PDF for information relevant to the user's question.
    Use this tool when the user asks about information contained
    in the PDF.
    """

    docs = retriever.invoke(query)

    if not docs:

        return "No relevant information was found in the PDF."

    results = []

    for doc in docs:

        source = doc.metadata.get(
            "source",
            "Unknown"
        )

        page = doc.metadata.get(
            "page",
            "Unknown"
        )

        results.append(
            f"Source: {source}\n"
            f"Page: {page}\n"
            f"Content: {doc.page_content}"
        )

    return "\n\n".join(results)