"""
管理员告警与监控 API
- 报告未提交提醒（日报/周报）
- 任务配额异常报警（每日任务数不足60条）
"""
from datetime import date, timedelta, datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.deps import get_current_admin_user
from app.models.user import User
from app.models.report import WorkReport
from app.models.task import CalendarTask

router = APIRouter(prefix="/api/admin", tags=["管理监控"])


@router.get("/users")
def get_all_users(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """获取所有用户列表（管理员专用）"""
    all_users = db.query(User).filter(User.status == "active").all()
    return [
        {
            "id": u.id,
            "account": u.account,
            "name": u.name,
            "role": u.role,
            "company": u.company,
            "avatar": u.avatar,
        }
        for u in all_users
    ]


def get_week_range(today: date):
    """返回本周的起止日期（周一到周日）"""
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return monday.isoformat(), sunday.isoformat()


@router.get("/alerts")
def get_admin_alerts(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    获取管理端综合告警：
    - 昨日未提交日报的员工列表
    - 本周未提交周报的员工列表
    - 今日任务数不足60条的员工列表
    """
    today = date.today()
    yesterday = (today - timedelta(days=1)).isoformat()
    week_start, week_end = get_week_range(today)

    alerts = {
        "daily_missing": [],   # 昨日未交日报
        "weekly_missing": [],  # 本周未交周报
        "task_quota_alert": [],  # 今日任务<60条
    }

    # 获取所有活跃用户
    all_users = db.query(User).filter(User.status == "active").all()
    if not all_users:
        return alerts

    # --- 1. 检查昨日日报 ---
    daily_authors = set()
    daily_reports = db.query(WorkReport) \
        .filter(WorkReport.type == "daily", WorkReport.date == yesterday) \
        .all()
    for r in daily_reports:
        daily_authors.add(r.author_id)

    for u in all_users:
        if u.id not in daily_authors:
            alerts["daily_missing"].append({
                "user_id": u.id,
                "name": u.name or u.account,
                "account": u.account,
                "role": u.role,
                "company": u.company,
                "date": yesterday,
            })

    # --- 2. 检查本周周报 ---
    weekly_authors = set()
    weekly_reports = db.query(WorkReport) \
        .filter(
            WorkReport.type == "weekly",
            WorkReport.date >= week_start,
            WorkReport.date <= week_end,
        ) \
        .all()
    for r in weekly_reports:
        weekly_authors.add(r.author_id)

    for u in all_users:
        if u.id not in weekly_authors:
            alerts["weekly_missing"].append({
                "user_id": u.id,
                "name": u.name or u.account,
                "account": u.account,
                "role": u.role,
                "company": u.company,
                "week": f"{week_start} ~ {week_end}",
            })

    # --- 3. 检查今日任务配额（不足60条）---
    today_str = today.isoformat()

    task_counts = db.query(
        CalendarTask.created_by,
        func.count(CalendarTask.id).label("count")
    ).filter(
        CalendarTask.date_key == today_str
    ).group_by(CalendarTask.created_by).all()

    task_count_map = {tc[0]: tc[1] for tc in task_counts}

    min_quota = 60
    for u in all_users:
        count = task_count_map.get(u.id, 0)
        if count < min_quota:
            alerts["task_quota_alert"].append({
                "user_id": u.id,
                "name": u.name or u.account,
                "account": u.account,
                "role": u.role,
                "company": u.company,
                "task_count": count,
                "min_required": min_quota,
                "shortfall": min_quota - count,
                "date": today_str,
                "level": "critical" if count < 20 else "warning" if count < 40 else "normal",
            })

    # 按缺少数排序，缺得多的排前面
    alerts["task_quota_alert"].sort(key=lambda x: x["shortfall"], reverse=True)

    return alerts
