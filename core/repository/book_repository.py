from core.models.book import Book
from core import db
from core.repository.author_repository import AuthorRepository


class BookRepository:
    def __init__(self):
        self.author_repository = AuthorRepository()

    def insert(self, book: Book) -> Book:
        db.save(book)

    def create(self, **kwargs) -> Book:
        self._id += 1
        kwargs["id"] = self._id
        book = Book(**kwargs)
        self._books.append(book)
        return book

    def all(self) -> list[Book]:
        return db.get_all(Book)
    
    def get_by_id(self, id: int) -> Book | None:
        return db.get_by_id(Book, id)

    def delete(self, id):
        book = self.get_by_id(Book, id)
        db.delete(Book, book.id)