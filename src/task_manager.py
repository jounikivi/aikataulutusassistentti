from __future__ import annotations

import json
from pathlib import Path

try:
    from .google_auth import get_current_user_email
    from .task_utils import normalize_task
except ImportError:
    from google_auth import get_current_user_email
    from task_utils import normalize_task

LEGACY_TASK_FILE = Path("tasks.json")
DEFAULT_TASK_FILE = Path("tasks_default_user.json")


def _sanitize_email(email: str) -> str:
    return email.replace("@", "_").replace(".", "_")


def get_user_task_file(email: str | None = None) -> Path:
    active_email = (email or get_current_user_email()).strip() or "default_user"
    return Path(f"tasks_{_sanitize_email(active_email)}.json")


def _find_existing_task_file(target_file: Path) -> Path:
    if target_file.exists():
        return target_file

    candidates: list[Path] = []
    if target_file.name != DEFAULT_TASK_FILE.name:
        candidates.extend([DEFAULT_TASK_FILE, LEGACY_TASK_FILE])
    else:
        candidates.append(LEGACY_TASK_FILE)

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return target_file


def _load_normalized_tasks(path: Path) -> list[dict]:
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return []

    if not isinstance(data, list):
        return []

    tasks = []
    for item in data:
        if not isinstance(item, dict):
            continue
        try:
            tasks.append(normalize_task(item))
        except (TypeError, ValueError):
            continue
    return tasks


def load_tasks() -> list[dict]:
    target_file = get_user_task_file()
    source_file = _find_existing_task_file(target_file)
    tasks = _load_normalized_tasks(source_file)

    if tasks and source_file != target_file:
        save_tasks(tasks)

    return tasks


def save_tasks(tasks: list[dict]) -> None:
    normalized_tasks = []
    for task in tasks:
        if not isinstance(task, dict):
            continue
        normalized_tasks.append(normalize_task(task))

    target_file = get_user_task_file()
    with target_file.open("w", encoding="utf-8") as handle:
        json.dump(normalized_tasks, handle, ensure_ascii=False, indent=2)
