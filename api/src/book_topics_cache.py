import json
from pathlib import Path


class BookTopicsCache:
    def __init__(
            self,
            p_file: Path
    ) -> None:
        self._p = p_file
        self._cache: dict[str, list[int]] | None = None

    def _load_cache(self) -> None:
        self._cache = json.loads(self._p.read_text()) if self._p.exists() else dict()

    def _store_cache(self) -> None:
        self._p.write_text(json.dumps(self._cache))

    def get(self, book_identifier: str) -> list[int] | None:
        if self._cache is None:
            self._load_cache()
        return self._cache.get(book_identifier)

    def set(self, book_identifier: str, topics: list[int]) -> None:
        if self._cache is None:
            self._load_cache()
        self._cache[book_identifier] = topics
        self._store_cache()
