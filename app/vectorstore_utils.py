from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from typing import List

def create_faiss_index(documents: List[str]) -> FAISS:
    """
    Creates a FAISS index from a list of documents.

    Args:
        documents (List[str]): A list of text documents to be indexed.

    Returns:
        FAISS: A FAISS index containing the vector representations of the documents.
    """
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    faiss_index = FAISS.from_texts(documents, embeddings)
    return faiss_index

def retrive_relevant_docs(faiss_index: FAISS, query: str, k: int = 4):
    """
    Retrieves the most relevant documents from the FAISS index based on a query.

    Args:
        faiss_index (FAISS): The FAISS index to search.
        query (str): The query string to search for relevant documents.
        k (int): The number of top relevant documents to retrieve. Default is 4.

    """
    return faiss_index.similarity_search(query, k=k)

