# Use the official Python image
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for MySQL client and Vertex AI/Torch issues
RUN apt-get update && apt-get install -y \
    build-essential \
    libmariadb-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from backend directory
COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir uvicorn fastapi python-multipart email-validator pyjwt[crypto] passlib[bcrypt]

# Copy application code (backend and llm)
COPY backend /app/backend
COPY llm /app/llm

# Set working directory to backend so uvicorn finds main:app easily
WORKDIR /app/backend

# Expose port and start
ENV PORT 8080
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
