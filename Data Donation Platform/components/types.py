from __future__ import annotations

from datetime import datetime
from typing import Any, Literal, TypedDict


JsonValue = Any
SourceFormat = Literal["chatgpt_export", "extension_export"]
MessageSource = Literal["messages", "mapping"]


class PiiMatch(TypedDict, total=False):
    Text: str
    Category: str
    Confidence: float


class NormalizedMessage(TypedDict):
    id: str
    role: str
    time: str | None
    text: str
    source: MessageSource
    message_index: int
    pii: list[PiiMatch]


class StepItem(TypedDict):
    title: str
    body: str
    icon: str


class StatItem(TypedDict):
    label: str
    value: str | int


class StepCardItem(TypedDict):
    title: str
    desc: str
    gif: str


ChatRecord = dict[str, Any]
ChatList = list[ChatRecord]
DatetimeOrNone = datetime | None
