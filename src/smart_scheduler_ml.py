from __future__ import annotations

import csv
import json
import pickle
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

try:
    from .task_utils import (
        DEFAULT_DURATION_MINUTES,
        build_prediction_context,
        clamp_int,
        format_deadline,
        normalize_task,
        parse_deadline,
        task_time_window,
    )
except ImportError:
    from task_utils import (
        DEFAULT_DURATION_MINUTES,
        build_prediction_context,
        clamp_int,
        format_deadline,
        normalize_task,
        parse_deadline,
        task_time_window,
    )

MODEL_FILE = Path("model.pkl")
DATASET_FILE = Path("opetusdata_ai_kalenteri.csv")
MODEL_VERSION = 2


def _read_csv_samples(dataset_path: Path) -> list[dict[str, int]]:
    if not dataset_path.exists():
        return []

    samples: list[dict[str, int]] = []
    with dataset_path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            samples.append(
                {
                    "difficulty": clamp_int(row.get("difficulty"), 3, 1, 5),
                    "priority": clamp_int(row.get("priority"), 3, 1, 5),
                    "deadline_days": clamp_int(row.get("deadline_days"), 1, 0, 365),
                    "start_hour": clamp_int(row.get("start_hour"), 12, 0, 23),
                    "day_of_week": clamp_int(row.get("day_of_week"), 0, 0, 6),
                    "estimated_by_user": clamp_int(
                        row.get("estimated_by_user"), DEFAULT_DURATION_MINUTES, 15, 480
                    ),
                    "duration_minutes": clamp_int(
                        row.get("duration_minutes"), DEFAULT_DURATION_MINUTES, 15, 480
                    ),
                }
            )
    return samples


def _read_task_history_samples() -> list[dict[str, int]]:
    samples: list[dict[str, int]] = []
    for path in sorted(Path(".").glob("tasks*.json")):
        try:
            with path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (OSError, json.JSONDecodeError):
            continue

        if not isinstance(data, list):
            continue

        for item in data:
            if not isinstance(item, dict):
                continue
            try:
                task = normalize_task(item)
                context = build_prediction_context(task)
            except (TypeError, ValueError):
                continue

            samples.append(
                {
                    **context,
                    "duration_minutes": clamp_int(
                        task.get("predicted_duration", task["estimated_duration"]),
                        task["estimated_duration"],
                        15,
                        480,
                    ),
                }
            )

    return samples


def train_model(
    model_path: str | Path = MODEL_FILE, dataset_path: str | Path = DATASET_FILE
) -> dict[str, Any]:
    samples = _read_csv_samples(Path(dataset_path))
    samples.extend(_read_task_history_samples())

    if not samples:
        raise FileNotFoundError("Opetusdataa ei löytynyt mallin kouluttamiseen.")

    payload = {
        "version": MODEL_VERSION,
        "trained_at": datetime.now().isoformat(timespec="seconds"),
        "sample_count": len(samples),
        "samples": samples,
    }

    with Path(model_path).open("wb") as handle:
        pickle.dump(payload, handle)

    return payload


def load_model(model_path: str | Path = MODEL_FILE, auto_train: bool = True) -> dict[str, Any]:
    path = Path(model_path)
    if path.exists():
        try:
            with path.open("rb") as handle:
                payload = pickle.load(handle)
            if (
                isinstance(payload, dict)
                and payload.get("version") == MODEL_VERSION
                and isinstance(payload.get("samples"), list)
            ):
                return payload
        except Exception:
            pass

    if auto_train:
        return train_model(model_path=path)

    return {"version": MODEL_VERSION, "sample_count": 0, "samples": []}


def _cyclic_distance(left: int, right: int, cycle: int) -> int:
    difference = abs(left - right)
    return min(difference, cycle - difference)


def _sample_distance(sample: dict[str, int], target: dict[str, int]) -> float:
    return (
        abs(sample["priority"] - target["priority"]) * 2.2
        + abs(sample["difficulty"] - target["difficulty"]) * 1.4
        + abs(sample["deadline_days"] - target["deadline_days"]) * 0.6
        + _cyclic_distance(sample["start_hour"], target["start_hour"], 24) * 0.4
        + _cyclic_distance(sample["day_of_week"], target["day_of_week"], 7) * 0.3
        + abs(sample["estimated_by_user"] - target["estimated_by_user"]) / 20.0
    )


def _predict_from_context(context: dict[str, int], model: dict[str, Any]) -> int:
    samples = model.get("samples", [])
    if not samples:
        return context["estimated_by_user"]

    neighbors = sorted(samples, key=lambda sample: _sample_distance(sample, context))[:5]
    weighted_total = 0.0
    weight_sum = 0.0

    for sample in neighbors:
        distance = _sample_distance(sample, context)
        weight = 1.0 / (distance + 1.0)
        weighted_total += weight * sample["duration_minutes"]
        weight_sum += weight

    prediction = round(weighted_total / weight_sum) if weight_sum else context["estimated_by_user"]
    return clamp_int(prediction, context["estimated_by_user"], 15, 480)


def predict_duration_for_task(task: dict[str, Any]) -> int:
    normalized = normalize_task(task)
    context = build_prediction_context(normalized)
    model = load_model()
    return _predict_from_context(context, model)


def predict_duration(
    priority: int,
    estimated_by_user: int = DEFAULT_DURATION_MINUTES,
    deadline: str | datetime | None = None,
    difficulty: int | None = None,
) -> int:
    if deadline is None:
        deadline_dt = (datetime.now() + timedelta(days=1)).replace(
            hour=18, minute=0, second=0, microsecond=0
        )
    elif isinstance(deadline, datetime):
        deadline_dt = deadline
    else:
        deadline_dt = parse_deadline(deadline)

    task = {
        "title": "AI-arvio",
        "deadline": format_deadline(deadline_dt),
        "priority": priority,
        "estimated_duration": estimated_by_user,
        "difficulty": difficulty or priority,
        "status": "pending",
    }
    return predict_duration_for_task(task)


def recommend_schedule(task: dict[str, Any]) -> dict[str, Any]:
    normalized = normalize_task(task)
    predicted_duration = predict_duration_for_task(normalized)
    start_time, end_time, _ = task_time_window(normalized, predicted_duration)

    return {
        "predicted_duration": predicted_duration,
        "recommended_start": format_deadline(start_time.replace(tzinfo=None)),
        "deadline": format_deadline(end_time.replace(tzinfo=None)),
    }


def predict_schedule(
    priority: int, duration: int = DEFAULT_DURATION_MINUTES, deadline: str | None = None
) -> str:
    predicted_duration = predict_duration(
        priority=priority,
        estimated_by_user=duration,
        deadline=deadline,
        difficulty=priority,
    )

    if deadline:
        deadline_dt = parse_deadline(deadline)
    else:
        deadline_dt = (datetime.now() + timedelta(days=1)).replace(
            hour=18, minute=0, second=0, microsecond=0
        )

    start_time = deadline_dt - timedelta(minutes=predicted_duration)
    return start_time.strftime("%H:%M")
