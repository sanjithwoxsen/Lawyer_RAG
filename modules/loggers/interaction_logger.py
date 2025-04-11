import json
import os
from datetime import datetime

LOG_FILE = "logs/interactions.json"

# Ensure log directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log_interaction(model_type: str, model_name: str, question: str, answer: str):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "model_type": model_type,
        "model_name": model_name,
        "question": question,
        "answer": answer
    }

    # Append the entry as a JSON line
    with open(LOG_FILE, "a") as f:
        json.dump(log_entry, f , indent=4, ensure_ascii=False)
        f.write(",\n")
