from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.report import WorkReport


def get_reports(db: Session, author_id: Optional[str] = None, report_type: Optional[str] = None,
                status: Optional[str] = None, is_admin: bool = False,
                skip: int = 0, limit: int = 50) -> List[WorkReport]:
    q = db.query(WorkReport)
    if not is_admin and author_id:
        q = q.filter(WorkReport.author_id == author_id)
    if report_type and report_type != "all":
        q = q.filter(WorkReport.type == report_type)
    if status and status != "all":
        q = q.filter(WorkReport.status == status)
    return q.order_by(WorkReport.created_at.desc()).offset(skip).limit(limit).all()


def get_report_by_id(db: Session, report_id: str) -> Optional[WorkReport]:
    return db.query(WorkReport).filter(WorkReport.id == report_id).first()


def create_report(db: Session, **kwargs) -> WorkReport:
    defaults = {
        "title": "",
        "type": "daily",
        "date": "",
        "author": "",
        "author_id": "",
    }
    defaults.update(kwargs)
    report = WorkReport(**defaults)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def update_report(db: Session, report_id: str, **kwargs) -> Optional[WorkReport]:
    report = get_report_by_id(db, report_id)
    if not report:
        return None
    for key, value in kwargs.items():
        if hasattr(report, key) and value is not None:
            setattr(report, key, value)
    db.commit()
    db.refresh(report)
    return report


def approve_report(db: Session, report_id: str, status: str,
                   comment: str = "", approved_by: str = "") -> Optional[WorkReport]:
    from datetime import datetime
    import json
    report = get_report_by_id(db, report_id)
    if not report:
        return None
    report.approval_status = status
    report.approver = approved_by
    report.approved_at = datetime.utcnow().isoformat()

    # 追加批复意见到 approval_comments JSON 数组
    try:
        comments = json.loads(report.approval_comments) if report.approval_comments else []
    except (json.JSONDecodeError, TypeError):
        comments = []
    comments.append({
        "id": str(int(datetime.utcnow().timestamp() * 1000)),
        "type": status,
        "content": comment or ("已通过" if status == "approved" else "已驳回"),
        "createdBy": approved_by,
        "createdAt": datetime.utcnow().isoformat(),
    })
    report.approval_comments = json.dumps(comments, ensure_ascii=False)

    db.commit()
    db.refresh(report)
    return report


def delete_report(db: Session, report_id: str) -> bool:
    report = get_report_by_id(db, report_id)
    if not report:
        return False
    db.delete(report)
    db.commit()
    return True
