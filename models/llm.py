# LLM models (OpenAI / Groq / Gemini)

# models/llm.py

from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain.chat_models import ChatOpenAI

from config.config import GROQ_API_KEY

def get_llm(model_name, temperature):
    """Returns an LLM based on the model name."""
    if "llama" in model_name.lower() or "mixtral" in model_name.lower():
        return ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name=model_name,
            temperature=temperature
        )
    elif "gpt" in model_name.lower():
        # Assuming OPENAI_API_KEY is still available or handled elsewhere if needed
        # For now, we'll use a placeholder or assume it's imported if necessary
        # from config.config import OPENAI_API_KEY # Uncomment if you need OpenAI
        return ChatOpenAI(
            # openai_api_key=OPENAI_API_KEY, # Uncomment if you need OpenAI
            model_name=model_name,
            temperature=temperature
        )
    else:
        raise ValueError(f"Unsupported LLM model: {model_name}")

def build_qa_chain(vectorstore, model_name="llama3-8b-8192", temperature=0.3):
    """
    Builds a RetrievalQA chain using LLM + vectorstore retriever.
    
    Args:
        vectorstore: FAISS vectorstore
        model_name: which LLM to use
        temperature: LLM creativity
    
    Returns:
        qa_chain: RetrievalQA pipeline
    """
    llm = get_llm(model_name, temperature)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",  # can also be "map_reduce" for longer texts
        return_source_documents=True
    )
    return qa_chain