from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.deps import get_current_user, is_admin_user
from app.models.user import User
from app.schemas.influencer import (
    InfluencerRecordCreate, InfluencerRecordUpdate, InfluencerRecordResponse,
    InfluencerSummaryResponse,
)
from app.crud import influencer as influencer_crud

router = APIRouter(prefix="/api/influencers", tags=["达人合作台账"])


@router.get("/records", response_model=list[InfluencerRecordResponse])
def list_records(
    start_date: Optional[str] = Query(default=None),
    end_date: Optional[str] = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    records = influencer_crud.get_influencer_records(
        db,
        user_id=current_user.id,
        is_admin=is_admin_user(current_user),
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit,
    )
    return [InfluencerRecordResponse.model_validate(r.to_dict()) for r in records]


@router.get("/summary", response_model=InfluencerSummaryResponse)
def get_summary(
    start_date: Optional[str] = Query(default=None),
    end_date: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    summary = influencer_crud.get_influencer_summary(
        db,
        user_id=current_user.id,
        is_admin=is_admin_user(current_user),
        start_date=start_date,
        end_date=end_date,
    )
    # 获取records
    records = influencer_crud.get_influencer_records(
        db,
        user_id=current_user.id,
        is_admin=is_admin_user(current_user),
        start_date=start_date,
        end_date=end_date,
        limit=200,
    )
    summary["records"] = [InfluencerRecordResponse.model_validate(r.to_dict()).model_dump() for r in records]
    return InfluencerSummaryResponse(**summary)


@router.get("/records/{record_id}", response_model=InfluencerRecordResponse)
def get_record(record_id: str,
               db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    record = influencer_crud.get_influencer_record_by_id(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    if not is_admin_user(current_user) and record.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限查看")
    return InfluencerRecordResponse.model_validate(record.to_dict())


@router.post("/records", response_model=InfluencerRecordResponse)
def create_record(record_data: InfluencerRecordCreate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    record = influencer_crud.create_influencer_record(
        db,
        user_id=current_user.id,
        user_name=current_user.name,
        **record_data.model_dump(),
    )
    return InfluencerRecordResponse.model_validate(record.to_dict())


@router.put("/records/{record_id}", response_model=InfluencerRecordResponse)
def update_record(record_id: str, record_data: InfluencerRecordUpdate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    record = influencer_crud.get_influencer_record_by_id(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    if not is_admin_user(current_user) and record.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限修改")

    update_data = record_data.model_dump(exclude_unset=True)
    updated = influencer_crud.update_influencer_record(db, record_id, **update_data)
    return InfluencerRecordResponse.model_validate(updated.to_dict())


@router.delete("/records/{record_id}")
def delete_record(record_id: str,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    record = influencer_crud.get_influencer_record_by_id(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    if not is_admin_user(current_user) and record.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限删除")

    influencer_crud.delete_influencer_record(db, record_id)
    return {"message": "删除成功"}
