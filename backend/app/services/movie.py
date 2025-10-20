from app.services.base import BaseService
from app.repositories.movie import movie_repo

class MovieService(BaseService):
    pass

movie_service = MovieService(movie_repo)
