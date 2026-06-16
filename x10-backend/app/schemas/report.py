from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class ReportBase(BaseModel):
    title: str
    type: str = Field("daily", description="daily/weekly/monthly")
    date: str = Field(..., description="YYYY-MM-DD")
    period: str = ""
    company: str = ""
    company_id: str = ""
    summary: str = ""
    achievements: str = ""
    problems: str = ""
    plans: str = ""
    work_items: str = "[]"
    target_amount: str = "0"
    completed_amount: str = "0"
    customer_count: str = "0"
    new_customer_count: str = "0"
    department: str = ""
    status: str = "submitted"
    approval_status: str = "pending"
    approver: str = ""
    approved_at: str = ""
    approval_comments: str = "[]"
    attachments: str = "[]"


class ReportCreate(ReportBase):
    @field_validator("summary")
    @classmethod
    def summary_min_length(cls, v: str) -> str:
        if not v or len(v.strip()) < 50:
            raise ValueError(f"工作报告内容至少需要50字，当前{len(v.strip())}字，请补充内容后再提交")
        return v


class ReportUpdate(BaseModel):
    title: Optional[str] = None
    type: Optional[str] = None
    date: Optional[str] = None
    period: Optional[str] = None
    company: Optional[str] = None
    summary: Optional[str] = None
    achievements: Optional[str] = None
    problems: Optional[str] = None
    plans: Optional[str] = None
    work_items: Optional[str] = None
    target_amount: Optional[str] = None
    completed_amount: Optional[str] = None
    customer_count: Optional[str] = None
    new_customer_count: Optional[str] = None
    department: Optional[str] = None
    status: Optional[str] = None
    approval_status: Optional[str] = None
    approver: Optional[str] = None
    approved_at: Optional[str] = None
    approval_comments: Optional[str] = None
    attachments: Optional[str] = None


class ReportResponse(BaseModel):
    id: str
    title: str
    type: str
    date: str
    period: str = ""
    company: str = ""
    company_id: str = ""
    summary: str = ""
    achievements: str = ""
    problems: str = ""
    plans: str = ""
    work_items: str = "[]"
    target_amount: str = "0"
    completed_amount: str = "0"
    customer_count: str = "0"
    new_customer_count: str = "0"
    author: str = ""
    author_id: str = ""
    department: str = ""
    status: str = "submitted"
    approval_status: str = "pending"
    approver: str = ""
    approved_at: str = ""
    approval_comments: str = "[]"
    attachments: str = "[]"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class ReportApproval(BaseModel):
    status: str = Field(..., description="approved/rejected")
    comment: str = ""
