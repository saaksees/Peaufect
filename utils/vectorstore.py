# utils/vectorstore.py

from langchain.vectorstores import FAISS
from models.embeddings import get_embedding_model

def build_vectorstore(docs, provider="huggingface"):
    """
    Builds and returns a FAISS vectorstore from a list of documents.
    
    Args:
        docs: List of documents to embed.
        provider: Embedding provider to use (e.g., "huggingface").
    
    Returns:
        FAISS vectorstore.
    """
    embeddings = get_embedding_model(provider)
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore


def get_retriever(vectorstore, k=3):
    """
    Returns a retriever from the vectorstore.
    
    Args:
        vectorstore (FAISS): FAISS vector database.
        k (int): Number of top results to return.
    
    Returns:
        retriever: Retriever object.
    """
    return vectorstore.as_retriever(search_kwargs={"k": k})
