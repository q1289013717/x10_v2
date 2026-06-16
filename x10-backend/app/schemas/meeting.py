from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MeetingCreate(BaseModel):
    title: str
    content: str = ""
    question: str = ""


class MeetingUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    question: Optional[str] = None


class MeetingResponse(BaseModel):
    id: str
    title: str
    content: str
    question: str
    created_by: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class MeetingAnswerCreate(BaseModel):
    meeting_id: str
    answer: str


class MeetingAnswerResponse(BaseModel):
    id: str
    meeting_id: str
    user_id: str
    user_name: str
    answer: str
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class SystemConfigUpdate(BaseModel):
    config_key: str
    config_value: str
