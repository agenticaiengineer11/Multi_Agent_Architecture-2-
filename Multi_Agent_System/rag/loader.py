from pathlib import Path

from pypdf import PdfReader
from langchain_core.documents import Document


def load_pdf(pdf_path: str) -> list[Document]:
    """
    Load a PDF and convert each page into a LangChain Document.
    """

    reader = PdfReader(pdf_path)

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""

        if text.strip():

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": Path(pdf_path).name,
                        "page": page_number
                    }
                )
            )

    if not documents:
        raise ValueError(
            "No text could be extracted from the PDF."
        )

    return documents