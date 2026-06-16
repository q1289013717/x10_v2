import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text
from app.core.database import Base


class WorkReport(Base):
    """工作报告/复盘"""
    __tablename__ = "work_reports"

    id = Column(String, primary_key=True, default=lambda: f"report_{uuid.uuid4().hex[:12]}")
    title = Column(String(500), nullable=False)
    type = Column(String(20), nullable=False, index=True)  # daily, weekly, monthly
    date = Column(String(10), nullable=False, index=True)  # YYYY-MM-DD
    period = Column(String(100), default="")  # 报告周期标签

    # 正文内容
    summary = Column(Text, default="")
    achievements = Column(Text, default="")
    problems = Column(Text, default="")
    plans = Column(Text, default="")

    # 工作项 (JSON 数组)
    work_items = Column(Text, default="[]")

    # 数据指标
    target_amount = Column(String, default="0")
    completed_amount = Column(String, default="0")
    customer_count = Column(String, default="0")
    new_customer_count = Column(String, default="0")

    # 元信息
    author = Column(String(100), default="")
    author_id = Column(String(100), default="", index=True)
    department = Column(String(200), default="")
    company = Column(String(200), default="")
    company_id = Column(String(100), default="")

    # 报告状态 (submitted, draft)
    status = Column(String(20), default="submitted", index=True)
    # 批复状态 (pending, approved, rejected)
    approval_status = Column(String(20), default="pending", index=True)
    approver = Column(String(100), default="")
    approved_at = Column(String(30), default="")
    # 批复意见 (JSON 数组)
    approval_comments = Column(Text, default="[]")

    # 附件 (JSON 数组)
    attachments = Column(Text, default="[]")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "type": self.type,
            "date": self.date,
            "period": self.period,
            "summary": self.summary,
            "achievements": self.achievements,
            "problems": self.problems,
            "plans": self.plans,
            "work_items": self.work_items,
            "target_amount": self.target_amount,
            "completed_amount": self.completed_amount,
            "customer_count": self.customer_count,
            "new_customer_count": self.new_customer_count,
            "author": self.author,
            "author_id": self.author_id,
            "department": self.department,
            "company": self.company,
            "company_id": self.company_id,
            "status": self.status,
            "approval_status": self.approval_status,
            "approver": self.approver,
            "approved_at": self.approved_at,
            "approval_comments": self.approval_comments,
            "attachments": self.attachments,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
