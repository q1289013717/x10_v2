from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.deps import get_current_user, get_current_admin_user, is_admin_user
from app.models.user import User
from app.schemas.report import ReportCreate, ReportUpdate, ReportResponse, ReportApproval
from app.crud import report as report_crud

router = APIRouter(prefix="/api/reports", tags=["工作报告"])


@router.get("", response_model=list[ReportResponse])
def list_reports(
    type: Optional[str] = Query(default=None, description="daily/weekly/monthly"),
    status: Optional[str] = Query(default=None, description="submitted/draft"),
    approval_status: Optional[str] = Query(default=None, description="pending/approved/rejected"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=200, ge=1, le=500),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(report_crud.WorkReport)
    if not is_admin_user(current_user):
        q = q.filter(report_crud.WorkReport.author_id == current_user.id)
    if type and type != "all":
        q = q.filter(report_crud.WorkReport.type == type)
    if status and status != "all":
        q = q.filter(report_crud.WorkReport.status == status)
    if approval_status and approval_status != "all":
        q = q.filter(report_crud.WorkReport.approval_status == approval_status)
    reports = q.order_by(report_crud.WorkReport.created_at.desc()).offset(skip).limit(limit).all()
    return [ReportResponse.model_validate(r.to_dict()) for r in reports]


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(report_id: str,
               current_user: User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    report = report_crud.get_report_by_id(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="报告不存在")
    if not is_admin_user(current_user) and report.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限查看")
    return ReportResponse.model_validate(report.to_dict())


@router.post("", response_model=ReportResponse)
def create_report(report_data: ReportCreate,
                  current_user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    report = report_crud.create_report(
        db,
        title=report_data.title,
        type=report_data.type,
        date=report_data.date,
        period=report_data.period,
        summary=report_data.summary,
        achievements=report_data.achievements,
        problems=report_data.problems,
        plans=report_data.plans,
        work_items=report_data.work_items,
        target_amount=report_data.target_amount,
        completed_amount=report_data.completed_amount,
        customer_count=report_data.customer_count,
        new_customer_count=report_data.new_customer_count,
        author=current_user.name or current_user.account,
        author_id=str(current_user.id),
        department=report_data.department or "",
        company=report_data.company or current_user.company,
        company_id=report_data.company_id,
        status=report_data.status,
        approval_status=report_data.approval_status,
        attachments=report_data.attachments,
    )
    return ReportResponse.model_validate(report.to_dict())


@router.put("/{report_id}", response_model=ReportResponse)
def update_report(report_id: str, report_data: ReportUpdate,
                  current_user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    report = report_crud.get_report_by_id(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="报告不存在")
    if not is_admin_user(current_user) and report.author_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="无权限修改")

    update_data = report_data.model_dump(exclude_unset=True)
    updated = report_crud.update_report(db, report_id, **update_data)
    return ReportResponse.model_validate(updated.to_dict())


@router.put("/{report_id}/approve", response_model=ReportResponse)
def approve_report(report_id: str, approval: ReportApproval,
                   current_user: User = Depends(get_current_admin_user),
                   db: Session = Depends(get_db)):
    updated = report_crud.approve_report(
        db, report_id, approval.status, approval.comment,
        current_user.name or current_user.account,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="报告不存在")
    return ReportResponse.model_validate(updated.to_dict())


@router.delete("/{report_id}")
def delete_report(report_id: str,
                  current_user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    report = report_crud.get_report_by_id(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="报告不存在")
    if not is_admin_user(current_user) and report.author_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="无权限删除")

    report_crud.delete_report(db, report_id)
    return {"message": "删除成功"}
