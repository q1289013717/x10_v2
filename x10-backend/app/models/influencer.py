import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, Text, JSON
from app.core.database import Base


class DarenResource(Base):
    """达人资源库"""
    __tablename__ = "daren_resources"

    id = Column(String, primary_key=True, default=lambda: f"daren_{uuid.uuid4().hex[:12]}")
    name = Column(String(200), default="")
    date = Column(String(10), default="")
    daren_id = Column(String(100), unique=True, nullable=False)  # 达人唯一ID
    daren_name = Column(String(200), default="")
    platform = Column(String(100), default="")
    contact = Column(String(100), default="")
    position = Column(String(100), default="")
    position_other = Column(String(200), default="")
    followers = Column(String(50), default="")
    categories = Column(JSON, default=list)
    fan_portrait = Column(Text, default="")
    gmv = Column(String(50), default="")
    channel = Column(String(100), default="")
    first_contact_date = Column(String(10), default="")
    latest_follow_date = Column(String(10), default="")
    next_follow_date = Column(String(10), default="")
    tags = Column(JSON, default=list)
    special_requirement = Column(String(200), default="")
    special_requirement_note = Column(Text, default="")
    remarks = Column(Text, default="")
    created_by = Column(String(100), default="")
    updated_by = Column(String(100), default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "daren_id": self.daren_id,
            "daren_name": self.daren_name,
            "platform": self.platform,
            "contact": self.contact,
            "position": self.position,
            "position_other": self.position_other,
            "followers": self.followers,
            "categories": self.categories,
            "fan_portrait": self.fan_portrait,
            "gmv": self.gmv,
            "channel": self.channel,
            "first_contact_date": self.first_contact_date,
            "latest_follow_date": self.latest_follow_date,
            "next_follow_date": self.next_follow_date,
            "tags": self.tags,
            "special_requirement": self.special_requirement,
            "special_requirement_note": self.special_requirement_note,
            "remarks": self.remarks,
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class InfluencerRecord(Base):
    """达人合作台账"""
    __tablename__ = "influencer_records"

    id = Column(String, primary_key=True, default=lambda: f"inf_{uuid.uuid4().hex[:12]}")
    user_id = Column(String(100), nullable=False, index=True)
    user_name = Column(String(100), default="")
    date = Column(String(10), default="", index=True)
    influencer_id = Column(String(100), default="")
    influencer_name = Column(String(200), default="")
    contact = Column(String(100), default="")
    platform = Column(String(100), default="")
    platform_uid = Column(String(100), default="")
    commission_rate = Column(Float, default=0.0)
    traffic_method = Column(String(100), default="")
    cooperation_start = Column(String(10), default="")
    cooperation_end = Column(String(10), default="")
    compliance_status = Column(String(50), default="")
    gmv = Column(Float, default=0.0)
    roi = Column(Float, default=0.0)
    conversion_rate = Column(Float, default=0.0)
    return_rate = Column(Float, default=0.0)
    payment_status = Column(String(50), default="")
    re_broadcast_willingness = Column(String(50), default="")
    re_broadcast_date = Column(String(10), default="")
    remarks = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "date": self.date,
            "influencer_id": self.influencer_id,
            "influencer_name": self.influencer_name,
            "contact": self.contact,
            "platform": self.platform,
            "platform_uid": self.platform_uid,
            "commission_rate": self.commission_rate,
            "traffic_method": self.traffic_method,
            "cooperation_start": self.cooperation_start,
            "cooperation_end": self.cooperation_end,
            "compliance_status": self.compliance_status,
            "gmv": self.gmv,
            "roi": self.roi,
            "conversion_rate": self.conversion_rate,
            "return_rate": self.return_rate,
            "payment_status": self.payment_status,
            "re_broadcast_willingness": self.re_broadcast_willingness,
            "re_broadcast_date": self.re_broadcast_date,
            "remarks": self.remarks,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
