from dataclasses import dataclass


@dataclass
class Note:
    id: int | None
    text: str
    created_at: str
    pinned: bool = False
