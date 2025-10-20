from app.models import Producer
from app.repositories.base import BaseRepository


class ProducerRepository(BaseRepository[Producer]):
    pass


producer_repository = ProducerRepository(Producer)
