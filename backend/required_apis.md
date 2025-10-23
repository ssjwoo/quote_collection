
# Required APIs

This document outlines the required API endpoints for the quote collection application.

## Authentication

### POST /api/login
- **Description:** User login.
- **Request Body:**
  ```json
  {
    "username": "user1",
    "password": "password123"
  }
  ```
- **Response:**
  ```json
  {
    "token": "some-jwt-token"
  }
  ```

### POST /api/logout
- **Description:** User logout.

### POST /api/signup
- **Description:** User signup.
- **Request Body:**
  ```json
  {
    "name": "newuser",
    "email": "newuser@example.com",
    "password": "newpassword"
  }
  ```

### POST /api/users/check-name
- **Description:** Check if a username is already taken.
- **Request Body:**
  ```json
  {
    "name": "newuser"
  }
  ```
- **Response:**
  ```json
  {
    "isAvailable": true
  }
  ```

## Quotes

### GET /api/quotes
- **Description:** Get all quotes. Can be filtered by `popular`, `new`, and `recommended`.
- **Query Parameters:**
  - `filter`: `popular` | `new` | `recommended`
- **Response:**
  ```json
  [
    {
      "id": 1,
      "category": "book",
      "title": "The Little Prince",
      "creater": "Antoine de Saint-Exupéry",
      "content": "It is only with the heart that one can see rightly; what is essential is invisible to the eye.",
      "tags": ["philosophy", "love"],
      "writer": "user1",
      "createdAt": "2023-10-27T10:00:00Z"
    }
  ]
  ```

### GET /api/quotes/{id}
- **Description:** Get a specific quote by ID.
- **Response:**
  ```json
  {
    "id": 1,
    "category": "book",
    "title": "The Little Prince",
    "creater": "Antoine de Saint-Exupéry",
    "content": "It is only with the heart that one can see rightly; what is essential is invisible to the eye.",
    "tags": ["philosophy", "love"],
    "writer": "user1",
    "createdAt": "2023-10-27T10:00:00Z"
  }
  ```

### POST /api/quotes
- **Description:** Create a new quote.
- **Request Body:**
  ```json
  {
    "category": "movie",
    "title": "Forrest Gump",
    "creater": "Robert Zemeckis",
    "content": "Life is like a box of chocolates; you never know what you're gonna get.",
    "tags": ["life", "destiny"]
  }
  ```

### PUT /api/quotes/{id}
- **Description:** Update a quote.
- **Request Body:**
  ```json
  {
    "content": "Life was like a box of chocolates. You never know what you're gonna get."
  }
  ```

### DELETE /api/quotes/{id}
- **Description:** Delete a quote.

### GET /api/search
- **Description:** Search for quotes.
- **Query Parameters:**
  - `q`: search query
- **Response:**
  ```json
  [
    {
      "id": 1,
      "title": "The Little Prince",
      "content": "It is only with the heart that one can see rightly; what is essential is invisible to the eye."
    }
  ]
  ```

## User

### GET /api/users/{id}
- **Description:** Get user information.
- **Response:**
  ```json
  {
    "id": "user1",
    "email": "user1@example.com",
    "name": "User One"
  }
  ```

### PUT /api/users/{id}
- **Description:** Update user information.
- **Request Body:**
  ```json
  {
    "name": "User One Updated",
    "password": "newpassword123"
  }
  ```

### GET /api/users/{id}/quotes
- **Description:** Get all quotes uploaded by a user.
- **Response:**
  ```json
  [
    {
      "id": 1,
      "title": "The Little Prince",
      "content": "It is only with the heart that one can see rightly; what is essential is invisible to the eye.",
      "creater": "Antoine de Saint-Exupéry",
      "createdAt": "2023-10-27T10:00:00Z"
    }
  ]
  ```

### GET /api/users/{id}/bookmarks
- **Description:** Get all bookmarks of a user.
- **Response:**
  ```json
  [
    {
      "id": 2,
      "title": "Forrest Gump",
      "content": "Life is like a box of chocolates; you never know what you're gonna get."
    }
  ]
  ```

### POST /api/users/{id}/bookmarks
- **Description:** Add a bookmark.
- **Request Body:**
  ```json
  {
    "quoteId": 2
  }
  ```

### DELETE /api/users/{id}/bookmarks/{quoteId}
- **Description:** Remove a bookmark.

## Recommendations

### GET /api/recommendations/user-based
- **Description:** Get user-based recommended quotes.
- **Response:**
  ```json
  [
    {
      "id": 3,
      "content": "The only way to do great work is to love what you do."
    }
  ]
  ```
