from pathlib import Path

from langchain_core.tools import tool

from rag.loader import load_pdf
from rag.splitter import split_documents
from rag.embeddings import create_embeddings
from rag.vector_store import create_vector_store
from rag.retriever import create_retriever


def build_retriever(pdf_path: str):
    """
    Build a RAG retriever dynamically from the PDF
    provided by the current user/session.
    """

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {pdf_path}"
        )

    documents = load_pdf(str(pdf_path))

    chunks = split_documents(documents)

    embeddings = create_embeddings()

    vector_store = create_vector_store(
        chunks,
        embeddings
    )

    return create_retriever(vector_store)


def create_search_pdf_tool(pdf_path: str):
    """
    Create a search_pdf tool connected specifically
    to the user's uploaded PDF.
    """

    retriever = build_retriever(pdf_path)

    @tool
    def search_pdf(query: str) -> str:
        """
        Search the user's uploaded PDF for information
        relevant to the user's question.
        """

        docs = retriever.invoke(query)

        if not docs:
            return (
                "No relevant information was found "
                "in the uploaded PDF."
            )

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

    return search_pdf