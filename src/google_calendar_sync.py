from __future__ import annotations

try:
    from .google_auth import GoogleAuthError, get_credentials
    from .smart_scheduler_ml import recommend_schedule
    from .task_manager import load_tasks, save_tasks
    from .task_utils import LOCAL_TIMEZONE, task_time_window
except ImportError:
    from google_auth import GoogleAuthError, get_credentials
    from smart_scheduler_ml import recommend_schedule
    from task_manager import load_tasks, save_tasks
    from task_utils import LOCAL_TIMEZONE, task_time_window


def _get_calendar_modules():
    try:
        from googleapiclient.discovery import build
        from googleapiclient.errors import HttpError
    except ImportError as exc:
        raise GoogleAuthError(
            "Google Calendar -kirjastot puuttuvat. Asenna riippuvuudet komennolla `pip install -r requirements.txt`."
        ) from exc

    return build, HttpError


def _get_calendar_service(interactive: bool = True):
    creds = get_credentials(interactive=interactive)
    if not creds:
        raise GoogleAuthError("Kirjaudu sisään Google-tilillä ennen kalenterisynkkaa.")

    build, http_error = _get_calendar_modules()
    return build("calendar", "v3", credentials=creds), http_error


def _build_calendar_event(task: dict, predicted_duration: int) -> dict:
    start_time, end_time, duration = task_time_window(task, predicted_duration)
    description_lines = [
        f"Tärkeysaste: {task['priority']}",
        f"Arvioitu kesto: {duration} min",
        f"Tila: {task['status']}",
    ]

    return {
        "summary": task["title"],
        "description": "\n".join(description_lines),
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": LOCAL_TIMEZONE,
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": LOCAL_TIMEZONE,
        },
    }


def delete_task_event(task: dict) -> bool:
    event_id = task.get("calendar_event_id")
    if not event_id:
        return False

    try:
        service, _ = _get_calendar_service(interactive=False)
        service.events().delete(calendarId="primary", eventId=event_id).execute()
    except Exception:
        return False

    return True


def sync_tasks_to_calendar() -> dict[str, int]:
    service, http_error = _get_calendar_service(interactive=True)
    tasks = load_tasks()
    created = 0
    updated = 0
    skipped = 0
    changed = False

    for task in tasks:
        if task.get("status") == "completed":
            skipped += 1
            continue

        recommendation = recommend_schedule(task)
        predicted_duration = recommendation["predicted_duration"]
        if task.get("predicted_duration") != predicted_duration:
            task["predicted_duration"] = predicted_duration
            changed = True

        event = _build_calendar_event(task, predicted_duration)

        try:
            event_id = task.get("calendar_event_id")
            if event_id:
                service.events().update(
                    calendarId="primary",
                    eventId=event_id,
                    body=event,
                ).execute()
                updated += 1
            else:
                created_event = service.events().insert(calendarId="primary", body=event).execute()
                task["calendar_event_id"] = created_event["id"]
                created += 1
                changed = True

            if task.pop("sync_error", None):
                changed = True
        except http_error as exc:
            status_code = getattr(getattr(exc, "resp", None), "status", None)
            task["sync_error"] = str(exc)
            if status_code == 404 and task.get("calendar_event_id"):
                task.pop("calendar_event_id", None)
            changed = True
        except Exception as exc:
            task["sync_error"] = str(exc)
            changed = True

    if changed:
        save_tasks(tasks)

    return {"created": created, "updated": updated, "skipped": skipped}
