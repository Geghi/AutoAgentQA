from langchain_openai import OpenAIEmbeddings
import os

def get_embedding_function():
    """
    Initializes and returns an OpenAIEmbeddings instance.

    Returns:
        OpenAIEmbeddings: An instance of the OpenAIEmbeddings class.
    """
    return OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
