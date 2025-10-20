from app.models import Book
from app.repositories.base import BaseRepository


class BookRepository(BaseRepository[Book]):
    pass


book_repository = BookRepository(Book)
