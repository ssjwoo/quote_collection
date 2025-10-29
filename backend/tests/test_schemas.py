import pytest
from datetime import datetime, timezone
from pydantic import ValidationError
from app.schemas import UserCreate, UserUpdate, UserResponse, Token, BookCreate, BookUpdate, BookRead, BookmarkRead, BookmarkCreate

def test_user_create_schema():
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "securepassword",
    }
    user = UserCreate(**user_data)
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.password == "securepassword"

    with pytest.raises(ValidationError):
        UserCreate(email="invalid-email", username="user", password="pass")
    with pytest.raises(ValidationError):
        UserCreate(email="test@example.com", username="", password="pass")
    with pytest.raises(ValidationError):
        UserCreate(email="test@example.com", username="user", password="short")

def test_user_update_schema():
    user_update_data = {"email": "new@example.com", "username": "newuser"}
    user_update = UserUpdate(**user_update_data)
    assert user_update.email == "new@example.com"
    assert user_update.username == "newuser"
    assert user_update.password is None

    user_update_data = {"password": "newsecurepassword"}
    user_update = UserUpdate(**user_update_data)
    assert user_update.password == "newsecurepassword"
    assert user_update.email is None

def test_user_response_schema():
    now = datetime.now(timezone.utc)
    user_response_data = {
        "id": 1,
        "email": "response@example.com",
        "username": "respuser",
        "is_active": True,
        "created_at": now,
    }
    user_response = UserResponse(**user_response_data)
    assert user_response.id == 1
    assert user_response.email == "response@example.com"
    assert user_response.username == "respuser"
    assert user_response.is_active is True
    assert user_response.created_at == now

def test_token_schema():
    now = datetime.now(timezone.utc)
    user_response_data = {
        "id": 1,
        "email": "token@example.com",
        "username": "tokenuser",
        "is_active": True,
        "created_at": now,
    }
    token_data = {
        "access_token": "some_access_token",
        "token_type": "bearer",
        "user": user_response_data,
    }
    token = Token(**token_data)
    assert token.access_token == "some_access_token"
    assert token.token_type == "bearer"
    assert token.user.email == "token@example.com"

def test_book_create_schema():
    book_data = {"title": "Test Book", "author": "Test Author", "publisher_id": 1}
    book = BookCreate(**book_data)
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.publisher_id == 1

    with pytest.raises(ValidationError):
        BookCreate(title="", author="Author")

def test_book_update_schema():
    book_update_data = {"title": "New Title", "author": "New Author"}
    book_update = BookUpdate(**book_update_data)
    assert book_update.title == "New Title"
    assert book_update.author == "New Author"
    assert book_update.publisher_id is None

def test_book_read_schema():
    now = datetime.now(timezone.utc)
    publisher_data = {"id": 1, "name": "Read Publisher"}
    book_read_data = {
        "id": 1,
        "title": "Read Book",
        "author": "Read Author",
        "publisher": publisher_data,
        "created_at": now,
    }
    book_read = BookRead(**book_read_data)
    assert book_read.id == 1
    assert book_read.title == "Read Book"
    assert book_read.author == "Read Author"
    assert book_read.publisher.name == "Read Publisher"
    assert book_read.created_at == now

def test_bookmark_create_schema():
    bookmark_data = {"user_id": 1, "quote_id": 1}
    bookmark = BookmarkCreate(**bookmark_data)
    assert bookmark.user_id == 1
    assert bookmark.quote_id == 1

def test_bookmark_read_schema():
    now = datetime.now(timezone.utc)
    bookmark_read_data = {
        "user_id": 1,
        "quote_id": 1,
        "created_at": now,
    }
    bookmark_read = BookmarkRead(**bookmark_read_data)
    assert bookmark_read.user_id == 1
    assert bookmark_read.quote_id == 1
    assert bookmark_read.created_at == now

