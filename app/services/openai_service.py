import os
from langchain_openai import ChatOpenAI
from langchain_community.callbacks import get_openai_callback

from app.core.config import config
from app.utils.logger import logger

def get_chat_model():
    """
    Initializes and returns a ChatOpenAI instance.

    Returns:
        ChatOpenAI: An instance of the ChatOpenAI class.
    """
    llm = ChatOpenAI(
        model=config.CHAT_MODEL,
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0,
        max_tokens=1000,
    )
    return llm

def calculate_and_log_cost(cb):
    """
    Calculates and logs the cost of the OpenAI API call.
    """
    if cb:
        logger.info(f"OpenAI Call - Total Tokens: {cb.total_tokens}")
        logger.info(f"OpenAI Call - Prompt Tokens: {cb.prompt_tokens}")
        logger.info(f"OpenAI Call - Completion Tokens: {cb.completion_tokens}")
        logger.info(f"OpenAI Call - Total Cost (USD): ${cb.total_cost:.6f}")
    else:
        logger.warning("No OpenAI callback data available to log cost.")
