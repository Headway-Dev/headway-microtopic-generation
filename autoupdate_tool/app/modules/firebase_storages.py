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

        self._books: list[abstract.Book] | None = None
        self._identifier2microtopics: dict[str, list[str]] | None = None  # fetched from db
        self._identifier2microtopics_updates: dict[str, list[str]] = dict()  # to be inserted into db

    def list_books(self) -> list[abstract.Book]:
        if self._books is None:
            self._load_books()
        return self._books

    def get_book_microtopics(self, book_identifier: str) -> list[str] | None:
        if self._identifier2microtopics is None:
            self._load_identifier2microtopics()
        return self._identifier2microtopics.get(book_identifier)
    
    def set_book_microtopics(self, book_identifier: str, microtopics: list[str]) -> None:
        self._identifier2microtopics_updates[book_identifier] = microtopics

    def _load_books(self) -> None:
        loguru.logger.debug('Fetching books from FireBase')
        self._books = []

        ref_buff = []
        page_size = 100
        books_ref_gen = self._db.collection('books').list_documents(page_size=page_size)
        while True:
            try:
                doc_ref = next(books_ref_gen)
                ref_buff.append(doc_ref)
                stop = False
            except:
                stop = True
            if stop or len(ref_buff) == page_size:
                books_data = [d.to_dict() for d in self._db.get_all(ref_buff)]
                ref_buff.clear()

                for book_data in books_data:
                    if not book_data or not book_data.get('enabled', False):
                        continue
                    identifier = book_data.get('id')
                    if not identifier:
                        continue
                    en_title = book_data.get('localization', {}).get('en', {}).get('title')
                    if not en_title:
                        continue
                    self._books.append(abstract.Book(identifier=identifier, title=en_title))
                loguru.logger.debug(f'Fetched {len(self._books)} books...')
            if stop:
                break

    def _load_identifier2microtopics(self) -> None:
        self._identifier2microtopics = dict()
        # todo: de-hardcode
        self._identifier2microtopics = self._db.collection('common').document('title_relations').get().to_dict()['microtopics']

    def store_changes(self) -> None:
        FIELDNAME = 'microtopics_test'
        self._identifier2microtopics.update(self._identifier2microtopics_updates)
        self._identifier2microtopics_updates.clear()
        # todo: de-hardcode
        self._db.collection('common').document('title_relations').update({
            FIELDNAME: self._identifier2microtopics
        })
        loguru.logger.info(f'Uploaded changes to {FIELDNAME}')
