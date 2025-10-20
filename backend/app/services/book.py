from app.repositories import book_repository
from app.services.base import BaseService
from app.repositories.book import BookRepository


class BookService(BaseService[BookRepository]):
    pass


book_service = BookService(book_repository)
