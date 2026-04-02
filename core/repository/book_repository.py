from core.models.book import Book


class BookRepository:
    def __init__(self):
        self._id = 0
        self._books: list[Book] = []

    def create(self, **kwargs) -> Book:
        self._id += 1
        kwargs["id"] = self._id
        book = Book(**kwargs)
        self._books.append(book)
        return book

    def all(self) -> list[Book]:
        return self._books
    
    def get_by_id(self, id: int) -> Book | None:
        for book in self._books:
            if book.id == id:
                return book
        return None

    def delete(self, id):
        for ind, book in enumerate(self._books):
            if book.id == id:
                del self._books[ind]
                return True
        return False