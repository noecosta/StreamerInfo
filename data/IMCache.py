from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


class IMCache:
    @dataclass
    class ChannelInformation:
        name: str = field(default_factory=str)
        displayed_name: str = field(default_factory=str)
        is_partnered: bool = field(default_factory=bool)
        avatar_uri: str = field(default_factory=str)
        live_count: int = field(default_factory=int)
        follower_count: int = field(default_factory=int)
        latest_stream: datetime = field(default_factory=datetime)
        timestamp: datetime = field(default_factory=datetime)

    cache: dict[str, ChannelInformation] = {}

    def __init__(self: IMCache) -> None:
        raise NotImplementedError("Instantiation of IMCache not allowed.")

    @classmethod
    def get(cls: IMCache, key: str) -> ChannelInformation | bool:
        if key in cls.cache:
            return cls.cache[key]
        return False

    @classmethod
    def store(cls: IMCache, key: str, value: ChannelInformation) -> None:
        cls.cache[key] = value
