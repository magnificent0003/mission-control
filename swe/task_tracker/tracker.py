import json
import sys
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).parent / "tasks.json"


def _load() -> list[dict[str, Any]]:
    if not DB_PATH.exists():
        return []
    return json.loads(DB_PATH.read_text(encoding="utf-8"))


def _save(tasks: list[dict[str, Any]]) -> None:
    DB_PATH.write_text(json.dumps(tasks, indent=2), encoding="utf-8")


def add_task(title: str) -> dict[str, Any]:
    title = title.strip()
    if not title:
        raise ValueError("title cannot be empty")

    tasks = _load()
    next_id = max([t["id"] for t in tasks], default=0) + 1
    task = {"id": next_id, "title": title, "done": False}
    tasks.append(task)
    _save(tasks)
    return task


def list_tasks() -> list[dict[str, Any]]:
    return _load()


def mark_done(task_id: int) -> dict[str, Any]:
    tasks = _load()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            _save(tasks)
            return t
    raise KeyError(f"task id {task_id} not found")


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: python tracker.py add \"Title\" | list | done <id>")
        return 1

    cmd = argv[1].lower()

    try:
        if cmd == "add":
            if len(argv) < 3:
                print("Missing title. Example: python tracker.py add \"Buy milk\"")
                return 1
            task = add_task(" ".join(argv[2:]))
            print(f"Added: [{task['id']}] {task['title']}")
            return 0

        if cmd == "list":
            tasks = list_tasks()
            if not tasks:
                print("No tasks yet.")
                return 0
            for t in tasks:
                status = "✅" if t["done"] else "⬜"
                print(f"{status} [{t['id']}] {t['title']}")
            return 0

        if cmd == "done":
            if len(argv) < 3:
                print("Missing id. Example: python tracker.py done 2")
                return 1
            updated = mark_done(int(argv[2]))
            print(f"Done: [{updated['id']}] {updated['title']}")
            return 0

        print(f"Unknown command: {cmd}")
        return 1

    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
