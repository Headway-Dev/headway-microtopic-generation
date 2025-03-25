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
        books_to_update = [b for b in all_books if self._books_s.get_book_microtopics(b.identifier) is None]
        loguru.logger.info(f'{len(books_to_update)} / {len(all_books)} books need micro-topic update')

        # Generate books' micro-topics
        def process_book(b):
            pred_microtopics = self._predictor.predict(b, all_microtopics)
            loguru.logger.debug(f'Predicted {len(pred_microtopics)} for "{b.identifier}"')
            self._books_s.set_book_microtopics(b.identifier, pred_microtopics)
        with ThreadPoolExecutor(max_workers=30) as executor:  # TODO: de-hardcode the number of workers
            executor.map(process_book, books_to_update)

        # Store changes
        self._books_s.store_changes()
