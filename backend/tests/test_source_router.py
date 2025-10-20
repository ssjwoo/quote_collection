from app.services import source_service

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Book, Movie, Drama, Producer, Source
from app.core.auth import hash_password


@pytest.mark.asyncio
async def test_source_crud_with_details(client: AsyncClient, db_session: AsyncSession):
    # 1. Create a Producer for Drama
    producer = Producer(name="Test Producer", pd_type="broadcast")
    db_session.add(producer)
    await db_session.commit()

    # 2. Create specific detail objects
    book = Book(title="Test Book", author="Test Author", isbn="1234567890")
    movie = Movie(
        title="Test Movie", director="Test Director", release_date="2023-01-01"
    )
    drama = Drama(
        title="Test Drama", producer_id=producer.id, release_date="2022-01-01"
    )
    db_session.add_all([book, movie, drama])
    await db_session.commit()

    # 3. Create Sources linked to details
    source_book_data = {
        "title": book.title,
        "source_type": "book",
        "creator": book.author,
        "details_id": book.id,
    }
    response = await client.post("/source/", json=source_book_data)
    assert response.status_code == 200
    source_book = response.json()
    assert source_book["title"] == book.title
    assert source_book["source_type"] == "book"
    assert source_book["details_id"] == book.id
    assert source_book["details"]["title"] == book.title
    assert source_book["details"]["author"] == book.author

    source_movie_data = {
        "title": movie.title,
        "source_type": "movie",
        "creator": movie.director,
        "details_id": movie.id,
    }
    response = await client.post("/source/", json=source_movie_data)
    assert response.status_code == 200
    source_movie = response.json()
    assert source_movie["title"] == movie.title
    assert source_movie["source_type"] == "movie"
    assert source_movie["details_id"] == movie.id
    assert source_movie["details"]["title"] == movie.title
    assert source_movie["details"]["director"] == movie.director

    source_drama_data = {
        "title": drama.title,
        "source_type": "tv",  # Using 'tv' for drama
        "creator": "Vince Gilligan",  # Creator for drama
        "details_id": drama.id,
    }
    response = await client.post("/source/", json=source_drama_data)
    assert response.status_code == 200
    source_drama = response.json()
    assert source_drama["title"] == drama.title
    assert source_drama["source_type"] == "tv"
    assert source_drama["details_id"] == drama.id
    assert source_drama["details"]["title"] == drama.title
    assert source_drama["details"]["producer_id"] == drama.producer_id

    # 4. Get a single Source with details
    response = await client.get(f"/source/{source_book["id"]}")
    assert response.status_code == 200
    retrieved_source = response.json()
    assert retrieved_source["id"] == source_book["id"]
    assert retrieved_source["details"]["title"] == book.title

    # 5. List all Sources with details
    response = await client.get("/source/")
    assert response.status_code == 200
    listed_sources = response.json()
    assert len(listed_sources) == 3
    # Check that details are present for at least one
    assert any(s["details"] is not None for s in listed_sources)

    # 6. Update a Source (only generic fields)
    update_data = {"title": "Updated Book Title"}
    response = await client.put(f"/source/{source_book["id"]}", json=update_data)
    await db_session.commit()  # Explicitly commit the session
    assert response.status_code == 200
    # Retrieve the updated source from the database to get a mapped instance with details
    updated_source_with_details = await source_service.get_with_details(
        db_session, source_id=source_book["id"]
    )
    assert updated_source_with_details is not None
    assert updated_source_with_details.title == "Updated Book Title"
    assert (
        updated_source_with_details.details.title == book.title
    )  # Specific detail title should remain original    # 7. Delete a Source
    response = await client.delete(f"/source/{source_book["id"]}")
    assert response.status_code == 200
    assert response.json()["message"] == "소스 삭제 완료"

    # 8. Verify deletion
    response = await client.get(f"/source/{source_book["id"]}")
    assert response.status_code == 404
