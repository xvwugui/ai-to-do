import json
from pathlib import Path
from typing import List, Dict, Any

DB_PATH = Path.home() / ".ai_todo_db.json"

def read_tasks() -> List[Dict[str, Any]]:
    if not DB_PATH.is_file():
        return []
    with DB_PATH.open("r") as f:
        try:
            tasks = json.load(f)
            return tasks
        except json.JSONDecoderError:
            return []

def write_tasks(tasks : List[Dict[str, Any]]):
    with DB_PATH.open("w") as f:
        json.dump(tasks, f, indent = 4)

def reindex_tasks(tasks : List[Dict[str,Any]]) -> List[Dict[str,Any]]:
    for new_id, task in enumerate(tasks, start=1):
        task["id"] = new_id
    return tasks
