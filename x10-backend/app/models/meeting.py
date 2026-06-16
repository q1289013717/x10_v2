import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text
from app.core.database import Base


class Meeting(Base):
    """共识档案 - 会议记录"""
    __tablename__ = "meetings"

    id = Column(String, primary_key=True, default=lambda: f"meeting_{uuid.uuid4().hex[:12]}")
    title = Column(String(500), nullable=False)
    content = Column(Text, default="")
    question = Column(Text, default="")  # 会议提问
    created_by = Column(String(100), default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "question": self.question,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class MeetingAnswer(Base):
    """会议答题"""
    __tablename__ = "meeting_answers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    meeting_id = Column(String(100), nullable=False, index=True)
    user_id = Column(String(100), nullable=False)
    user_name = Column(String(100), default="")
    answer = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "meeting_id": self.meeting_id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "answer": self.answer,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class SystemConfig(Base):
    """系统配置"""
    __tablename__ = "system_configs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    config_key = Column(String(100), unique=True, nullable=False, index=True)
    config_value = Column(Text, default="")
    updated_by = Column(String(100), default="")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "config_key": self.config_key,
            "config_value": self.config_value,
            "updated_by": self.updated_by,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
