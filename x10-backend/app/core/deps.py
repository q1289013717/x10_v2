from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

ADMIN_TYPES = ["集团", "集团管理员", "分公司管理员", "admin", "manager", "管理员"]


def is_admin_user(user: User) -> bool:
    return user.role in ADMIN_TYPES


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    if user.status != "active":
        raise HTTPException(status_code=403, detail="账号已禁用")
    return user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not is_admin_user(current_user):
        raise HTTPException(status_code=403, detail="无管理员权限")
    return current_user


def get_optional_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """可选认证 - 用于允许匿名访问的接口"""
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id:
            return db.query(User).filter(User.id == user_id).first()
    except JWTError:
        pass
    return None
