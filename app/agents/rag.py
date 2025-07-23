from typing import List, Tuple
from langchain_core.documents import Document
import time
from app.utils.logger import logger
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_chroma import Chroma
from app.ingestion.embeddings import get_embedding_function
from app.prompts.chat_response_prompt import CHAT_RESPONSE_SYSTEM_PROMPT, CHAT_RESPONSE_USER_PROMPT
from app.services.openai_service import get_chat_model

def format_docs_with_scores(docs_with_scores: List[Tuple[Document, float]]) -> str:
    """
    Formats a list of documents with their similarity scores into a single string.

    Args:
        docs_with_scores: A list of tuples, each containing a Document object and its similarity score.

    Returns:
        A string containing the formatted documents with scores.
    """
    formatted_strings = []
    for doc, score in docs_with_scores:
        source = doc.metadata.get('source', 'N/A')
        formatted_strings.append(f"Content from {source}:\n{doc.page_content}")
    return "\n\n".join(formatted_strings)

def get_rag_chain():
    """
    Initializes and returns a RAG chain.

    Returns:
        A RAG chain.
    """
    vectorstore = Chroma(
        persist_directory="chroma/chroma",
        embedding_function=get_embedding_function()
    )
    
    prompt = ChatPromptTemplate.from_messages(
        [CHAT_RESPONSE_SYSTEM_PROMPT, CHAT_RESPONSE_USER_PROMPT]
    )
    
    llm = get_chat_model()
    
    def retrieve_and_score(question: str) -> List[Tuple[Document, float]]:
        """
        Retrieves documents with similarity scores.
        """
        start_time = time.time()
        docs_with_scores = vectorstore.similarity_search_with_score(question)
        logger.info(f"Retrieval time: {time.time() - start_time:.4f} seconds")
        print("\n--- Retrieved Documents with Scores ---")
        for doc, score in docs_with_scores:
            print(f"Source: {doc.metadata.get('source', 'N/A')}, Score: {score:.4f}")
        print("--- End Retrieved Documents with Scores ---\n")
        return docs_with_scores

    rag_chain = (
        RunnablePassthrough.assign(
            context=(lambda x: x["question"]) | RunnableLambda(retrieve_and_score) | format_docs_with_scores
        )
        | prompt
        # | (lambda x: print(f"--- Final Prompt ---\n{x.messages}\n--- End Prompt ---") or x)
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
    start_time = time.time()
    rag_chain = get_rag_chain()
    result = rag_chain.invoke({"question": query})
    logger.info(f"Total RAG pipeline time: {time.time() - start_time:.4f} seconds")
    return result.content
