from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_db
from app.schemas import UserCreate, Token, UserResponse
from app.services import user_service
from app.core.auth import (
    verify_password,
    create_access_token,
    verify_token,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# 회원가입
@router.post("/register", response_model=Token)
async def register(user_create: UserCreate, db: AsyncSession = Depends(get_async_db)):
    # 이메일 중복 확인
    if await user_service.repository.get_by_email(db, email=user_create.email):
        raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다.")

    # 새 사용자 생성
    db_user = await user_service.repository.create(db, obj_in=user_create)

    # 토큰 생성
    access_token = create_access_token(db_user.id)
    return Token(access_token=access_token, user=UserResponse.model_validate(db_user))


# 로그인
@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db),
):
    # 사용자 찾기
    user = await user_service.repository.get_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="메일 또는 비번이 틀립니다.")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="비활성화 계정입니다.")

    # 토큰 생성
    access_token = create_access_token(user.id)
    return Token(access_token=access_token, user=UserResponse.model_validate(user))


# 현재 사용자 정보
@router.get("/me", response_model=UserResponse)
async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_db)
):
    user_id = verify_token(token)
    user = await user_service.repository.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="없는 사용자입니다.")
    return UserResponse.model_validate(user)


# 로그아웃 (실제로는 클라이언트에서 토큰 삭제)
@router.post("/logout")
def logout():
    return {"message": "로그아웃 완료"}
