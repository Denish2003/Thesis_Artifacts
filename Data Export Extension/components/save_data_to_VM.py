from __future__ import annotations

import os
import json
from datetime import datetime
import uuid
from typing import Any

DONATION_DIR = os.path.expanduser("~/data_donations")
EMAIL_DIR = os.path.expanduser("~/email_reminders")


def _ensure_parent_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def _load_json_list(filepath: str) -> list[dict[str, Any]]:
    """Read a JSON list from disk and recover gracefully from missing or bad files."""
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []

    return data if isinstance(data, list) else []


def save_donation(json_data: Any) -> str:
    """Persist a donated JSON payload to the local donation directory."""
    donation_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().strftime("%Y_%m_%d_%H_%M_%S")

    filename = f"donation_{timestamp}_{donation_id}.json"
    filepath = os.path.join(DONATION_DIR, filename)

    _ensure_parent_dir(filepath)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2)

    return filepath


def save_email(email: str) -> bool:
    """Append a reminder email entry to the local reminder store."""
    os.makedirs(EMAIL_DIR, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y/%m/%d_%H:%M:%S")

    entry = {
        "email": email,
        "timestamp": timestamp
    }

    filepath = os.path.join(EMAIL_DIR, "emails.json")
    data = _load_json_list(filepath)

    data.append(entry)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return True
    
