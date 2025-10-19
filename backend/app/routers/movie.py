from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.movie import movie_repo
from app.schemas import movie as movie_schema

router = APIRouter(prefix="/movies", tags=["movies"])


@router.post("/", response_model=movie_schema.MovieRead, status_code=201)
def create_new_movie(movie: movie_schema.MovieCreate, db: Session = Depends(get_db)):
    """
    새로운 영화 기록을 생성합니다.
    """
    created_movie = movie_repo.create_movie(db=db, movie_data=movie)
    return created_movie
