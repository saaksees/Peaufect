# models/embeddings.py

from langchain.embeddings import HuggingFaceEmbeddings

# Added a comment to force module refresh

def get_embedding_model(provider="huggingface"):
    """
    Returns an embedding model instance.
    Currently supports: HuggingFace.
    """
    if provider == "huggingface":
        # Example: "sentence-transformers/all-MiniLM-L6-v2"
        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    else:
        raise ValueError("Unsupported embedding provider. Only 'huggingface' is supported.")
