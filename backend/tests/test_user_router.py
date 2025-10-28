import pytest
import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, Quote, Source
from app.core.auth import hash_password

@pytest.mark.asyncio
async def test_check_username_available(client: httpx.AsyncClient, db_session: AsyncSession):
    # Create a user to make a username unavailable
    user = User(email="test_check_name@example.com", username="existinguser", hashed_password=hash_password("password"))
    db_session.add(user)
    await db_session.commit()

    # Test available username
    response = await client.post("/users/check-name", json={"username": "newuser"})
    assert response.status_code == 200
    assert response.json() == {"is_available": True}

    # Test unavailable username
    response = await client.post("/users/check-name", json={"username": "existinguser"})
    assert response.status_code == 200
    assert response.json() == {"is_available": False}

@pytest.mark.asyncio
async def test_get_user_quotes(client: httpx.AsyncClient, db_session: AsyncSession):
    # Create a user
    user = User(email="user_quotes@example.com", username="userquotes", hashed_password=hash_password("password"))
    db_session.add(user)
    await db_session.commit()

    # Create a source
    source = Source(title="Test Book for Quotes", source_type="book", creator="Test Author")
    db_session.add(source)
    await db_session.commit()

    # Create quotes for the user
    quote1 = Quote(user_id=user.id, source_id=source.id, content="User Quote 1")
    quote2 = Quote(user_id=user.id, source_id=source.id, content="User Quote 2")
    db_session.add_all([quote1, quote2])
    await db_session.commit()

    # Create a quote for another user
    other_user = User(email="other_user@example.com", username="otheruser", hashed_password=hash_password("password"))
    db_session.add(other_user)
    await db_session.commit()
    other_quote = Quote(user_id=other_user.id, source_id=source.id, content="Other User Quote")
    db_session.add(other_quote)
    await db_session.commit()

    # Get quotes for the user
    response = await client.get(f"/users/{user.id}/quotes")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["content"] == "User Quote 1"
    assert data[1]["content"] == "User Quote 2"

    # Test non-existent user
    response = await client.get("/users/99999/quotes")
    assert response.status_code == 404
