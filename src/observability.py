import json
import os
from datetime import datetime

LOGS_FOLDER = "logs"
LOG_FILE = os.path.join(LOGS_FOLDER, "rag_log.jsonl")


def log_event(data):
    os.makedirs(LOGS_FOLDER, exist_ok=True)
    data["timestamp"] = datetime.now().isoformat(timespec="seconds")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    log_event({"question": "test", "answer": "it worked"})
    print(f"Log written to {LOG_FILE}")
