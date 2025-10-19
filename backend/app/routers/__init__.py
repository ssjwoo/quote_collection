from fastapi import APIRouter

from . import (
    auth,
    book,
    bookmark,
    producer,
    publisher,
    quote,
    source,
    tag,
    user,
    movie,
)  ### Movie추가 ### quote_tag 임시 비활성화

router = APIRouter()

router.include_router(auth.router)
router.include_router(book.router)
router.include_router(bookmark.router)
router.include_router(producer.router)
router.include_router(publisher.router)
router.include_router(quote.router)
# router.include_router(quote_tag.router) 임시 비활성화
router.include_router(source.router)
router.include_router(tag.router)
router.include_router(user.router)
router.include_router(movie.router)
