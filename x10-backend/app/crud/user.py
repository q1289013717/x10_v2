from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.user import User
from app.core.security import get_password_hash, verify_password


def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_account(db: Session, account: str) -> Optional[User]:
    return db.query(User).filter(User.account == account).first()


def get_all_users(db: Session, include_disabled: bool = False) -> List[User]:
    q = db.query(User)
    if not include_disabled:
        q = q.filter(User.status == "active")
    return q.order_by(User.created_at.desc()).all()


def create_user(db: Session, account: str, name: str, password: str,
                role: str = "员工", company: str = "", avatar: str = "U") -> User:
    hashed_pw = get_password_hash(password)
    user = User(
        account=account,
        name=name,
        password=hashed_pw,
        role=role,
        company=company,
        avatar=avatar or name[0].upper() if name else "U",
        status="active",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: str, **kwargs) -> Optional[User]:
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    if "password" in kwargs and kwargs["password"]:
        kwargs["password"] = get_password_hash(kwargs["password"])
    for key, value in kwargs.items():
        if hasattr(user, key) and value is not None:
            setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: str) -> bool:
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True


def authenticate_user(db: Session, account: str, password: str) -> Optional[User]:
    user = get_user_by_account(db, account)
    if not user:
        return None
    if user.status != "active":
        return None
    if not verify_password(password, user.password):
        return None
    return user


def change_password(db: Session, user_id: str, old_password: str, new_password: str) -> bool:
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    if not verify_password(old_password, user.password):
        return False
    user.password = get_password_hash(new_password)
    db.commit()
    return True
