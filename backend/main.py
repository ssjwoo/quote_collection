from fastapi import FastAPI
from app.routers import router as api_router
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import uvicorn
from contextlib import asynccontextmanager
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy import create_engine
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database if it doesn't exist
    engine = create_engine(settings.sync_database_url)
    if not database_exists(engine.url):
        create_database(engine.url)

    # Run alembic migrations
    subprocess.run(["alembic", "upgrade", "head"])
    yield


app = FastAPI(lifespan=lifespan)


# 허용할 출처 목록
origins = [
    "http://localhost:5173",  # React 개발 서버 주소
    "https://gen-lang-client-0121173096.web.app", # Firebase Hosting
    "https://gen-lang-client-0121173096.firebaseapp.com", # Firebase Secondary Domain
    "null",  # 로컬에서 직접 연 html 파일 (test.html)
]
# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ["*"] 대신 위에서 만든 origins 리스트를 사용
    # allow_origins=["*"],  # frontend IP 로 추후 바꾸기
    allow_credentials=True,
    allow_methods=["*"],  # 모든 method 허용
    allow_headers=["*"],  # 모든 header 허용
)


# Force reload for AI debug - version 2
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8081, reload=True)
