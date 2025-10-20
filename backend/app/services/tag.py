from app.repositories import tag_repository
from app.services.base import BaseService
from app.repositories.tag import TagRepository


class TagService(BaseService[TagRepository]):
    pass


tag_service = TagService(tag_repository)
