from typing import List
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma
from app.ingestion.embeddings import get_embedding_function
from app.prompts.chat_response_prompt import CHAT_RESPONSE_SYSTEM_PROMPT, CHAT_RESPONSE_USER_PROMPT
from app.services.openai_service import get_chat_model

def format_docs(docs: List[Document]) -> str:
    """
    Formats a list of documents into a single string.

    Args:
        docs: A list of Document objects.

    Returns:
        A string containing the formatted documents.
    """
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain():
    """
    Initializes and returns a RAG chain.

    Returns:
        A RAG chain.
    """
    vectorstore = Chroma(
        persist_directory="chroma/",
        embedding_function=get_embedding_function()
    )
    retriever = vectorstore.as_retriever()
    
    prompt = ChatPromptTemplate.from_messages(
        [CHAT_RESPONSE_SYSTEM_PROMPT, CHAT_RESPONSE_USER_PROMPT]
    )
    
    llm = get_chat_model()
    
    rag_chain = (
        RunnablePassthrough.assign(
            context=(lambda x: x["question"]) | retriever | format_docs
        )
        | prompt
        | (lambda x: print(f"--- Final Prompt ---\n{x.messages}\n--- End Prompt ---") or x)
        | llm
    )
    return rag_chain

def rag_pipeline(query: str) -> str:
    """
    Executes the RAG pipeline for a given query.

    Args:
        query: The user's query.

    Returns:
        The generated answer.
    """
    rag_chain = get_rag_chain()
    result = rag_chain.invoke({"question": query})
    return result.content
