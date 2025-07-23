from langchain_openai import OpenAIEmbeddings
import os
from app.core.config import config

def get_embedding_function():
    """
    Initializes and returns an OpenAIEmbeddings instance.

    Returns:
        OpenAIEmbeddings: An instance of the OpenAIEmbeddings class.
    """
    return OpenAIEmbeddings(model=config.TEXT_EMBEDDING_MODEL, api_key=config.OPENAI_API_KEY)
