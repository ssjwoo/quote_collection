from app.repositories import bookmark_repository
from app.services.base import BaseService
from app.repositories.bookmark import BookmarkRepository


class BookmarkService(BaseService[BookmarkRepository]):
    pass


bookmark_service = BookmarkService(bookmark_repository)
