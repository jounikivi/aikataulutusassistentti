from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

DATE_FORMAT = "%Y-%m-%d %H:%M"
LOCAL_TIMEZONE = "Europe/Helsinki"
LOCAL_ZONEINFO = ZoneInfo(LOCAL_TIMEZONE)
DEFAULT_DURATION_MINUTES = 30
DEFAULT_PRIORITY = 3
VALID_STATUSES = {"pending", "completed"}


def clamp_int(value: Any, default: int, minimum: int, maximum: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return max(minimum, min(maximum, parsed))


def parse_deadline(value: str) -> datetime:
    return datetime.strptime(value.strip(), DATE_FORMAT)


def format_deadline(value: datetime) -> str:
    return value.strftime(DATE_FORMAT)


def normalize_status(value: Any) -> str:
    status = str(value or "pending").strip().lower()
    if status not in VALID_STATUSES:
        return "pending"
    return status


def normalize_priority(value: Any) -> int:
    return clamp_int(value, DEFAULT_PRIORITY, 1, 5)


def normalize_duration(value: Any) -> int:
    return clamp_int(value, DEFAULT_DURATION_MINUTES, 15, 480)


def normalize_task(task: dict[str, Any]) -> dict[str, Any]:
    title = str(task.get("title", "")).strip()
    if not title:
        raise ValueError("Task title is required.")

    deadline = format_deadline(parse_deadline(str(task.get("deadline", "")).strip()))
    priority = normalize_priority(task.get("priority", DEFAULT_PRIORITY))
    estimated_duration = normalize_duration(
        task.get("estimated_duration", task.get("duration", DEFAULT_DURATION_MINUTES))
    )

    normalized: dict[str, Any] = {
        "title": title,
        "deadline": deadline,
        "priority": priority,
        "estimated_duration": estimated_duration,
        "difficulty": clamp_int(task.get("difficulty", priority), priority, 1, 5),
        "status": normalize_status(task.get("status", "pending")),
    }

    if task.get("calendar_event_id"):
        normalized["calendar_event_id"] = str(task["calendar_event_id"]).strip()

    if task.get("predicted_duration") is not None:
        normalized["predicted_duration"] = normalize_duration(task.get("predicted_duration"))

    if task.get("sync_error"):
        normalized["sync_error"] = str(task["sync_error"]).strip()

    return normalized


def build_prediction_context(
    task: dict[str, Any], reference_time: datetime | None = None
) -> dict[str, int]:
    deadline_dt = parse_deadline(task["deadline"])
    now = reference_time or datetime.now()
    deadline_days = max(0, (deadline_dt.date() - now.date()).days)

    return {
        "difficulty": clamp_int(task.get("difficulty", task["priority"]), task["priority"], 1, 5),
        "priority": normalize_priority(task["priority"]),
        "deadline_days": deadline_days,
        "start_hour": deadline_dt.hour,
        "day_of_week": deadline_dt.weekday(),
        "estimated_by_user": normalize_duration(
            task.get("estimated_duration", task.get("duration", DEFAULT_DURATION_MINUTES))
        ),
    }


def task_time_window(
    task: dict[str, Any], duration_minutes: int | None = None
) -> tuple[datetime, datetime, int]:
    duration = normalize_duration(
        duration_minutes
        if duration_minutes is not None
        else task.get("predicted_duration", task.get("estimated_duration", DEFAULT_DURATION_MINUTES))
    )
    deadline_dt = parse_deadline(task["deadline"]).replace(tzinfo=LOCAL_ZONEINFO)
    start_time = deadline_dt - timedelta(minutes=duration)
    return start_time, deadline_dt, duration
