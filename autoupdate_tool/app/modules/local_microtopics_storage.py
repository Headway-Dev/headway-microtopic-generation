import loguru
import pandas as pd

from . import abstract


class LocalMicrotopicsStorage(abstract.AbstractMicrotopicsStorage):
    def __init__(self, p_microtopics_csv) -> None:
        self._is_active = False
        self._microtopics: list[str] | None = None
        self._p = p_microtopics_csv

    def __enter__(self) -> "LocalMicrotopicsStorage":
        self._is_active = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._is_active = False

    def list_microtopics(self) -> list[str]:
        loguru.logger.debug('Fetching micro-topics')
        if self._microtopics is None:
            self._load_microtopics()
        return self._microtopics

    def _load_microtopics(self) -> None:
        self._microtopics = list(pd.read_csv(self._p, index_col=0).iloc[:, 0])
