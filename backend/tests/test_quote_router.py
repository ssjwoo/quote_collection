import pytest
import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, Source, Quote, Bookmark
from app.core.auth import hash_password

@pytest.mark.asyncio
async def test_get_popular_quotes(client: httpx.AsyncClient, db_session: AsyncSession):
    # 1. Setup: Create users, sources, quotes, and bookmarks
    user1 = User(email="popuser1@example.com", username="popuser1", hashed_password=hash_password("pw"))
    user2 = User(email="popuser2@example.com", username="popuser2", hashed_password=hash_password("pw"))
    source = Source(title="Test Book", source_type="book", creator="Test Author")
    db_session.add_all([user1, user2, source])
    await db_session.commit()

    quote1 = Quote(user_id=user1.id, source_id=source.id, content="Quote 1") # Less popular
    quote2 = Quote(user_id=user1.id, source_id=source.id, content="Quote 2") # Most popular
    quote3 = Quote(user_id=user1.id, source_id=source.id, content="Quote 3") # No bookmarks
    db_session.add_all([quote1, quote2, quote3])
    await db_session.commit()

    # Bookmark quote2 three times, quote1 once
    bm1 = Bookmark(user_id=user1.id, quote_id=quote2.id)
    bm2 = Bookmark(user_id=user2.id, quote_id=quote2.id)
    bm3 = Bookmark(user_id=user1.id, quote_id=quote1.id)
    # Simulating a third bookmark for quote2 from a different user
    user3 = User(email="popuser3@example.com", username="popuser3", hashed_password=hash_password("pw"))
    db_session.add(user3)
    await db_session.commit()
    bm4 = Bookmark(user_id=user3.id, quote_id=quote2.id)

    db_session.add_all([bm1, bm2, bm3, bm4])
    await db_session.commit()

    # 2. Act: Call the popular quotes endpoint
    response = await client.get("/quote/popular")

    # 3. Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2 # Only bookmarked quotes should be returned

    # Check the order
    assert data[0]["id"] == quote2.id
    assert data[1]["id"] == quote1.id

@pytest.mark.asyncio
async def test_create_quote_with_existing_source(client: httpx.AsyncClient):
    # First, create a user
    user_data = {"email": "test2@example.com", "username": "testuser2", "password": "password"}
    response = await client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    user_id = response.json()["user"]["id"]

    # Then, create a producer
    producer_data = {"name": "Test Producer", "pd_type": "publisher"}
    response = await client.post("/producers/", json=producer_data)
    assert response.status_code == 200
    producer_id = response.json()["id"]

    # Then, create a source
    source_data = {
        "title": "Another Test Book",
        "source_type": "book",
        "creator": "Another Test Author",
        "pd_id": producer_id,
        "data": {},
    }
    response = await client.post("/source/", json=source_data)
    assert response.status_code == 200
    source_id = response.json()["id"]

    # Then, create a quote with the existing source
    quote_data = {
        "content": "This is another test quote.",
        "user_id": user_id,
        "source_id": source_id,
    }
    response = await client.post("/quote/", json=quote_data)
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == quote_data["content"]
    assert data["user_id"] == quote_data["user_id"]
    assert data["source_id"] == source_id