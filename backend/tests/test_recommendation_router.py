import pytest
import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, Source, Quote, Bookmark
from app.core.auth import hash_password

@pytest.mark.asyncio
async def test_get_user_based_recommendations(client: httpx.AsyncClient, db_session: AsyncSession):
    # 1. Create a user and log in
    user_data = {"email": "reco_user@example.com", "username": "recouser", "password": "password"}
    response = await client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    user_id = response.json()["user"]["id"]

    headers = {"Authorization": f"Bearer {token}"}

    # Create another user
    other_user = User(email="other_reco_user@example.com", username="otherrecouser", hashed_password=hash_password("password"))
    db_session.add(other_user)
    await db_session.commit()

    # 2. Create sources
    source1 = Source(title="Source A", source_type="book", creator="Author A")
    source2 = Source(title="Source B", source_type="book", creator="Author B")
    source3 = Source(title="Source C", source_type="book", creator="Author C")
    db_session.add_all([source1, source2, source3])
    await db_session.commit()

    # 3. Create quotes
    # Quotes from Source A (user's own and other user's)
    quote1_s1_user = Quote(user_id=user_id, source_id=source1.id, content="User's Quote 1 from Source A")
    quote2_s1_other = Quote(user_id=other_user.id, source_id=source1.id, content="Other User's Quote 2 from Source A")
    # Quotes from Source B (user's own and other user's)
    quote3_s2_user = Quote(user_id=user_id, source_id=source2.id, content="User's Quote 1 from Source B")
    quote4_s2_other = Quote(user_id=other_user.id, source_id=source2.id, content="Other User's Quote 2 from Source B")
    # Quotes from Source C (not bookmarked by user)
    quote5_s3_user = Quote(user_id=user_id, source_id=source3.id, content="User's Quote 1 from Source C")
    db_session.add_all([quote1_s1_user, quote2_s1_other, quote3_s2_user, quote4_s2_other, quote5_s3_user])
    await db_session.commit()

    # 4. Create bookmarks for the user (bookmark quote1_s1_user and quote3_s2_user)
    bookmark1 = Bookmark(user_id=user_id, quote_id=quote1_s1_user.id)
    bookmark2 = Bookmark(user_id=user_id, quote_id=quote3_s2_user.id)
    db_session.add_all([bookmark1, bookmark2])
    await db_session.commit()

    # 5. Call the recommendations endpoint
    response = await client.get("/recommendations/user-based", headers=headers)
    assert response.status_code == 200
    data = response.json()

    # Expected recommendations: quote2_s1_other (from Source A, not bookmarked, not user's own)
    # and quote4_s2_other (from Source B, not bookmarked, not user's own)
    recommended_quote_ids = {q["id"] for q in data}
    assert len(recommended_quote_ids) == 2
    assert quote2_s1_other.id in recommended_quote_ids
    assert quote4_s2_other.id in recommended_quote_ids
    assert quote1_s1_user.id not in recommended_quote_ids
    assert quote3_s2_user.id not in recommended_quote_ids
    assert quote5_s3_user.id not in recommended_quote_ids

@pytest.mark.asyncio
async def test_get_user_based_recommendations_no_bookmarks(client: httpx.AsyncClient, db_session: AsyncSession):
    # 1. Create a user and log in
    user_data = {"email": "reco_user_no_bm@example.com", "username": "recousernobm", "password": "password"}
    response = await client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    user_id = response.json()["user"]["id"]

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create sources and quotes for popular quotes
    source_pop = Source(title="Popular Source", source_type="book", creator="Popular Author")
    db_session.add(source_pop)
    await db_session.commit()

    pop_quote1 = Quote(user_id=user_id, source_id=source_pop.id, content="Popular Quote 1")
    pop_quote2 = Quote(user_id=user_id, source_id=source_pop.id, content="Popular Quote 2")
    db_session.add_all([pop_quote1, pop_quote2])
    await db_session.commit()

    # Create bookmarks for popular quotes (by other users to make them popular)
    other_user1 = User(email="other_pop_user1@example.com", username="otherpopuser1", hashed_password=hash_password("pw"))
    other_user2 = User(email="other_pop_user2@example.com", username="otherpopuser2", hashed_password=hash_password("pw"))
    db_session.add_all([other_user1, other_user2])
    await db_session.commit()

    bm_pop1 = Bookmark(user_id=other_user1.id, quote_id=pop_quote1.id)
    bm_pop2 = Bookmark(user_id=other_user2.id, quote_id=pop_quote1.id) # pop_quote1 has 2 bookmarks
    bm_pop3 = Bookmark(user_id=other_user1.id, quote_id=pop_quote2.id) # pop_quote2 has 1 bookmark
    db_session.add_all([bm_pop1, bm_pop2, bm_pop3])
    await db_session.commit()

    # 3. Call the recommendations endpoint for a user with no bookmarks
    response = await client.get("/recommendations/user-based", headers=headers)
    assert response.status_code == 200
    data = response.json()

    # Should return popular quotes, ordered by popularity
    assert len(data) == 2
    assert data[0]["id"] == pop_quote1.id
    assert data[1]["id"] == pop_quote2.id
