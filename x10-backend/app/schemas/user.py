from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ========== 用户/Auth ==========
class UserBase(BaseModel):
    account: str
    name: str
    role: str = "员工"
    company: str = ""


class UserCreate(UserBase):
    password: str = Field(..., min_length=1)


class UserUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    company: Optional[str] = None
    status: Optional[str] = None
    password: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    account: str
    name: str
    role: str
    company: str
    status: str
    avatar: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    account: str
    password: str
    remember_me: bool = False


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
