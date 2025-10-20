from app.models import Publisher
from app.repositories.base import BaseRepository


class PublisherRepository(BaseRepository[Publisher]):
    pass


publisher_repository = PublisherRepository(Publisher)
