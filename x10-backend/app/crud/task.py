from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
import calendar

from app.models.task import CalendarTask, DailyTarget, MonthlyTarget


# ========== 日历任务（按用户隔离） ==========

def get_tasks_by_date(db: Session, date_key: str, user_id: Optional[str] = None,
                      is_admin: bool = False) -> List[CalendarTask]:
    q = db.query(CalendarTask).filter(CalendarTask.date_key == date_key)
    if not is_admin and user_id:
        q = q.filter(CalendarTask.created_by == user_id)
    return q.order_by(CalendarTask.created_at.asc()).all()


def get_task_by_id(db: Session, task_id: str) -> Optional[CalendarTask]:
    return db.query(CalendarTask).filter(CalendarTask.id == task_id).first()


def create_task(db: Session, date_key: str, action: str, responsible: str = "",
                risk: str = "无", status: str = "pending", amount: float = 0.0,
                created_by: str = "") -> CalendarTask:
    target = get_or_create_target(db, date_key, created_by)
    task = CalendarTask(
        date_key=date_key,
        action=action,
        responsible=responsible,
        risk=risk,
        status=status,
        amount=amount,
        target_amount=target.target_amount,
        created_by=created_by,
    )
    db.add(task)

    # 更新目标完成额
    if status == "completed":
        target.completed_amount = (target.completed_amount or 0) + amount

    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task_id: str, **kwargs) -> Optional[CalendarTask]:
    task = get_task_by_id(db, task_id)
    if not task:
        return None

    old_status = task.status
    old_amount = task.amount
    new_date_key = kwargs.get("date_key")

    for key, value in kwargs.items():
        if hasattr(task, key) and value is not None:
            setattr(task, key, value)

    # 更新目标完成额
    target = db.query(DailyTarget).filter(
        DailyTarget.date_key == task.date_key,
        DailyTarget.user_id == task.created_by or (DailyTarget.user_id == "" if not task.created_by else True)
    ).first()
    # 精确匹配用户
    target = db.query(DailyTarget).filter(
        DailyTarget.date_key == task.date_key,
        DailyTarget.user_id == (task.created_by or "")
    ).first()

    if target:
        if old_status == "completed" and task.status != "completed":
            target.completed_amount = max(0, (target.completed_amount or 0) - old_amount)
        elif old_status != "completed" and task.status == "completed":
            target.completed_amount = (target.completed_amount or 0) + task.amount

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: str) -> bool:
    task = get_task_by_id(db, task_id)
    if not task:
        return False

    # 更新目标完成额
    target = db.query(DailyTarget).filter(
        DailyTarget.date_key == task.date_key,
        DailyTarget.user_id == (task.created_by or "")
    ).first()
    if target and task.status == "completed":
        target.completed_amount = max(0, (target.completed_amount or 0) - (task.amount or 0))

    db.delete(task)
    db.commit()
    return True


def move_task(db: Session, task_id: str, new_date_key: str) -> Optional[CalendarTask]:
    """将任务移动到另一个日期"""
    task = get_task_by_id(db, task_id)
    if not task:
        return None

    old_date = task.date_key
    old_status = task.status

    # 更新旧日期的完成额
    old_target = db.query(DailyTarget).filter(
        DailyTarget.date_key == old_date,
        DailyTarget.user_id == (task.created_by or "")
    ).first()
    if old_target and old_status == "completed":
        old_target.completed_amount = max(0, (old_target.completed_amount or 0) - (task.amount or 0))

    task.date_key = new_date_key
    get_or_create_target(db, new_date_key, task.created_by)

    db.commit()
    db.refresh(task)
    return task


# ========== 每日目标（按用户隔离） ==========

def get_or_create_target(db: Session, date_key: str, user_id: str = "", created_by: str = "") -> DailyTarget:
    """获取或创建某用户的每日目标"""
    target = db.query(DailyTarget).filter(
        DailyTarget.date_key == date_key,
        DailyTarget.user_id == user_id
    ).first()
    if not target:
        target = DailyTarget(date_key=date_key, user_id=user_id, created_by=created_by or user_id)
        db.add(target)
        db.flush()
    return target


def get_target_by_date(db: Session, date_key: str, user_id: str = "") -> Optional[DailyTarget]:
    """获取指定日期指定用户的目标"""
    return db.query(DailyTarget).filter(
        DailyTarget.date_key == date_key,
        DailyTarget.user_id == user_id
    ).first()


def set_daily_target(db: Session, date_key: str, amount: float, user_id: str = "",
                     created_by: str = "", is_auto_spread: int = 0) -> DailyTarget:
    """设置某用户的每日目标"""
    target = db.query(DailyTarget).filter(
        DailyTarget.date_key == date_key,
        DailyTarget.user_id == user_id
    ).first()
    if target:
        target.target_amount = amount
        target.is_auto_spread = is_auto_spread
        if created_by:
            target.created_by = created_by
    else:
        target = DailyTarget(
            date_key=date_key, user_id=user_id,
            target_amount=amount, created_by=created_by or user_id,
            is_auto_spread=is_auto_spread,
        )
        db.add(target)
    db.commit()
    db.refresh(target)
    return target


