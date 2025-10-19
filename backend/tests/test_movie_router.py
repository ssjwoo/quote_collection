import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_movie_crud(client: AsyncClient):
    # 1. Create a Movie
    movie_data = {
        "title": "The Test Movie",
        "director": "Test Director",
        "release_date": "2023-01-01"
    }
    response = await client.post("/movie/", json=movie_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "The Test Movie"
    assert data["director"] == "Test Director"
    movie_id = data["id"]

    # 2. Read the Movie
    response = await client.get(f"/movie/{movie_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "The Test Movie"

    # 3. Update the Movie
    update_data = {"title": "The Updated Test Movie"}
    response = await client.put(f"/movie/{movie_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "The Updated Test Movie"

    # 4. Delete the Movie
    response = await client.delete(f"/movie/{movie_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Movie deleted"

    # 5. Verify Deletion
    response = await client.get(f"/movie/{movie_id}")
    assert response.status_code == 404
