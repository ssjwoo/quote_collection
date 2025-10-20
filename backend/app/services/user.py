from app.repositories import user_repository
from app.services.base import BaseService
from app.repositories.user import UserRepository


class UserService(BaseService[UserRepository]):
    pass


user_service = UserService(user_repository)
