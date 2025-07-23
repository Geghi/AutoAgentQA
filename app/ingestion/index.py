import hashlib
import json
import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Set, Tuple
from langchain.docstore.document import Document
from langchain_chroma import Chroma
from langchain.embeddings.base import Embeddings
from app.core.config import config
from app.ingestion.embeddings import get_embedding_function


def get_processed_hashes() -> Set[str]:
    """
    Loads the set of processed document hashes from the JSON file.
    """
    if not os.path.exists(config.PROCESSED_HASHES_FILE):
        return set()
    with open(config.PROCESSED_HASHES_FILE, "r") as f:
        try:
            return set(json.load(f))
        except json.JSONDecodeError:
            return set()

def save_processed_hashes(hashes: Set[str]):
    """
    Saves the set of processed hashes to the JSON file.
    """
    with open(config.PROCESSED_HASHES_FILE, "w") as f:
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

def get_document_names() -> List[str]:
    """
    Retrieves a list of unique document names (sources) from the Chroma index.
    """
    embedding_fn = get_embedding_function()
    chroma_client = Chroma(
        persist_directory=config.CHROMA_DB_PATH,
        embedding_function=embedding_fn
    )
    
    # Retrieve all documents, including their metadata
    results = chroma_client.get(include=['metadatas'])
    
    document_sources = set()
    for metadata in results.get('metadatas', []):
        if 'source' in metadata:
            document_sources.add(metadata['source'])
    return list(document_sources)

async def delete_documents_by_name(document_names: List[str]) -> int:
    """
    Deletes documents from the Chroma index based on their source names.

    Args:
        document_names (List[str]): A list of document source names to delete.

    Returns:
        int: The number of chunks deleted.
    """
    embedding_fn = get_embedding_function()
    chroma_client = Chroma(
        persist_directory=config.CHROMA_DB_PATH,
        embedding_function=embedding_fn
    )
    deleted_count = 0
    for name in document_names:
        # Find IDs of documents with the matching source
        results = chroma_client.get(where={"source": name}, include=['ids'])
        ids_to_delete = results.get('ids', [])
        if ids_to_delete:
            chroma_client.delete(ids=ids_to_delete)
            deleted_count += len(ids_to_delete)
            print(f"Deleted {len(ids_to_delete)} chunks for document: {name}")
    return deleted_count

