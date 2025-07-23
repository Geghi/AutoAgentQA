import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    PROJECT_NAME: str = "AutoAgent QA API"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "AI-powered helpdesk agent for internal company knowledge"

    DOC_SET_NAME: str = "italian_monetary_fund" 
    # DOC_SET_NAME: str = "sample_dataset" 
    CHROMA_DB_PATH: str = f"chroma/{DOC_SET_NAME}_chroma_db"
    DOC_DATASET_PATH: str = f"data/{DOC_SET_NAME}"
    PROCESSED_HASHES_FILE: str = DOC_DATASET_PATH + "/processed_hashes.json"
    TEXT_EMBEDDING_MODEL: str = os.getenv("TEXT_EMBEDDING_MODEL", "text-embedding-3-small")
    CHAT_MODEL: str = "gpt-4.1-nano"
    RERANKER_MODEL: str = os.getenv("RERANKER_MODEL", "BAAI/bge-reranker-base")

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    SLACK_BOT_TOKEN: str = os.getenv("SLACK_BOT_TOKEN", "")
    SLACK_SIGNING_SECRET: str = os.getenv("SLACK_SIGNING_SECRET", "")
    SLACK_BOT_USER_ID: str = os.getenv("SLACK_BOT_USER_ID", "U0XXXXXXX")
    HF_AUTH_TOKEN: str = os.getenv("HF_AUTH_TOKEN", "")
    SKIP_RERANKING: bool = os.getenv("SKIP_RERANKING", "False").lower() == "true"

config = Config()
