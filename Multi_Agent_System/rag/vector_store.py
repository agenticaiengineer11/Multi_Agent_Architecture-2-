from langchain_chroma import Chroma


def create_vector_store(documents, embeddings):

    return Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name="multi_agent_rag"
    )