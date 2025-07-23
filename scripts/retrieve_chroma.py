# scripts/retrieve_chroma.py
import argparse
from typing import List, Optional

from langchain_chroma import Chroma  # Updated import
from langchain_core.documents import Document
from chromadb.config import Settings

def retrieve_chroma_elements(filter_query: Optional[str] = None) -> List[Document]:
    """
    Retrieves all elements from the Chroma database, with an optional filter.

    Args:
        filter_query: An optional filter query string.

    Returns:
        A list of Document objects.
    """
    try:
        db = Chroma(persist_directory="chroma/chroma")
        results = db.get()
        documents = [Document(page_content=doc, metadata={}) for doc in results['documents']]
        if filter_query:
            documents = [doc for doc in documents if filter_query in doc.page_content]
        return documents
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def main():
    parser = argparse.ArgumentParser(description="Retrieve elements from Chroma DB.")
    parser.add_argument(
        "--filter", type=str, help="Filter query string (e.g., 'test')"
    )
    args = parser.parse_args()

    elements = retrieve_chroma_elements(args.filter)

    if elements:
        print("Retrieved elements:")
        for element in elements:
            print(f"  Content: {element.page_content}")
            print(f"  Metadata: {element.metadata}")
            print("-" * 20)
    else:
        print("No elements found or an error occurred.")


if __name__ == "__main__":
    main()