# ========== 月度目标 & 自动平摊 ==========

def _get_work_days(year: int, month: int) -> List[str]:
    """获取月份内所有工作日（周一到周五），返回 YYYY-MM-DD 列表"""
    _, days_in_month = calendar.monthrange(year, month)
    work_days = []
    for day in range(1, days_in_month + 1):
        d = datetime(year, month, day)
        if d.weekday() < 5:  # 周一到周五 (0-4)
            work_days.append(f"{year}-{month:02d}-{day:02d}")
    return work_days


def set_monthly_target(db: Session, user_id: str, year: int, month: int,
                       target_amount: float) -> MonthlyTarget:
    """
    设置月度目标，自动平摊到每个工作日。

    核心逻辑：员工设置月度总目标 → 计算当月工作日天数 → 平均分摊到每一天
    例如：3万目标 / 22个工作日 ≈ 1364元/天
    """
    # 获取或创建月度目标记录
    mt = db.query(MonthlyTarget).filter(
        MonthlyTarget.user_id == user_id,
        MonthlyTarget.year == year,
        MonthlyTarget.month == month,
    ).first()

    work_days_list = _get_work_days(year, month)
    work_day_count = len(work_days_list)
    daily_avg = round(target_amount / work_day_count, 2) if work_day_count > 0 else 0

    if mt:
        mt.target_amount = target_amount
        mt.daily_target_avg = daily_avg
        mt.work_days = work_day_count
    else:
        mt = MonthlyTarget(
            user_id=user_id,
            year=year,
            month=month,
            target_amount=target_amount,
            daily_target_avg=daily_avg,
            work_days=work_day_count,
        )
        db.add(mt)
    db.flush()

    # 清除该用户该月的旧自动平摊记录
    db.query(DailyTarget).filter(
        DailyTarget.user_id == user_id,
        DailyTarget.is_auto_spread == 1,
        DailyTarget.date_key.like(f"{year}-{month:02d}-%"),
    ).delete()

    # 为每个工作日创建/更新每日目标
    for dk in work_days_list:
        existing = db.query(DailyTarget).filter(
            DailyTarget.date_key == dk,
            DailyTarget.user_id == user_id,
        ).first()
        if existing:
            # 如果已有手动设置的目标且不是自动平摊的，保留原值；否则覆盖
            if existing.is_auto_spread == 1 or existing.target_amount == 0:
                existing.target_amount = daily_avg
                existing.is_auto_spread = 1
        else:
            db.add(DailyTarget(
                date_key=dk, user_id=user_id,
                target_amount=daily_avg,
                is_auto_spread=1,
                created_by=user_id,
            ))

    db.commit()
    db.refresh(mt)
    return mt


def get_monthly_target(db: Session, user_id: str, year: int, month: int) -> Optional[MonthlyTarget]:
    """获取用户的月度目标"""
    return db.query(MonthlyTarget).filter(
        MonthlyTarget.user_id == user_id,
        MonthlyTarget.year == year,
        MonthlyTarget.month == month,
    ).first()


def get_monthly_calendar_data(db: Session, user_id: str, year: int, month: int,
                              is_admin: bool = False, admin_user_id: str = "") -> dict:
    """
    获取月度日历数据（供前端日历渲染使用）

    返回格式：
    {
      "2026-06-01": { targetAmount: 1364, completedAmount: 800, tasks: [...] },
      "2026-06-02": { targetAmount: 1364, completedAmount: 1500, tasks: [...] },
      ...
    }
    """
    query_user_id = user_id if not is_admin else admin_user_id
    if not query_user_id:
        query_user_id = user_id

    result = {}
    _, days_in_month = calendar.monthrange(year, month)

    # 批量获取该用户该月所有每日目标
    targets = db.query(DailyTarget).filter(
        DailyTarget.user_id == query_user_id,
        DailyTarget.date_key.like(f"{year}-{month:02d}-%"),
    ).all()
    target_map = {t.date_key: t for t in targets}

    # 批量获取该用户该月所有任务
    q = db.query(CalendarTask).filter(
        CalendarTask.date_key.like(f"{year}-{month:02d}-%"),
    )
    if not is_admin:
        q = q.filter(CalendarTask.created_by == query_user_id)
    all_tasks = q.all()

    # 按 date_key 分组任务
    from collections import defaultdict
    task_map = defaultdict(list)
    for t in all_tasks:
        task_map[t.date_key].append(t.to_dict())

    # 组装结果
    for day in range(1, days_in_month + 1):
        dk = f"{year}-{month:02d}-{day:02d}"
        tgt = target_map.get(dk)
        result[dk] = {
            "targetAmount": tgt.target_amount if tgt else 0,
            "completedAmount": tgt.completed_amount if tgt else 0,
            "isAutoSpread": tgt.is_auto_spread if tgt else 0,
            "tasks": task_map.get(dk, []),
        }

    return result


