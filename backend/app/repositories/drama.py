from app.repositories.base import BaseRepository
from app.models import Drama

class DramaRepository(BaseRepository[Drama]):
    pass

drama_repo = DramaRepository(Drama)
