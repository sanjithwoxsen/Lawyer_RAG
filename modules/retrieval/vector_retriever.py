import os
from modules.document.vector_db import VectorStore
from modules.loggers.log_decorator import log_retrieved_docs

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

class VectorRetriever:
    @staticmethod
    @log_retrieved_docs
    def retrieve_faiss(user_question, db_names):
        """Retrieves relevant documents from multiple FAISS vector stores."""
        retrieved_docs = {}

        for db_name in db_names:
            db = VectorStore.load_VDB(db_name)
            retrieved_docs[db_name] = db.similarity_search(user_question) if db else []

        return retrieved_docs
