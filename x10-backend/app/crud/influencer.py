from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.influencer import DarenResource, InfluencerRecord


# ========== 达人资源 ==========

def get_daren_resources(db: Session, user_id: Optional[str] = None,
                        is_admin: bool = False, keyword: Optional[str] = None,
                        platform: Optional[str] = None,
                        skip: int = 0, limit: int = 50) -> List[DarenResource]:
    q = db.query(DarenResource)
    if not is_admin and user_id:
        q = q.filter(DarenResource.created_by == user_id)
    if keyword:
        q = q.filter(
            (DarenResource.daren_name.contains(keyword)) |
            (DarenResource.daren_id.contains(keyword)) |
            (DarenResource.name.contains(keyword))
        )
    if platform:
        q = q.filter(DarenResource.platform == platform)
    return q.order_by(DarenResource.created_at.desc()).offset(skip).limit(limit).all()


def get_daren_resource_by_id(db: Session, resource_id: str) -> Optional[DarenResource]:
    return db.query(DarenResource).filter(DarenResource.id == resource_id).first()


def get_daren_by_daren_id(db: Session, daren_id: str) -> Optional[DarenResource]:
    return db.query(DarenResource).filter(DarenResource.daren_id == daren_id).first()


def create_daren_resource(db: Session, **kwargs) -> DarenResource:
    resource = DarenResource(**kwargs)
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource


def update_daren_resource(db: Session, resource_id: str, **kwargs) -> Optional[DarenResource]:
    resource = get_daren_resource_by_id(db, resource_id)
    if not resource:
        return None
    for key, value in kwargs.items():
        if hasattr(resource, key) and value is not None:
            setattr(resource, key, value)
    db.commit()
    db.refresh(resource)
    return resource


def delete_daren_resource(db: Session, resource_id: str) -> bool:
    resource = get_daren_resource_by_id(db, resource_id)
    if not resource:
        return False
    db.delete(resource)
    db.commit()
    return True


def count_daren_resources(db: Session, user_id: Optional[str] = None,
                          is_admin: bool = False, keyword: Optional[str] = None,
                          platform: Optional[str] = None) -> int:
    q = db.query(DarenResource)
    if not is_admin and user_id:
        q = q.filter(DarenResource.created_by == user_id)
    if keyword:
        q = q.filter(
            (DarenResource.daren_name.contains(keyword)) |
            (DarenResource.daren_id.contains(keyword))
        )
    if platform:
        q = q.filter(DarenResource.platform == platform)
    return q.count()


# ========== 达人合作台账 ==========

def get_influencer_records(db: Session, user_id: Optional[str] = None,
                           is_admin: bool = False, start_date: Optional[str] = None,
                           end_date: Optional[str] = None,
                           skip: int = 0, limit: int = 50) -> List[InfluencerRecord]:
    q = db.query(InfluencerRecord)
    if not is_admin and user_id:
        q = q.filter(InfluencerRecord.user_id == user_id)
    if start_date:
        q = q.filter(InfluencerRecord.date >= start_date)
    if end_date:
        q = q.filter(InfluencerRecord.date <= end_date)
    return q.order_by(InfluencerRecord.created_at.desc()).offset(skip).limit(limit).all()


def get_influencer_record_by_id(db: Session, record_id: str) -> Optional[InfluencerRecord]:
    return db.query(InfluencerRecord).filter(InfluencerRecord.id == record_id).first()


def create_influencer_record(db: Session, user_id: str, user_name: str, **kwargs) -> InfluencerRecord:
    record = InfluencerRecord(user_id=user_id, user_name=user_name, **kwargs)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def update_influencer_record(db: Session, record_id: str, **kwargs) -> Optional[InfluencerRecord]:
    record = get_influencer_record_by_id(db, record_id)
    if not record:
        return None
    for key, value in kwargs.items():
        if hasattr(record, key) and value is not None:
            setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record


def delete_influencer_record(db: Session, record_id: str) -> bool:
    record = get_influencer_record_by_id(db, record_id)
    if not record:
        return False
    db.delete(record)
    db.commit()
    return True


def get_influencer_summary(db: Session, user_id: Optional[str] = None,
                           is_admin: bool = False,
                           start_date: Optional[str] = None,
                           end_date: Optional[str] = None) -> dict:
    q = db.query(InfluencerRecord)
    if not is_admin and user_id:
        q = q.filter(InfluencerRecord.user_id == user_id)
    if start_date:
        q = q.filter(InfluencerRecord.date >= start_date)
    if end_date:
        q = q.filter(InfluencerRecord.date <= end_date)
    records = q.all()

    total_gmv = sum(float(r.gmv or 0) for r in records)
    unique_influencers = len(set(r.influencer_id for r in records if r.influencer_id))

    platform_dist = {}
    payment_dist = {}
    compliance_dist = {}
    re_broadcast_dist = {}

    for r in records:
        if r.platform:
            platform_dist[r.platform] = platform_dist.get(r.platform, 0) + 1
        if r.payment_status:
            payment_dist[r.payment_status] = payment_dist.get(r.payment_status, 0) + 1
        if r.compliance_status:
            compliance_dist[r.compliance_status] = compliance_dist.get(r.compliance_status, 0) + 1
        w = r.re_broadcast_willingness or "未设置"
        re_broadcast_dist[w] = re_broadcast_dist.get(w, 0) + 1

    return {
        "total_records": len(records),
        "unique_influencers": unique_influencers,
        "total_gmv": total_gmv,
        "avg_roi": sum(float(r.roi or 0) for r in records) / len(records) if records else 0,
        "avg_conversion_rate": sum(float(r.conversion_rate or 0) for r in records) / len(records) if records else 0,
        "avg_return_rate": sum(float(r.return_rate or 0) for r in records) / len(records) if records else 0,
        "platform_distribution": platform_dist,
        "payment_status_distribution": payment_dist,
        "compliance_status_distribution": compliance_dist,
        "re_broadcast_willingness_distribution": re_broadcast_dist,
    }
