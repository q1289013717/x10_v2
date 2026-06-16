import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    account = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)  # bcrypt hash
    role = Column(String(50), nullable=False, default="员工")  # 集团管理员, 分公司管理员, 员工
    company = Column(String(200), default="")
    status = Column(String(20), default="active")  # active, disabled
    avatar = Column(String(10), default="U")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "account": self.account,
            "name": self.name,
            "role": self.role,
            "company": self.company,
            "status": self.status,
            "avatar": self.avatar,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def to_safe_dict(self):
        """不含密码的字典"""
        d = self.to_dict()
        d.pop("password", None)
        return d
