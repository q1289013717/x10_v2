from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.meeting import Meeting, MeetingAnswer, SystemConfig


# ========== 会议/共识档案 ==========

def get_meetings(db: Session, skip: int = 0, limit: int = 50) -> List[Meeting]:
    return db.query(Meeting).order_by(Meeting.created_at.desc()).offset(skip).limit(limit).all()


def get_meeting_by_id(db: Session, meeting_id: str) -> Optional[Meeting]:
    return db.query(Meeting).filter(Meeting.id == meeting_id).first()


def create_meeting(db: Session, title: str, content: str = "",
                   question: str = "", created_by: str = "") -> Meeting:
    meeting = Meeting(title=title, content=content, question=question, created_by=created_by)
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    return meeting


def update_meeting(db: Session, meeting_id: str, **kwargs) -> Optional[Meeting]:
    meeting = get_meeting_by_id(db, meeting_id)
    if not meeting:
        return None
    for key, value in kwargs.items():
        if hasattr(meeting, key) and value is not None:
            setattr(meeting, key, value)
    db.commit()
    db.refresh(meeting)
    return meeting


def delete_meeting(db: Session, meeting_id: str) -> bool:
    meeting = get_meeting_by_id(db, meeting_id)
    if not meeting:
        return False
    # 级联删除答题
    db.query(MeetingAnswer).filter(MeetingAnswer.meeting_id == meeting_id).delete()
    db.delete(meeting)
    db.commit()
    return True


# ========== 会议答题 ==========

def get_meeting_answers(db: Session, meeting_id: str) -> List[MeetingAnswer]:
    return db.query(MeetingAnswer).filter(
        MeetingAnswer.meeting_id == meeting_id
    ).order_by(MeetingAnswer.created_at.desc()).all()


def create_meeting_answer(db: Session, meeting_id: str, user_id: str,
                          user_name: str, answer: str) -> MeetingAnswer:
    # 同一用户同一会议只保留最新答案
    existing = db.query(MeetingAnswer).filter(
        MeetingAnswer.meeting_id == meeting_id,
        MeetingAnswer.user_id == user_id,
    ).first()
    if existing:
        existing.answer = answer
        existing.user_name = user_name
        db.commit()
        db.refresh(existing)
        return existing

    ans = MeetingAnswer(
        meeting_id=meeting_id, user_id=user_id,
        user_name=user_name, answer=answer,
    )
    db.add(ans)
    db.commit()
    db.refresh(ans)
    return ans


# ========== 系统配置 ==========

def get_config(db: Session, config_key: str) -> Optional[str]:
    config = db.query(SystemConfig).filter(SystemConfig.config_key == config_key).first()
    return config.config_value if config else None


def set_config(db: Session, config_key: str, config_value: str, updated_by: str = "") -> SystemConfig:
    config = db.query(SystemConfig).filter(SystemConfig.config_key == config_key).first()
    if config:
        config.config_value = config_value
        config.updated_by = updated_by
    else:
        config = SystemConfig(config_key=config_key, config_value=config_value, updated_by=updated_by)
        db.add(config)
    db.commit()
    db.refresh(config)
    return config


def get_all_configs(db: Session) -> dict:
    configs = db.query(SystemConfig).all()
    return {c.config_key: c.config_value for c in configs}
