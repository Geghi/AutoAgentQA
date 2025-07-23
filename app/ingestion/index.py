import hashlib
import json
import os
from typing import List, Set, Tuple
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma
from langchain.embeddings.base import Embeddings
from app.core.config import config

PROCESSED_HASHES_FILE = "data/processed_hashes.json"

def get_processed_hashes() -> Set[str]:
    """
    Loads the set of processed document hashes from the JSON file.
    """
    if not os.path.exists(PROCESSED_HASHES_FILE):
        return set()
    with open(PROCESSED_HASHES_FILE, "r") as f:
        try:
            return set(json.load(f))
        except json.JSONDecodeError:
            return set()

def save_processed_hashes(hashes: Set[str]):
    """
    Saves the set of processed hashes to the JSON file.
    """
    with open(PROCESSED_HASHES_FILE, "w") as f:
        json.dump(list(hashes), f, indent=4)

def filter_new_documents(documents: List[Document]) -> Tuple[List[Document], Set[str]]:
    """
    Filters a list of documents, returning only the new ones.

    Args:
        documents (List[Document]): The list of documents to filter.

    Returns:
        Tuple[List[Document], Set[str]]: A tuple containing the list of new documents and the set of their hashes.
    """
    processed_hashes = get_processed_hashes()
    new_documents = []
    new_hashes = set()

    for doc in documents:
        hash_input = doc.page_content + str(doc.metadata.get('source', ''))
        doc_hash = hashlib.md5(hash_input.encode()).hexdigest()
        if doc_hash not in processed_hashes:
            new_documents.append(doc)
            new_hashes.add(doc_hash)
            
    return new_documents, new_hashes

def create_and_persist_chroma_index(chunks: List[Document], embedding_fn: Embeddings):
    """
    Creates and persists a Chroma index from document chunks.

    Args:
        chunks (List[Document]): A list of document chunks to be indexed.
        embedding_fn (Embeddings): The embedding function to use.
    """
    if not chunks:
        print("No new chunks to add to the index.")
        return

    chroma = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_fn,
        persist_directory=config.CHROMA_DB_PATH
    )
    print(f"Added {len(chunks)} new chunks to the index.")