def get_admin_monthly_summary(db: Session, year: int, month: int) -> dict:
    """
    管理员视角：获取所有人的月度汇总

    返回每个人的：
    - 月度目标、日均目标、已完成总额、完成率、有数据的日期数
    以及全公司汇总
    """
    from app.models.user import User

    _, days_in_month = calendar.monthrange(year, month)

    # 获取所有有任务的活跃用户
    active_users = db.query(User).filter(User.status == "active").all()

    users_summary = []
    grand_target = 0
    grand_completed = 0

    for u in active_users:
        uid = u.id
        # 月度目标
        mt = get_monthly_target(db, uid, year, month)
        monthly_tgt = mt.target_amount if mt else 0
        daily_avg = mt.daily_target_avg if mt else 0

        # 该月所有每日目标的完成金额合计
        day_targets = db.query(DailyTarget).filter(
            DailyTarget.user_id == uid,
            DailyTarget.date_key.like(f"{year}-{month:02d}-%"),
        ).all()
        total_completed = sum((dt.completed_amount or 0) for dt in day_targets)
        days_with_data = sum(1 for dt in day_targets if dt.target_amount > 0)

        completion_rate = round(total_completed / monthly_tgt * 100, 1) if monthly_tgt > 0 else 0

        grand_target += monthly_tgt
        grand_completed += total_completed

        users_summary.append({
            "user_id": uid,
            "user_name": u.name,
            "role": u.role,
            "company": u.company,
            "monthly_target": monthly_tgt,
            "daily_target_avg": daily_avg,
            "total_completed": total_completed,
            "completion_rate": completion_rate,
            "days_with_data": days_with_data,
            "total_days": days_in_month,
        })

    grand_rate = round(grand_completed / grand_target * 100, 1) if grand_target > 0 else 0

    return {
        "year": year,
        "month": month,
        "grand_total_target": grand_target,
        "grand_total_completed": grand_completed,
        "grand_completion_rate": grand_rate,
        "users": users_summary,
    }


# ========== 统计 ==========

def get_calendar_stats(db: Session, user_id: Optional[str] = None, is_admin: bool = False) -> dict:
    """获取仪表盘统计数据"""
    today = datetime.now().strftime("%Y-%m-%d")
    query_uid = user_id or ""

    # 今日目标
    today_target = db.query(DailyTarget).filter(
        DailyTarget.date_key == today,
        DailyTarget.user_id == query_uid,
    ).first()
    today_target_amount = today_target.target_amount if today_target else 50000
    today_completed = today_target.completed_amount if today_target else 0

    # 本周数据
    week_completed = 0
    for i in range(7):
        d = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        t = db.query(DailyTarget).filter(
            DailyTarget.date_key == d,
            DailyTarget.user_id == query_uid,
        ).first()
        if t:
            week_completed += t.completed_amount or 0

    # 今日任务统计
    q = db.query(CalendarTask).filter(CalendarTask.date_key == today)
    if not is_admin and user_id:
        q = q.filter(CalendarTask.created_by == user_id)
    today_tasks = q.all()

    pending = len([t for t in today_tasks if t.status == "pending"])
    completed = len([t for t in today_tasks if t.status == "completed"])
    risk = len([t for t in today_tasks if t.risk and t.risk != "无"])

    return {
        "today_target": today_target_amount,
        "today_completed": today_completed,
        "week_target": 350000,
        "week_completed": week_completed,
        "pending_tasks": pending,
        "completed_tasks": completed,
        "risk_tasks": risk,
        "total_tasks": len(today_tasks),
    }


def get_recent_tasks(db: Session, days: int = 7, user_id: Optional[str] = None,
                     is_admin: bool = False) -> List[dict]:
    """获取最近N天的任务摘要"""
    query_uid = user_id or ""
    result = []
    for i in range(days):
        d = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        target = db.query(DailyTarget).filter(
            DailyTarget.date_key == d,
            DailyTarget.user_id == query_uid,
        ).first()
        q = db.query(CalendarTask).filter(CalendarTask.date_key == d)
        if not is_admin and user_id:
            q = q.filter(CalendarTask.created_by == user_id)
        tasks = q.all()
        if tasks or target:
            result.append({
                "date": d,
                "target_amount": target.target_amount if target else 0,
                "completed_amount": target.completed_amount if target else 0,
                "is_auto_spread": target.is_auto_spread if target else 0,
                "tasks": [t.to_dict() for t in tasks],
                "task_count": len(tasks),
            })
    return result
