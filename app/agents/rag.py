from typing import List, Tuple
from langchain_core.documents import Document
import time
from app.core.config import config
from app.utils.logger import logger
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_chroma import Chroma
from app.ingestion.embeddings import get_embedding_function
from app.prompts.chat_response_prompt import CHAT_RESPONSE_SYSTEM_PROMPT, CHAT_RESPONSE_USER_PROMPT
from app.services.openai_service import get_chat_model
from sentence_transformers import CrossEncoder

# Global or cached reranker model (load once)
reranker_model = None

def load_reranker_model():
    global reranker_model
    if reranker_model is None:
        logger.info(f"Loading {config.RERANKER_MODEL} model...")
        reranker_model = CrossEncoder(config.RERANKER_MODEL, token=config.HF_AUTH_TOKEN if config.HF_AUTH_TOKEN else None)
        logger.info(f"{config.RERANKER_MODEL} model loaded.")
    return reranker_model

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
        persist_directory=config.CHROMA_DB_PATH,
        embedding_function=get_embedding_function()
    )
    
    prompt = ChatPromptTemplate.from_messages(
        [CHAT_RESPONSE_SYSTEM_PROMPT, CHAT_RESPONSE_USER_PROMPT]
    )
    
    llm = get_chat_model()
    
    def retrieve_and_rerank(question: str) -> List[Tuple[Document, float]]:
        """
        Retrieves and optionally reranks documents based on the SKIP_RERANKING flag.
        """
        start_time = time.time()

        if config.SKIP_RERANKING:
            logger.info(f"Retrieval (No Reranking) Started...")
            # Skip reranking, retrieve top 5 directly
            top_docs_with_scores = vectorstore.similarity_search_with_score(question, k=config.TOP_K_NO_RERANK)
            logger.info(f"Retrieval (no reranking) time: {time.time() - start_time:.4f} seconds")
            for doc, score in top_docs_with_scores:
                print(f"Source: {doc.metadata.get('source', 'N/A')}, Score: {score:.4f}")
            return top_docs_with_scores
        else:
            logger.info(f"Retrieval With Reranking Started...")
            # Load the reranker model
            reranker = load_reranker_model()
            # 1. Initial retrieval of a larger set (e.g., 20 documents)
            initial_docs_with_scores = vectorstore.similarity_search_with_score(question, k=config.TOP_K_WITH_RERANK)
            logger.info(f"Initial Retrieval time: {time.time() - start_time:.4f} seconds")

            initial_docs = [doc for doc, _ in initial_docs_with_scores]

            # Prepare pairs for reranking: (query, document_content)
            sentence_pairs = [[question, doc.page_content] for doc in initial_docs]

            logger.info(f"Reranking Step Started...")
            # 2. Rerank the initial set
            # The reranker returns scores for each pair
            rerank_scores = reranker.predict(sentence_pairs)

            # Combine documents with their rerank scores
            docs_with_rerank_scores = sorted(
                zip(initial_docs, rerank_scores),
                key=lambda x: x[1],
                reverse=True
            )

            # Select the top N documents after reranking (e.g., top 5)
            top_n_reranked_docs_with_scores = docs_with_rerank_scores[:5]

            logger.info(f"Retrieval and Reranking total time: {time.time() - start_time:.4f} seconds")
            for doc, score in top_n_reranked_docs_with_scores:
                print(f"Source: {doc.metadata.get('source', 'N/A')}, Rerank Score: {score:.4f}")

            return top_n_reranked_docs_with_scores

    retriever = RunnableLambda(retrieve_and_rerank)

    rag_chain_from_docs = (
        RunnablePassthrough.assign(
            context=(lambda x: format_docs_with_scores(x["retrieved_docs"]))
        )
        | prompt
        | llm
    )

    rag_chain = (
        {
            "retrieved_docs": retriever,
            "question": RunnablePassthrough(),
        }
        | RunnablePassthrough.assign(answer=rag_chain_from_docs)
    )
    return rag_chain

def rag_pipeline(query: str) -> dict:
    """
    Executes the RAG pipeline for a given query and returns the answer with groundings.

    Args:
        query: The user's query.

    Returns:
        A dictionary containing the generated answer and a list of source documents.
    """
    start_time = time.time()
    rag_chain = get_rag_chain()
    result = rag_chain.invoke(query)
    logger.info(f"Total RAG pipeline time: {time.time() - start_time:.4f} seconds")
    
    answer = result["answer"].content
    
    retrieved_docs = result.get('retrieved_docs', [])

    groundings = []
    if retrieved_docs:
        for doc, _ in retrieved_docs:
            source = doc.metadata.get('source', 'N/A')
            groundings.append(source)
    
    # Use set to get unique sources and sort them
    unique_groundings = sorted(list(set(groundings)))

    return {
        "answer": answer,
        "groundings": unique_groundings
    }
