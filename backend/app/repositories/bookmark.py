from app.models import Bookmark
from app.repositories.base import BaseRepository


class BookmarkRepository(BaseRepository[Bookmark]):
    pass


bookmark_repository = BookmarkRepository(Bookmark)
