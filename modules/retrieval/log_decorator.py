import logging
import datetime
import os
import json
from functools import wraps

# Configure logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, "retrieval_log.txt"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_retrieved_docs(func):
    """Decorator to log retrieved documents from multiple FAISS vector stores."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)  # Call the original function
        user_question = args[0]  # Extract the user question
        retrieved_docs = result  # The function returns a dictionary of retrieved documents

        log_data = {
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "question": user_question,
            "retrieved_docs": {}
        }

        for db_name, docs in retrieved_docs.items():
            if docs:
                log_data["retrieved_docs"][db_name] = [doc.page_content for doc in docs]
            else:
                log_data["retrieved_docs"][db_name] = "No relevant documents found."

            # Log separately for each DB
            with open(os.path.join(log_dir, f"{db_name}_retrieval_log.txt"), "a") as file:
                file.write(f"\n[{log_data['time']}] Question: {user_question}\n")
                if docs:
                    for i, doc in enumerate(docs, start=1):
                        file.write(f"Document {i}: {doc.page_content}\n")
                else:
                    file.write("No relevant documents found.\n")

        # Log full output in JSON format for easier debugging
        with open(os.path.join(log_dir, "retrieval_summary.json"), "a") as json_file:
            json.dump(log_data, json_file, indent=4)
            json_file.write(",\n")

        return result

    return wrapper
