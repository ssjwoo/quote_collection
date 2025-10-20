from app.repositories import producer_repository
from app.services.base import BaseService
from app.repositories.producer import ProducerRepository


class ProducerService(BaseService[ProducerRepository]):
    pass


producer_service = ProducerService(producer_repository)
