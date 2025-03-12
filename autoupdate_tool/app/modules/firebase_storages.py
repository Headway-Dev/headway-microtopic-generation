from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import loguru
from firebase_admin import initialize_app, credentials, firestore

from . import abstract


class FirebaseBookStorage(abstract.AbstractBooksDataStorage):
    def __init__(
            self,
            p_creds: Path, 
    ) -> None:
        creds = credentials.Certificate(str(p_creds))
        app = initialize_app(creds)
        self._db = firestore.client(app)

        self._is_active = False
        self._books: list[abstract.Book] | None = None
        self._identifier2microtopics: dict[str, list[str]] | None = None  # fetched from db
        self._identifier2microtopics_updates: dict[str, list[str]] = dict()  # to be inserted into db

    def __enter__(self) -> "FirebaseBookStorage":
        self._is_active = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._upload_book_microtopics()
        self._is_active = False

    def list_books(self) -> list[abstract.Book]:
        assert self._is_active
        if self._books is None:
            self._load_books()
        return self._books

    def get_book_microtopics(self, book_identifier: str) -> list[str] | None:
        assert self._is_active
        if self._identifier2microtopics is None:
            self._load_identifier2microtopics()
        return self._identifier2microtopics.get(book_identifier)
    
    def set_book_microtopics(self, book_identifier: str, microtopics: list[str]) -> None:
        assert self._is_active
        self._identifier2microtopics_updates[book_identifier] = microtopics

    def _load_books(self) -> None:
        loguru.logger.debug('Fetching books from FireBase')
        self._books = []

        book_doc_refs = self._db.collection('books').list_documents()

        def fetch_book(book_doc_ref):
            identifier = book_doc_ref.id  # Alternative to splitting path
            book_data = book_doc_ref.get().to_dict()

            if not book_data or not book_data.get('enabled', False):
                return None

            en_title = book_data.get('localization', {}).get('en', {}).get('title')
            if not en_title:
                return None

            return abstract.Book(identifier=identifier, title=en_title)

        with ThreadPoolExecutor(max_workers=100) as executor:  # todo: de-hardcode the number of workers
            books = list(executor.map(fetch_book, book_doc_refs))

        self._books = [book for book in books if book]  # Remove None values

    def _load_identifier2microtopics(self) -> None:
        self._identifier2microtopics = dict()
        # todo: de-hardcode
        self._identifier2microtopics = self._db.collection('common').document('title_relations').get().to_dict()['microtopics']

    def _upload_book_microtopics(self) -> None:
        FIELDNAME = 'microtopics_test'
        self._identifier2microtopics.update(self._identifier2microtopics_updates)
        self._identifier2microtopics_updates.clear()
        # todo: de-hardcode
        self._db.collection('common').document('title_relations').update({
            FIELDNAME: self._identifier2microtopics
        })
        loguru.logger.info(f'Uploaded changes to {FIELDNAME}')
