from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ========== 达人资源 ==========
class DarenResourceBase(BaseModel):
    name: str = ""
    date: str = ""
    daren_id: str = Field(..., description="达人唯一ID")
    daren_name: str = ""
    platform: str = ""
    contact: str = ""
    position: str = ""
    position_other: str = ""
    followers: str = ""
    categories: List[str] = []
    fan_portrait: str = ""
    gmv: str = ""
    channel: str = ""
    first_contact_date: str = ""
    latest_follow_date: str = ""
    next_follow_date: str = ""
    tags: List[str] = []
    special_requirement: str = ""
    special_requirement_note: str = ""
    remarks: str = ""


class DarenResourceCreate(DarenResourceBase):
    pass


class DarenResourceUpdate(BaseModel):
    name: Optional[str] = None
    date: Optional[str] = None
    daren_id: Optional[str] = None
    daren_name: Optional[str] = None
    platform: Optional[str] = None
    contact: Optional[str] = None
    position: Optional[str] = None
    position_other: Optional[str] = None
    followers: Optional[str] = None
    categories: Optional[List[str]] = None
    fan_portrait: Optional[str] = None
    gmv: Optional[str] = None
    channel: Optional[str] = None
    first_contact_date: Optional[str] = None
    latest_follow_date: Optional[str] = None
    next_follow_date: Optional[str] = None
    tags: Optional[List[str]] = None
    special_requirement: Optional[str] = None
    special_requirement_note: Optional[str] = None
    remarks: Optional[str] = None


class DarenResourceResponse(BaseModel):
    id: str
    name: str
    date: str
    daren_id: str
    daren_name: str
    platform: str
    contact: str
    position: str
    position_other: str
    followers: str
    categories: List[str]
    fan_portrait: str
    gmv: str
    channel: str
    first_contact_date: str
    latest_follow_date: str
    next_follow_date: str
    tags: List[str]
    special_requirement: str
    special_requirement_note: str
    remarks: str
    created_by: str
    updated_by: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


# ========== 达人合作台账 ==========
class InfluencerRecordBase(BaseModel):
    date: str = Field(..., description="YYYY-MM-DD")
    influencer_id: str = ""
    influencer_name: str = ""
    contact: str = ""
    platform: str = ""
    platform_uid: str = ""
    commission_rate: float = 0.0
    traffic_method: str = ""
    cooperation_start: str = ""
    cooperation_end: str = ""
    compliance_status: str = ""
    gmv: float = 0.0
    roi: float = 0.0
    conversion_rate: float = 0.0
    return_rate: float = 0.0
    payment_status: str = ""
    re_broadcast_willingness: str = ""
    re_broadcast_date: str = ""
    remarks: str = ""


class InfluencerRecordCreate(InfluencerRecordBase):
    pass


class InfluencerRecordUpdate(BaseModel):
    date: Optional[str] = None
    influencer_id: Optional[str] = None
    influencer_name: Optional[str] = None
    contact: Optional[str] = None
    platform: Optional[str] = None
    platform_uid: Optional[str] = None
    commission_rate: Optional[float] = None
    traffic_method: Optional[str] = None
    cooperation_start: Optional[str] = None
    cooperation_end: Optional[str] = None
    compliance_status: Optional[str] = None
    gmv: Optional[float] = None
    roi: Optional[float] = None
    conversion_rate: Optional[float] = None
    return_rate: Optional[float] = None
    payment_status: Optional[str] = None
    re_broadcast_willingness: Optional[str] = None
    re_broadcast_date: Optional[str] = None
    remarks: Optional[str] = None


class InfluencerRecordResponse(BaseModel):
    id: str
    user_id: str
    user_name: str
    date: str
    influencer_id: str
    influencer_name: str
    contact: str
    platform: str
    platform_uid: str
    commission_rate: float
    traffic_method: str
    cooperation_start: str
    cooperation_end: str
    compliance_status: str
    gmv: float
    roi: float
    conversion_rate: float
    return_rate: float
    payment_status: str
    re_broadcast_willingness: str
    re_broadcast_date: str
    remarks: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class InfluencerSummaryResponse(BaseModel):
    total_records: int
    unique_influencers: int
    total_gmv: float
    avg_roi: float
    avg_conversion_rate: float
    avg_return_rate: float
    platform_distribution: dict
    payment_status_distribution: dict
    compliance_status_distribution: dict
    re_broadcast_willingness_distribution: dict
    records: List[InfluencerRecordResponse]
