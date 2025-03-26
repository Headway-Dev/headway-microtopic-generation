import json
import loguru

from . import abstract


class LocalMicrotopicsStorage(abstract.AbstractMicrotopicsStorage):
    def __init__(self, p_tpk_to_class_en) -> None:
        self._tpk_to_class: dict[str, int] | None = None
        self._p = p_tpk_to_class_en

    def list_microtopics(self) -> list[str]:
        if self._tpk_to_class is None:
            self._load_microtopics()
        return list(self._tpk_to_class.keys())

    def _load_microtopics(self) -> None:
        loguru.logger.debug('Fetching micro-topics')
        self._tpk_to_class = json.loads(self._p.read_text())

    def microtopic_to_class(self, tpk: str) -> int | None:
        return self._tpk_to_class.get(tpk)
