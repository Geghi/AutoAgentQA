import os
import sys
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ingestion.loader import load_documents
from app.ingestion.splitter import chunk_documents
from app.ingestion.embeddings import get_embedding_function
from app.ingestion.index import (
    filter_new_documents,
    create_and_persist_chroma_index,
    get_processed_hashes,
    save_processed_hashes,
)

# Load environment variables from .env file
load_dotenv()

def main():
    """
    Main function to run the document ingestion process.
    """
    print("Starting document ingestion...")

    # 1. Load documents
    documents = load_documents()
    if not documents:
        print("No documents found to process.")
        return

    print(f"Loaded {len(documents)} documents.")
    
    # 2. Filter for new documents
    new_documents, new_hashes = filter_new_documents(documents)
    if not new_documents:
        print("No new documents to process.")
        return

    print(f"Found {len(new_documents)} new documents to process.")

    # 3. Chunk the new documents
    chunks = chunk_documents(new_documents)
    if not chunks:
        print("No chunks were created from the new documents.")
        return

    # 4. Get the embedding function
    embedding_fn = get_embedding_function()

    # 5. Create and persist the Chroma index
    create_and_persist_chroma_index(chunks, embedding_fn)

    # 6. Update the processed hashes file
    all_hashes = get_processed_hashes().union(new_hashes)
    save_processed_hashes(all_hashes)

    print("Document ingestion process completed successfully.")

if __name__ == "__main__":
    main()
