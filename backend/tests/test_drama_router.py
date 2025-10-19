import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Producer # Dramas need a producer

@pytest.mark.asyncio
async def test_drama_crud(client: AsyncClient, db_session: AsyncSession):
    # 1. Create a prerequisite Producer
    producer = Producer(name="Test Producer", pd_type="broadcast")
    db_session.add(producer)
    await db_session.commit()

    # 2. Create a Drama
    drama_data = {
        "title": "The Test Drama",
        "producer_id": producer.id,
        "release_date": "2024-01-01"
    }
    response = await client.post("/drama/", json=drama_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "The Test Drama"
    assert data["producer_id"] == producer.id
    drama_id = data["id"]

    # 3. Read the Drama
    response = await client.get(f"/drama/{drama_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "The Test Drama"

    # 4. Update the Drama
    update_data = {"title": "The Updated Test Drama"}
    response = await client.put(f"/drama/{drama_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "The Updated Test Drama"

    # 5. Delete the Drama
    response = await client.delete(f"/drama/{drama_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Drama deleted"

    # 6. Verify Deletion
    response = await client.get(f"/drama/{drama_id}")
    assert response.status_code == 404
