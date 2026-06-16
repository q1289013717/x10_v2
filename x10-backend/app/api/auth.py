from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.database import get_db
from app.core.security import create_access_token, get_password_hash
from app.core.deps import get_current_user, get_current_admin_user
from app.core.config import settings
from app.models.user import User
from app.schemas.user import (
    UserCreate, UserUpdate, UserResponse, LoginRequest, TokenResponse,
    ChangePasswordRequest,
)
from app.crud import user as user_crud

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = user_crud.authenticate_user(db, request.account, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="账号或密码错误")

    expires_delta = timedelta(days=30) if request.remember_me else None
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=expires_delta,
    )
    return TokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user.to_safe_dict()),
    )


@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing = user_crud.get_user_by_account(db, user_data.account)
    if existing:
        raise HTTPException(status_code=400, detail="账号已存在")
    user = user_crud.create_user(
        db, account=user_data.account, name=user_data.name,
        password=user_data.password, role=user_data.role,
        company=user_data.company,
    )
    return UserResponse.model_validate(user.to_safe_dict())


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user.to_safe_dict())


@router.put("/me/password")
def change_my_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    success = user_crud.change_password(
        db, current_user.id, request.old_password, request.new_password,
    )
    if not success:
        raise HTTPException(status_code=400, detail="原密码错误")
    return {"message": "密码修改成功"}


@router.get("/users", response_model=list[UserResponse])
def list_users(current_user: User = Depends(get_current_admin_user),
               db: Session = Depends(get_db)):
    users = user_crud.get_all_users(db)
    return [UserResponse.model_validate(u.to_safe_dict()) for u in users]


@router.post("/users", response_model=UserResponse)
def create_user_api(user_data: UserCreate,
                    current_user: User = Depends(get_current_admin_user),
                    db: Session = Depends(get_db)):
    existing = user_crud.get_user_by_account(db, user_data.account)
    if existing:
        raise HTTPException(status_code=400, detail="账号已存在")
    user = user_crud.create_user(
        db, account=user_data.account, name=user_data.name,
        password=user_data.password, role=user_data.role,
        company=user_data.company,
    )
    return UserResponse.model_validate(user.to_safe_dict())


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user_api(user_id: str, user_data: UserUpdate,
                    current_user: User = Depends(get_current_admin_user),
                    db: Session = Depends(get_db)):
    update_data = user_data.model_dump(exclude_unset=True)
    user = user_crud.update_user(db, user_id, **update_data)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return UserResponse.model_validate(user.to_safe_dict())


@router.delete("/users/{user_id}")
def delete_user_api(user_id: str,
                    current_user: User = Depends(get_current_admin_user),
                    db: Session = Depends(get_db)):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="不能删除自己")
    success = user_crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"message": "删除成功"}
