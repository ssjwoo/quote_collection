from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# 회원가입 요청
class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3)
    password: str = Field(min_length=6)


# 로그인 요청
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# 사용자 정보 수정
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3)
    password: Optional[str] = Field(None, min_length=6)
    is_active: Optional[bool] = None


# 사용자 응답 (비밀번호 제외)
class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# JWT 토큰 응답
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
