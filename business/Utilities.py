from __future__ import annotations

from pathlib import Path


class Utilities:
    @classmethod
    def get_dynamic_path(cls: Utilities, path: str) -> Path:
        if "compiled" in globals():
            # compiled version
            return Path(__file__).parent.joinpath(path)
        else:
            # uncompiled version
            return Path(__file__).parent.parent.joinpath(path)
