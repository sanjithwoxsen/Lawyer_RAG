import os
import shutil

class Cleanup:
    @staticmethod
    def clear_vector_store(db_name):
        """Clears a specific FAISS vector store by deleting the stored index."""
        directory = f"vector_store/{db_name}"

        try:
            if os.path.exists(directory):
                shutil.rmtree(directory)
                print(f"Deleted FAISS index at: {directory}")
            else:
                print(f"No index found at: {directory}")
        except Exception as e:
            print(f"Error deleting {directory}: {e}")
            return False

        return True
