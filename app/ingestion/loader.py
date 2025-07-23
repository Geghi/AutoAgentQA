from langchain_community.document_loaders import DirectoryLoader, TextLoader
from typing import List
from langchain.docstore.document import Document

def load_documents(path: str = "data/", glob: str = "**/*.txt") -> List[Document]:
    """
    Load documents from a directory.

    Args:
        path (str): The path to the directory containing the documents.
        glob (str): The glob pattern to match files.

    Returns:
        List[Document]: A list of loaded documents.
    """
    loader = DirectoryLoader(path, glob=glob, loader_cls=TextLoader)
    documents = loader.load()
    return documents
