from app.repositories.base import BaseRepository
from app.models import Movie

class MovieRepository(BaseRepository[Movie]):
    pass

movie_repo = MovieRepository(Movie)