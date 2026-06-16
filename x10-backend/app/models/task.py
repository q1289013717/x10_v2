import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, UniqueConstraint
from app.core.database import Base


class CalendarTask(Base):
    """日历任务 - 每日任务条目"""
    __tablename__ = "calendar_tasks"

    id = Column(String, primary_key=True, default=lambda: f"task_{uuid.uuid4().hex[:12]}")
    date_key = Column(String(10), nullable=False, index=True)  # YYYY-MM-DD
    action = Column(String(500), nullable=False)  # 任务名称/行动
    responsible = Column(String(100), default="")  # 负责人
    risk = Column(String(200), default="无")  # 风险备注
    status = Column(String(20), default="pending")  # pending, completed, in_progress
    amount = Column(Float, default=0.0)  # 任务金额
    target_amount = Column(Float, default=0.0)  # 当日目标金额
    completed_amount = Column(Float, default=0.0)  # 当日已完成金额
    created_by = Column(String(100), default="")  # 创建者ID
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "date_key": self.date_key,
            "action": self.action,
            "responsible": self.responsible,
            "risk": self.risk,
            "status": self.status,
            "amount": self.amount,
            "target_amount": self.target_amount,
            "completed_amount": self.completed_amount,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class DailyTarget(Base):
    """每日目标 - 按用户隔离，每个员工有自己的每日目标"""
    __tablename__ = "daily_targets"
    __table_args__ = (
        UniqueConstraint("date_key", "user_id", name="uq_daily_target_date_user"),
    )

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    date_key = Column(String(10), nullable=False, index=True)
    user_id = Column(String(100), nullable=False, index=True, default="")  # 所属用户ID
    target_amount = Column(Float, default=0.0)  # 当日目标（可由月度目标自动平摊）
    completed_amount = Column(Float, default=0.0)  # 当日已完成
    is_auto_spread = Column(Integer, default=0)  # 是否由月度目标自动平摊生成: 1=是 0=否
    created_by = Column(String(100), default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "date_key": self.date_key,
            "user_id": self.user_id,
            "target_amount": self.target_amount,
            "completed_amount": self.completed_amount,
            "is_auto_spread": self.is_auto_spread,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class MonthlyTarget(Base):
    """月度目标 - 员工设置月度总目标后自动平摊到每一天"""
    __tablename__ = "monthly_targets"
    __table_args__ = (
        UniqueConstraint("user_id", "year", "month", name="uq_monthly_target_user_ym"),
    )

    id = Column(String, primary_key=True, default=lambda: f"mt_{uuid.uuid4().hex[:12]}")
    user_id = Column(String(100), nullable=False, index=True)  # 目标所属用户
    year = Column(Integer, nullable=False)  # 年份
    month = Column(Integer, nullable=False)  # 月份 1-12
    target_amount = Column(Float, default=0.0)  # 月度总目标金额
    daily_target_avg = Column(Float, default=0.0)  # 平均每日目标（用于显示）
    work_days = Column(Integer, default=0)  # 工作日天数
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "year": self.year,
            "month": self.month,
            "target_amount": self.target_amount,
            "daily_target_avg": self.daily_target_avg,
            "work_days": self.work_days,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
