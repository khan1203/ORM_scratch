from core.exceptions import ResourceNotFoundException
from core.repository.book_repository import BookRepository
from core.models.book import Book


class BookService:
    def __init__(self):
        self.repository = BookRepository()
        self.seed_data()

    def seed_data(self):
        self.repository.create(
            name="The Great Gatsby", author="F. Scott Fitzgerald"
        )
        self.repository.create(
            name="Life of Pi", author="Yann Martel"
        )

    def get_all(self) -> list[Book]:
        return self.repository.all()

    def create(self, schema: dict) -> Book:
        return self.repository.create(**schema)

    def delete(self, book_id: int) -> None:
        deleted = self.repository.delete(book_id)
        if not deleted:
            raise ResourceNotFoundException(f"Book associated with id: {book_id} not found")