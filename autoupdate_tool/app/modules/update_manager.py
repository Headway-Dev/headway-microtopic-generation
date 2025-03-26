from concurrent.futures import ThreadPoolExecutor

import loguru

from .abstract import (
    AbstractBooksDataStorage, 
    AbstractMicrotopicsStorage, 
    AbstracBookMicrotopicsPredictor
)


class UpdateManager:
    def __init__(
            self,
            microtopics_storage: AbstractMicrotopicsStorage,
            predictor: AbstracBookMicrotopicsPredictor,
            books_storage: AbstractBooksDataStorage,
    ) -> None:
        self._predictor = predictor
        self._books_s = books_storage
        self._microtopics_s = microtopics_storage

    def run(self) -> None:
        # Fetch micro-topics
        all_microtopics = self._microtopics_s.list_microtopics()
        loguru.logger.info(f'Fetched {len(all_microtopics)} micro-topics')

        # Fetch books to update
        all_books = self._books_s.list_books()

        # Generate books' micro-topics
        def process_book(b, current_topics):
            current_topics = [] if current_topics is None else current_topics
            loguru.logger.debug(f'{b.identifier} had {len(current_topics)} topics')
            current_topics = self._refine_tpks_styles(current_topics)  # ensure correct toppics
            if len(current_topics) < 3:
                pred_microtopics = self._predictor.predict(b, all_microtopics)
                final_microtopics = (current_topics + [t for t in pred_microtopics if t not in current_topics])[:8]
            else:
                final_microtopics = current_topics
            loguru.logger.debug(f'Obtained {len(final_microtopics)} correct topics for "{b.identifier}"')
            self._books_s.set_book_microtopics(b.identifier, final_microtopics)
        with ThreadPoolExecutor(max_workers=50) as executor:  # TODO: de-hardcode the number of workers
            executor.map(process_book, all_books,
                         [self._books_s.get_book_microtopics(b.identifier) for b in all_books])

        self._books_s.store_changes()

    def _refine_tpks_styles(self, tpks_to_refine: list[str]) -> list[str]:
        correct_tpks = [
            [t for t in self._microtopics_s.list_microtopics()
             if t.lower() == curr_t.lower().replace('and', '&').replace('\'', '’')]
            for curr_t in tpks_to_refine
        ]
        correct_tpks = [v[0] for v in correct_tpks if len(v) > 0]
        return correct_tpks
