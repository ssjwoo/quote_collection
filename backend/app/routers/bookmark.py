from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_db
from app.schemas import BookmarkCreate, BookmarkRead, QuoteRead
from app.schemas.pagination import PaginatedResponse
from app.services import bookmark_service
import math
from app.models import Bookmark
from app.services import quote_service  # Need quote service to create new quotes

router = APIRouter(prefix="/bookmark", tags=["Bookmark"])

# 유저의 북마크 조회 (Paging 지원)
@router.get("/user/{user_id}", response_model=PaginatedResponse[QuoteRead])
async def get_bookmarks_by_user(
    user_id: int, 
    page: int = 1, 
    size: int = 10, 
    db: AsyncSession = Depends(get_async_db)
):
    items, total = await bookmark_service.get_by_user_id_paginated(db, user_id=user_id, page=page, size=size)
    total_pages = math.ceil(total / size) if total > 0 else 0
    
    return PaginatedResponse(
        items=[bookmark.quote for bookmark in items],
        total=total,
        page=page,
        size=size,
        total_pages=total_pages
    )

async def _ensure_ai_quote_exists(db: AsyncSession, bookmark_in: BookmarkCreate) -> int:
    """AI 추천 문구가 DB에 없는 경우(id <= 0) 새로 생성하거나 기존 것을 찾아 ID를 반환합니다.
    동일한 내용의 문구가 있으면 기존 ID를 반환하여 중복을 방지합니다.
    """
    if bookmark_in.quote_id > 0 or not bookmark_in.quote_data:
        return bookmark_in.quote_id

    try:
        from app.schemas import QuoteCreate, SourceCreate
        from app.services import source_service, quote_service
        from sqlalchemy import select
        from app.models import Quote, Source
        
        q_data = bookmark_in.quote_data
        content = q_data.get('content')
        title = q_data.get('source_title', 'Unknown Source')
        author = q_data.get('author') or q_data.get('creator') or 'Unknown'
        
        print(f"DEBUG: Ensuring AI quote exists: {content[:30]}...")
        
        # 1. 이미 동일한 내용의 문구가 있는지 확인 (가장 최신 것 하나 선택)
        stmt = select(Quote).where(Quote.content == content).order_by(Quote.id.desc())
        result = await db.execute(stmt)
        existing_quote = result.scalars().first() # Use first() instead of scalar_one_or_none() to avoid 500 on duplicates
        if existing_quote:
            print(f"DEBUG: Existing quote found (ID: {existing_quote.id}). Reusing.")
            return existing_quote.id

        # 2. Source 생성 전 기존 소스 확인 (중복 방지)
        stmt_source = select(Source).filter(Source.title == title, Source.creator == author).order_by(Source.id.desc())
        source_result = await db.execute(stmt_source)
        existing_source = source_result.scalars().first()
        
        if existing_source:
            source_id = existing_source.id
            print(f"DEBUG: Existing source found (ID: {source_id}).")
        else:
            # Source 신규 생성
            raw_type = q_data.get('source_type', 'book').lower()
            allowed_types = ["book", "movie", "drama", "tv", "speech", "other"]
            source_type = raw_type if raw_type in allowed_types else "other"
            
            new_source = await source_service.repository.create(db, obj_in=SourceCreate(
                title=title,
                creator=author,
                source_type=source_type
            ))
            await db.flush()
            source_id = new_source.id
        
        # 4. Quote 생성
        new_quote = await quote_service.repository.create(db, obj_in=QuoteCreate(
            content=content,
            source_id=source_id,
            user_id=bookmark_in.user_id
        ))
        await db.flush()
        return new_quote.id
    except Exception as e:
        print(f"CRITICAL: Error in _ensure_ai_quote_exists: {e}")
        import traceback
        traceback.print_exc()
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"AI 문구 저장 실패: {str(e)}")

# 북마크 추가
@router.post("/", response_model=BookmarkRead)
async def create_bookmark(bookmark: BookmarkCreate, db: AsyncSession = Depends(get_async_db)):
    # 1. AI 문구인 경우 실제 DB에 먼저 생성
    bookmark.quote_id = await _ensure_ai_quote_exists(db, bookmark)
    
    # 2. 북마크 생성 (quote_data 제외 필수: Bookmark 모델에 없는 필드임)
    try:
        new_bookmark = Bookmark(user_id=bookmark.user_id, quote_id=bookmark.quote_id)
        db.add(new_bookmark)
        await db.commit()
        return new_bookmark
    except Exception as e:
        await db.rollback()
        print(f"Error creating bookmark: {e}")
        # 이미 북마크된 경우 등 처리
        raise HTTPException(status_code=400, detail="이미 북마크된 문장이거나 저장할 수 없습니다.")

# 북마크 토글
@router.post("/toggle")
async def toggle_bookmark(bookmark_in: BookmarkCreate, db: AsyncSession = Depends(get_async_db)):
    # 1. AI 문구인 경우 실제 DB에 먼저 생성
    bookmark_in.quote_id = await _ensure_ai_quote_exists(db, bookmark_in)

    # 2. 토글 로직
    bookmark = await bookmark_service.repository.get(db, id=(bookmark_in.user_id, bookmark_in.quote_id))
    if bookmark:
        await db.delete(bookmark)
        await db.commit()
        return {"bookmarked": False}
    else:
        try:
            new_bookmark = Bookmark(user_id=bookmark_in.user_id, quote_id=bookmark_in.quote_id)
            db.add(new_bookmark)
            await db.commit()
            return {"bookmarked": True}
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail="북마크 처리 중 오류 발생")

# 북마크 상태 확인
@router.get("/status")
async def get_bookmark_status(user_id: int, quote_id: int, db: AsyncSession = Depends(get_async_db)):
    bookmark = await bookmark_service.repository.get(db, id=(user_id, quote_id))
    return {"bookmarked": bookmark is not None}

# 조회
@router.get("/", response_model=list[BookmarkRead])
async def list_bookmark(db: AsyncSession = Depends(get_async_db)):
    return await bookmark_service.repository.get_all(db)

# 삭제
@router.delete("/")
async def delete_bookmark(user_id: int, quote_id: int, db: AsyncSession = Depends(get_async_db)):
    bookmark = await bookmark_service.repository.get(db, id=(user_id, quote_id)) # 복합키
    if not bookmark:
        raise HTTPException(status_code=400, detail="북마크를 찾을 수 없음")
    await bookmark_service.repository.remove(db, id=(user_id, quote_id))
    return {"message": "북마크 삭제 됨"}