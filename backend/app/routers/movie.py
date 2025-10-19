from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_db
from app.schemas import MovieCreate, MovieRead, MovieUpdate
from app.services.movie import movie_service

router = APIRouter(prefix="/movie", tags=["Movie"])

@router.post("/", response_model=MovieRead)
async def create(movie: MovieCreate, db: AsyncSession = Depends(get_async_db)):
    return await movie_service.repository.create(db, obj_in=movie)

@router.get("/", response_model=list[MovieRead])
async def list(db: AsyncSession = Depends(get_async_db)):
    return await movie_service.repository.get_all(db)

@router.get("/{movie_id}", response_model=MovieRead)
async def get(movie_id: int, db: AsyncSession = Depends(get_async_db)):
    movie = await movie_service.repository.get(db, id=movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.put("/{movie_id}", response_model=MovieRead)
async def update(movie_id: int, movie_in: MovieUpdate, db: AsyncSession = Depends(get_async_db)):
    movie = await movie_service.repository.get(db, id=movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie = await movie_service.repository.update(db, db_obj=movie, obj_in=movie_in)
    return movie

@router.delete("/{movie_id}")
async def delete(movie_id: int, db: AsyncSession = Depends(get_async_db)):
    movie = await movie_service.repository.get(db, id=movie_id)
    if not movie:
        raise HTTPException(status_code=400, detail="Movie not found")
    await movie_service.repository.remove(db, id=movie_id)
    return {"message": "Movie deleted"}
