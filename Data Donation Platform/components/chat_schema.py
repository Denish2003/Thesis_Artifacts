from __future__ import annotations

from datetime import datetime
from typing import Any

from components.types import ChatList, ChatRecord, DatetimeOrNone, JsonValue, NormalizedMessage, SourceFormat


def normalize_conversation_payload(data: JsonValue) -> tuple[ChatList, SourceFormat]:
    """Accept both the legacy ChatGPT export and the extension wrapper format."""
    if isinstance(data, list):
        return data, "chatgpt_export"

    if isinstance(data, dict) and isinstance(data.get("conversations"), list):
        return data["conversations"], "extension_export"

    raise ValueError("Unsupported conversation JSON format.")


def extract_chat_text(chat: ChatRecord) -> str:
    """Flatten a conversation into searchable plain text for list filtering."""
    if isinstance(chat.get("messages"), list):
        texts = []
        for message in chat["messages"]:
            markdown = message.get("markdown", "")
            if isinstance(markdown, str) and markdown.strip():
                texts.append(markdown.strip())
        return " ".join(texts)

    texts = []
    mapping = chat.get("mapping", {})

    for node in mapping.values():
        message = node.get("message")
        if not message:
            continue

        content = message.get("content", {})
        parts = content.get("parts", [])

        if not isinstance(parts, list):
            continue

        for part in parts:
            if isinstance(part, str):
                texts.append(part)
            elif isinstance(part, dict):
                if "asset_pointer" in part:
                    texts.append("[Image]")
                else:
                    texts.append("[Non-text content]")

    return " ".join(texts)


def get_chat_datetime(chat: ChatRecord) -> DatetimeOrNone:
    """Prefer extension timestamps, then fall back to legacy ChatGPT timestamps."""
    saved_at = chat.get("savedAt")
    if saved_at:
        try:
            return datetime.fromisoformat(saved_at.replace("Z", "+00:00"))
        except Exception:
            pass

    ts = chat.get("create_time")
    if ts:
        try:
            return datetime.fromtimestamp(ts)
        except Exception:
            return None

    return None


def get_chat_messages(chat: ChatRecord) -> list[NormalizedMessage]:
    """Return a normalized message list regardless of the source schema."""
    if isinstance(chat.get("messages"), list):
        messages: list[NormalizedMessage] = []

        for index, message in enumerate(chat["messages"]):
            role = message.get("role", "unknown")
            if role in ("system", "tool"):
                continue

            text = message.get("markdown", "")
            if not isinstance(text, str) or not text.strip():
                continue

            # Preserve the original list index so redaction writes back to the same
            # message entry instead of rebuilding the payload from scratch.
            messages.append(
                {
                    "id": f"message_{index}",
                    "role": role,
                    "time": None,
                    "text": text.strip(),
                    "source": "messages",
                    "message_index": index,
                }
            )

        return messages

    messages: list[NormalizedMessage] = []
    mapping = chat.get("mapping", {})

    for node_id, node in mapping.items():
        msg = node.get("message")
        if not msg:
            continue

        role = msg.get("author", {}).get("role", "unknown")
        if role in ("system", "tool"):
            continue

        text = parse_legacy_message(msg)
        if not text:
            continue

        raw_time = msg.get("create_time")
        time_str = None
        if raw_time:
            try:
                time_str = datetime.fromtimestamp(raw_time).strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                time_str = str(raw_time)

        messages.append(
            {
                "id": node_id,
                "role": role,
                "time": time_str,
                "text": text,
                "source": "mapping",
            }
        )

    # Legacy exports are not guaranteed to be in chronological order in `mapping`.
    return sorted(messages, key=lambda item: item["time"] or "")


def update_message_text(chat: ChatRecord, message_data: NormalizedMessage, new_text: str) -> None:
    """Write edited text back into the original schema shape."""
    if message_data["source"] == "messages":
        chat["messages"][message_data["message_index"]]["markdown"] = new_text
        return

    mapping = chat.get("mapping", {})
    mapping[message_data["id"]]["message"]["content"]["parts"] = [new_text]
    chat["mapping"] = mapping


def parse_legacy_message(msg: dict[str, Any]) -> str:
    """Flatten legacy message parts into a display string with media placeholders."""
    content = msg.get("content") or {}
    parts = content.get("parts") or []

    display_parts = []
    for part in parts:
        if isinstance(part, str) and part.strip():
            display_parts.append(part.strip())
        elif isinstance(part, dict):
            display_parts.append("[Media content here]")
    return "\n".join(display_parts)
