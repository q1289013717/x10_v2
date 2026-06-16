from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.deps import get_current_user, is_admin_user
from app.models.user import User
from app.schemas.influencer import (
    DarenResourceCreate, DarenResourceUpdate, DarenResourceResponse,
    InfluencerRecordCreate, InfluencerRecordUpdate, InfluencerRecordResponse,
    InfluencerSummaryResponse,
)
from app.crud import influencer as influencer_crud

router = APIRouter(prefix="/api/daren", tags=["达人管理"])


# ========== 达人资源库 ==========

@router.get("/resources", response_model=list[DarenResourceResponse])
def list_daren_resources(
    keyword: Optional[str] = Query(default=None),
    platform: Optional[str] = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resources = influencer_crud.get_daren_resources(
        db,
        user_id=current_user.id,
        is_admin=is_admin_user(current_user),
        keyword=keyword,
        platform=platform,
        skip=skip,
        limit=limit,
    )
    return [DarenResourceResponse.model_validate(r.to_dict()) for r in resources]


@router.get("/resources/count")
def count_daren_resources(
    keyword: Optional[str] = Query(default=None),
    platform: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    count = influencer_crud.count_daren_resources(
        db,
        user_id=current_user.id,
        is_admin=is_admin_user(current_user),
        keyword=keyword,
        platform=platform,
    )
    return {"total": count}


@router.get("/resources/{resource_id}", response_model=DarenResourceResponse)
def get_daren_resource(resource_id: str,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    resource = influencer_crud.get_daren_resource_by_id(db, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="达人不存在")
    # 管理员看全部，普通用户看自己的
    if not is_admin_user(current_user) and resource.created_by != current_user.id:
        # 对非管理员脱敏联系方式
        d = resource.to_dict()
        if len(d.get("contact", "")) >= 11:
            d["contact"] = d["contact"][:3] + "****" + d["contact"][7:]
        return DarenResourceResponse(**d)
    return DarenResourceResponse.model_validate(resource.to_dict())


@router.post("/resources", response_model=DarenResourceResponse)
def create_daren_resource(resource_data: DarenResourceCreate,
                          db: Session = Depends(get_db),
                          current_user: User = Depends(get_current_user)):
    # 检查达人ID唯一性
    existing = influencer_crud.get_daren_by_daren_id(db, resource_data.daren_id)
    if existing:
        raise HTTPException(status_code=400, detail="该达人ID已存在")

    create_data = resource_data.model_dump()
    create_data["created_by"] = current_user.id
    create_data["updated_by"] = current_user.id
    resource = influencer_crud.create_daren_resource(db, **create_data)
    return DarenResourceResponse.model_validate(resource.to_dict())


@router.put("/resources/{resource_id}", response_model=DarenResourceResponse)
def update_daren_resource(resource_id: str, resource_data: DarenResourceUpdate,
                          db: Session = Depends(get_db),
                          current_user: User = Depends(get_current_user)):
    resource = influencer_crud.get_daren_resource_by_id(db, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="达人不存在")
    if not is_admin_user(current_user) and resource.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="无权限修改")

    update_data = resource_data.model_dump(exclude_unset=True)
    update_data["updated_by"] = current_user.id
    updated = influencer_crud.update_daren_resource(db, resource_id, **update_data)
    return DarenResourceResponse.model_validate(updated.to_dict())


@router.delete("/resources/{resource_id}")
def delete_daren_resource(resource_id: str,
                          db: Session = Depends(get_db),
                          current_user: User = Depends(get_current_user)):
    resource = influencer_crud.get_daren_resource_by_id(db, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="达人不存在")
    if not is_admin_user(current_user) and resource.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="无权限删除")

    influencer_crud.delete_daren_resource(db, resource_id)
    return {"message": "删除成功"}
