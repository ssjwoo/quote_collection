from app.repositories import publisher_repository
from app.services.base import BaseService
from app.repositories.publisher import PublisherRepository


class PublisherService(BaseService[PublisherRepository]):
    pass


publisher_service = PublisherService(publisher_repository)
