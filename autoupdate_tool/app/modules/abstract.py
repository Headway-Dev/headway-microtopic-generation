from abc import ABC, abstractmethod


class Book:
    def __init__(
            self,
            identifier: str,
            title: str,
    ) -> None:
        self._identifier = identifier
        self._title = title

    @property
    def identifier(self) -> str:
        return self._identifier
    
    @property
    def title(self) -> str:
        return self._title


class AbstractBooksDataStorage(ABC):
    @abstractmethod
    def __enter__(self) -> "AbstractBooksDataStorage":
        """E.g., set up db connection"""
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        """E.g., safely close db connection"""
        pass

    @abstractmethod
    def list_books(self) -> list[Book]:
        """
        :return: list of relevant books that ought to have microtopics
        """
        pass

    @abstractmethod
    def get_book_microtopics(self, book_identifier: str) -> list[str] | None:
        """
        :return: None if no microtopics set, the list of microtopics otherwise
        """
        pass
    
    @abstractmethod
    def set_book_microtopics(self, book_identifier: str, microtopics: list[str]) -> None:
        pass


class AbstractMicrotopicsStorage(ABC):
    @abstractmethod
    def __enter__(self) -> "AbstractMicrotopicsStorage":
        """E.g., set up db connection"""
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        """E.g., safely close db connection"""
        pass

    @abstractmethod
    def list_microtopics(self) -> list[str]:
        """
        :return: a list of latest microtopics that gotta be used
        """
        pass


class AbstracBookMicrotopicsPredictor(ABC):
    @abstractmethod
    def predict(self, book: Book, microtopics: list[str]) -> list[str]:
        pass
