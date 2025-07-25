import os
from langchain_openai import ChatOpenAI

from app.core.config import config

def get_chat_model():
    """
    Initializes and returns a ChatOpenAI instance.

    Returns:
        ChatOpenAI: An instance of the ChatOpenAI class.
    """
    return ChatOpenAI(
        model=config.CHAT_MODEL,
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0,
        max_tokens=1000,
    )
