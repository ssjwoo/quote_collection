import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, Source, Quote, Tag, Book, Movie, Drama, Producer
from app.core.auth import hash_password

@pytest.mark.asyncio
async def test_search(client: AsyncClient, db_session: AsyncSession):
    # 1. Setup: Create test data
    user = User(email="test@example.com", username="testuser", hashed_password=hash_password("password"))
    db_session.add(user)
    await db_session.commit()

    # Create a producer for drama
    producer = Producer(name="Test Producer", pd_type="broadcast")
    db_session.add(producer)
    await db_session.commit()

    # Create specific detail objects
    book = Book(title="The Great Book", author="Great Author", isbn="1111111111")
    movie = Movie(title="The Great Movie", director="Great Director", release_date="2020-01-01")
    drama = Drama(title="The Great Drama", producer_id=producer.id, release_date="2021-01-01")
    db_session.add_all([book, movie, drama])
    await db_session.commit()

    # Create Sources linked to details
    source_book = Source(title=book.title, source_type="book", creator=book.author, details_id=book.id)
    source_movie = Source(title=movie.title, source_type="movie", creator=movie.director, details_id=movie.id)
    source_drama = Source(title=drama.title, source_type="tv", creator="Drama Creator", details_id=drama.id)
    db_session.add_all([source_book, source_movie, source_drama])
    await db_session.commit()

    quote1 = Quote(user_id=user.id, source_id=source_book.id, content="A quote from the great book.")
    quote2 = Quote(user_id=user.id, source_id=source_movie.id, content="A quote from the great movie.")
    tag1 = Tag(name="great")
    tag2 = Tag(name="bookish")
    db_session.add_all([quote1, quote2, tag1, tag2])
    await db_session.commit()

    # 2. Act: Perform the search
    # Search for a quote content
    response = await client.get("/search/?q=book")
    assert response.status_code == 200
    data = response.json()
    assert len(data["quotes"]) == 1
    assert data["quotes"][0]["content"] == "A quote from the great book."
    assert data["quotes"][0]["source_id"] == source_book.id
    assert len(data["sources"]) == 1
    assert data["sources"][0]["title"] == book.title
    assert data["sources"][0]["details"]["author"] == book.author
    assert len(data["tags"]) == 1
    assert data["tags"][0]["name"] == "bookish"

    # Search for a movie title
    response = await client.get("/search/?q=movie")
    assert response.status_code == 200
    data = response.json()
    assert len(data["quotes"]) == 1
    assert data["quotes"][0]["content"] == "A quote from the great movie."
    assert len(data["sources"]) == 1
    assert data["sources"][0]["title"] == movie.title
    assert data["sources"][0]["details"]["director"] == movie.director

    # Search for a tag
    response = await client.get("/search/?q=great")
    assert response.status_code == 200
    data = response.json()
    assert len(data["tags"]) == 1
    assert data["tags"][0]["name"] == "great"

    # Search for something that doesn't exist
    response = await client.get("/search/?q=nonexistent")
    assert response.status_code == 200
    data = response.json()
    assert len(data["quotes"]) == 0
    assert len(data["sources"]) == 0
    assert len(data["tags"]) == 0

    # Search for book by author
    response = await client.get("/search/?q=Great Author")
    assert response.status_code == 200
    data = response.json()
    assert len(data["sources"]) == 1
    assert data["sources"][0]["title"] == "The Great Book"

    # Search for movie by director
    response = await client.get("/search/?q=Great Director")
    assert response.status_code == 200
    data = response.json()
    assert len(data["sources"]) == 1
    assert data["sources"][0]["title"] == "The Great Movie"

    # Search for drama by producer
    response = await client.get("/search/?q=Test Producer")
    assert response.status_code == 200
    data = response.json()
    assert len(data["sources"]) == 1
    assert data["sources"][0]["title"] == "The Great Drama"

    # Search for book by author
    response = await client.get("/search/?q=Great Author")
    assert response.status_code == 200
    data = response.json()
    assert len(data["sources"]) == 1
    assert data["sources"][0]["title"] == "The Great Book"

    # Search for movie by director
    response = await client.get("/search/?q=Great Director")
    assert response.status_code == 200
    data = response.json()
    assert len(data["sources"]) == 1
    assert data["sources"][0]["title"] == "The Great Movie"

    # Search for drama by producer
    response = await client.get("/search/?q=Test Producer")
    assert response.status_code == 200
    data = response.json()
    assert len(data["sources"]) == 1
    assert data["sources"][0]["title"] == "The Great Drama"
