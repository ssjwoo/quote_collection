from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_db
from app.schemas import BookmarkCreate, BookmarkRead, QuoteRead
from app.services import bookmark_service
from app.models import Bookmark
from app.services import quote_service  # Need quote service to create new quotes

router = APIRouter(prefix="/bookmark", tags=["Bookmark"])

# 유저의 북마크 조회
@router.get("/user/{user_id}", response_model=list[QuoteRead])
async def get_bookmarks_by_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    bookmarks = await bookmark_service.repository.get_by_user_id(db, user_id=user_id)
    return [bookmark.quote for bookmark in bookmarks]

# 북마크 추가
@router.post("/", response_model=BookmarkRead)
async def create_bookmark(bookmark: BookmarkCreate, db: AsyncSession = Depends(get_async_db)):
    # 1. Check if it's an AI Quote (negative ID or 0)
    if (bookmark.quote_id <= 0) and bookmark.quote_data:
        # Create the quote first
        print(f"DEBUG: Creating new AI quote for bookmark: {bookmark.quote_data.get('content')}")
        try:
            from app.schemas import QuoteCreate, SourceCreate, TagCreate
            from app.services import source_service, tag_service
            
            q_data = bookmark.quote_data
            
            # Ensure Source Exists or Create Dummy
            # For simplicity, we might reuse an existing "AI Recommendation" source or create one on fly
            # Here we try to use the provided source info
            source_title = q_data.get('source_title', 'Unknown Source')
            source_type = q_data.get('source_type', 'book')
            author = q_data.get('author', 'Unknown')
            
            # Simple check/create source (this logic might be complex depending on uniqueness constraints)
            # For now, let's assume we create a new quote attached to a generic or new source
            # Ideally, checks if source exists. To keep it simple, we trust quote_service or do a quick check
            
            # Let's create a full QuoteCreate object
            # We need to map dict to schema
            
            # Handle Tags
            tags_list = q_data.get('tags', [])
            tag_objects = [] # Logic to find/create tags would go here, simplified below
            
            # Because creating a full quote with source relations correctly is complex in one go without proper service methods,
            # we will assume quote_service.create_with_related (if exists) or build it manually.
            # Simplified approach: Create Source -> Create Quote -> Add Tags
            
            # 1. Source
            # Check if source exists by title? Or just create. 
            # We'll stick to a simple creation specific for this use case.
            
            new_source = await source_service.repository.create(db, obj_in=SourceCreate(
                title=source_title,
                actor=author, # Mapping author to actor/creator field
                source_type=source_type
            ))
            
            # 2. Quote
            new_quote = await quote_service.repository.create(db, obj_in=QuoteCreate(
                content=q_data.get('content'),
                source_id=new_source.id,
                user_id=bookmark.user_id # Assign validation to user? or system? Let's assign to user for now or 1 (admin)
            ))
            
            # 3. Tags (Optional, skip for MVP speed or implement if needed)
            
            # Update bookmark.quote_id with the real ID
            bookmark.quote_id = new_quote.id
            
        except Exception as e:
            print(f"Error creating AI quote: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to save AI quote: {str(e)}")

    return await bookmark_service.repository.create(db, obj_in=bookmark)

# 북마크 토글
@router.post("/toggle")
async def toggle_bookmark(bookmark_in: BookmarkCreate, db: AsyncSession = Depends(get_async_db)):
    # Handle AI Quote Creation Logic (Duplicate of create_bookmark Logic)
    # Refactoring recommended: Move to a service method `ensure_quote_exists`
    if (bookmark_in.quote_id <= 0) and bookmark_in.quote_data:
        print(f"DEBUG: Creating new AI quote for toggle: {bookmark_in.quote_data.get('content')}")
        try:
            from app.schemas import QuoteCreate, SourceCreate
            from app.services import source_service
            
            q_data = bookmark_in.quote_data
            
            # Create Source
            new_source = await source_service.repository.create(db, obj_in=SourceCreate(
                title=q_data.get('source_title', 'Unknown Source'),
                actor=q_data.get('author', 'Unknown'),
                source_type=q_data.get('source_type', 'book')
            ))
            
            # Create Quote
            new_quote = await quote_service.repository.create(db, obj_in=QuoteCreate(
                content=q_data.get('content'),
                source_id=new_source.id,
                user_id=bookmark_in.user_id 
            ))
            
            bookmark_in.quote_id = new_quote.id
            # Verify creation
            await db.flush()
            
        except Exception as e:
            print(f"Error creating AI quote in toggle: {e}")
            raise HTTPException(status_code=500, detail="Error saving AI quote")

    bookmark = await bookmark_service.repository.get(db, id=(bookmark_in.user_id, bookmark_in.quote_id))
    if bookmark:
        await db.delete(bookmark)
        await db.commit()
        return {"bookmarked": False}
    else:
        new_bookmark = Bookmark(user_id=bookmark_in.user_id, quote_id=bookmark_in.quote_id)
        db.add(new_bookmark)
        await db.commit()
        return {"bookmarked": True}

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