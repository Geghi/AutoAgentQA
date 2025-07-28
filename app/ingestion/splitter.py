from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.docstore.document import Document

def chunk_documents(documents: List[Document]) -> List[Document]:
    """
    Splits the documents into chunks.

    Args:
        documents (List[Document]): The documents to be chunked.

    Returns:
        List[Document]: A list of chunked documents.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200,
        add_start_index=True,
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = splitter.split_documents(documents)
    return chunks
