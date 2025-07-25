from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from typing import List
from langchain.docstore.document import Document
from app.core.config import config

def load_documents(path: str = config.DOC_DATASET_PATH, glob: str = "**/*") -> List[Document]:
    """
    Load documents from a directory.

    Args:
        path (str): The path to the directory containing the documents.
        glob (str): The glob pattern to match files.

    Returns:
        List[Document]: A list of loaded documents.
    """
    # Define a dictionary of loaders based on file extension
    loader_mapping = {
        ".txt": TextLoader,
        ".pdf": PyPDFLoader,
    }

    loaded_documents = []
    for ext, loader_cls in loader_mapping.items():
        current_glob = f"**/*{ext}"
        loader = DirectoryLoader(
            path,
            glob=current_glob,
            loader_cls=loader_cls,
            loader_kwargs={"encoding": "utf-8"} if ext == ".txt" else {}
        )
        loaded_documents.extend(loader.load())

    # Group documents by source and combine content for PDFs
    combined_documents = {}
    for doc in loaded_documents:
        source = doc.metadata.get('source')
        if source:
            if source not in combined_documents:
                combined_documents[source] = {
                    'page_content': [],
                    'metadata': doc.metadata
                }
            combined_documents[source]['page_content'].append(doc.page_content)

    final_documents = []
    for source, data in combined_documents.items():
        full_content = "\n".join(data['page_content'])
        final_documents.append(Document(page_content=full_content, metadata=data['metadata']))
    
    return final_documents
