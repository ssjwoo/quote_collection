from app.services.base import BaseService
from app.repositories.drama import drama_repo

class DramaService(BaseService):
    pass

drama_service = DramaService(drama_repo)
