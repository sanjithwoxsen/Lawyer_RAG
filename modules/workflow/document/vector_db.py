import os
import logging
from langchain.vectorstores import FAISS
from modules.workflow.document.embeddings import embeddings

class VectorStore:
    @staticmethod
    def store_VDB(db_name, text_chunks):
        """Stores text chunks as vector embeddings using FAISS."""
        if not text_chunks:
            logging.warning(f"No text chunks provided for {db_name} storage.")
            return False

        if embeddings is None:
            logging.error("Embeddings model is not initialized. Cannot store vectors.")
            return False

        try:
            vector_store = FAISS.from_texts(text_chunks, embeddings)
            os.makedirs(f"vector_store/{db_name}", exist_ok=True)
            vector_store.save_local(f"vector_store/{db_name}/faiss_index")
            return True
        except Exception as e:
            logging.error(f"Error storing {db_name}: {e}")
            return False

    @staticmethod
    def load_VDB(db_name):
        """Loads the FAISS vector store."""
        if embeddings is None:
            logging.error(f"Embeddings model is not initialized. Cannot load {db_name}.")
            return None

        try:
            return FAISS.load_local(f"vector_store/{db_name}/faiss_index", embeddings, allow_dangerous_deserialization=True)
        except Exception as e:
            logging.error(f"Error loading {db_name}: {e}")
            return None
