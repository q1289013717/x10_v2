from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.deps import get_current_user, get_current_admin_user
from app.models.user import User
from app.schemas.meeting import (
    MeetingCreate, MeetingUpdate, MeetingResponse,
    MeetingAnswerCreate, MeetingAnswerResponse,
    SystemConfigUpdate,
)
from app.crud import meeting as meeting_crud

router = APIRouter(prefix="/api/meetings", tags=["共识档案"])


@router.get("", response_model=list[MeetingResponse])
def list_meetings(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    meetings = meeting_crud.get_meetings(db, skip=skip, limit=limit)
    return [MeetingResponse.model_validate(m.to_dict()) for m in meetings]


@router.get("/{meeting_id}", response_model=MeetingResponse)
def get_meeting(meeting_id: str,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    meeting = meeting_crud.get_meeting_by_id(db, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="会议不存在")
    return MeetingResponse.model_validate(meeting.to_dict())


@router.post("", response_model=MeetingResponse)
def create_meeting(meeting_data: MeetingCreate,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    meeting = meeting_crud.create_meeting(
        db,
        title=meeting_data.title,
        content=meeting_data.content,
        question=meeting_data.question,
        created_by=current_user.id,
    )
    return MeetingResponse.model_validate(meeting.to_dict())


@router.put("/{meeting_id}", response_model=MeetingResponse)
def update_meeting(meeting_id: str, meeting_data: MeetingUpdate,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    update_data = meeting_data.model_dump(exclude_unset=True)
    meeting = meeting_crud.update_meeting(db, meeting_id, **update_data)
    if not meeting:
        raise HTTPException(status_code=404, detail="会议不存在")
    return MeetingResponse.model_validate(meeting.to_dict())


@router.delete("/{meeting_id}")
def delete_meeting(meeting_id: str,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_admin_user)):
    success = meeting_crud.delete_meeting(db, meeting_id)
    if not success:
        raise HTTPException(status_code=404, detail="会议不存在")
    return {"message": "删除成功"}


# ========== 会议答题 ==========

@router.get("/{meeting_id}/answers", response_model=list[MeetingAnswerResponse])
def get_meeting_answers(meeting_id: str,
                        db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    answers = meeting_crud.get_meeting_answers(db, meeting_id)
    return [MeetingAnswerResponse.model_validate(a.to_dict()) for a in answers]


@router.post("/{meeting_id}/answers", response_model=MeetingAnswerResponse)
def submit_meeting_answer(meeting_id: str, answer_data: MeetingAnswerCreate,
                          db: Session = Depends(get_db),
                          current_user: User = Depends(get_current_user)):
    ans = meeting_crud.create_meeting_answer(
        db,
        meeting_id=meeting_id,
        user_id=current_user.id,
        user_name=current_user.name,
        answer=answer_data.answer,
    )
    return MeetingAnswerResponse.model_validate(ans.to_dict())


# ========== 系统配置 ==========

router_config = APIRouter(prefix="/api/config", tags=["系统配置"])


@router_config.get("")
def get_configs(db: Session = Depends(get_db)):
    return meeting_crud.get_all_configs(db)


@router_config.get("/{config_key}")
def get_config(config_key: str, db: Session = Depends(get_db)):
    value = meeting_crud.get_config(db, config_key)
    return {"key": config_key, "value": value or ""}


@router_config.put("")
def set_config(config_data: SystemConfigUpdate,
               db: Session = Depends(get_db),
               current_user: User = Depends(get_current_admin_user)):
    config = meeting_crud.set_config(
        db, config_data.config_key, config_data.config_value, current_user.id,
    )
    return config.to_dict()
