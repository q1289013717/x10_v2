"""
X10 V2 种子数据填充脚本
用法: python seed_data.py
会向 x10.db 插入模拟数据，已存在的数据不会覆盖
"""

import sys
import os
import uuid
import json
import hashlib
import io
from datetime import datetime, timedelta
from random import choice, randint, uniform, random

# 修复 Windows GBK 编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 加载项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, SessionLocal
from app.core.security import get_password_hash
from app.models.user import User
from app.models.report import WorkReport
from app.models.task import CalendarTask, DailyTarget
from app.models.training import TrainingDoc, QuizQuestion, QuizRecord, TrainingProblem
from app.models.influencer import DarenResource, InfluencerRecord
from app.models.meeting import Meeting, MeetingAnswer, SystemConfig

TODAY = datetime.now().strftime("%Y-%m-%d")
YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
DAY_BEFORE = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
WEEK_AGO = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
NOW_ISO = datetime.now().isoformat()


# ─── 员工数据 ───────────────────────────────────────────────
EMPLOYEES = [
    # (account, name, role, company, avatar)
    ("admin", "超级管理员", "集团管理员", "集团总部", "A"),
    ("xujianxu", "许建栩", "admin", "X10增长引擎", "许"),
    ("zhangwei", "张伟", "分公司管理员", "上海分公司", "张"),
    ("liuna", "刘娜", "员工", "上海分公司", "刘"),
    ("wangfang", "王芳", "员工", "上海分公司", "王"),
    ("chenming", "陈明", "员工", "北京分公司", "陈"),
    ("liuyang", "刘洋", "员工", "北京分公司", "刘"),
    ("zhaoli", "赵丽", "员工", "广州分公司", "赵"),
    ("sunqiang", "孙强", "员工", "广州分公司", "孙"),
    ("huangjie", "黄杰", "分公司管理员", "深圳分公司", "黄"),
    ("wumin", "吴敏", "员工", "深圳分公司", "吴"),
]

# 达人名称池
DAREN_NAMES = [
    "小杨说事", "美妆Lisa", "吃货大魔王", "健身教练Tony", "旅行达人小周",
    "穿搭日记", "科技宅小明", "宝妈小丽", "数码老张", "美食家小陈",
    "护肤达人Coco", "运动少年阿飞", "宠物博主小喵", "读书人阿文", "手工达人小美",
    "摄影大叔", "音乐小青年", "游戏主播阿豪", "搞笑一家人", "生活妙招王",
    "甜品师Lily", "家居改造王", "园艺达人老李", "手工皮具匠", "咖啡师小赵",
    "瑜伽教练Amy", "画画的小鱼", "汽车评测老K", "母婴好物推荐", "极客小新",
    "日料师傅小林", "街舞少年阿杰", "种植达人老王", "收纳专家小雪", "编程小哥阿涛",
    "调酒师Mike", "插画师小云", "钓鱼大叔老陈", "减肥日记", "手账少女",
    "脱口秀小王", "书法大师", "茶艺师小叶", "花艺师Rose", "跑步达人阿伟",
    "DIY达人", "育儿嫂小张", "装修老赵", "养花阿姨", "品酒师小李",
    "滑雪教练", "潜水达人", "攀岩小队", "骑行侠", "桌游达人",
    "摄影新手", "配音演员", "编舞师", "手工编织", "露营玩家",
    "宠物医生", "营养师小王", "心理咨询师", "理财顾问", "保险达人",
]

PLATFORMS = ["抖音", "快手", "小红书", "B站", "微博", "视频号"]
POSITIONS = ["头部达人", "腰部达人", "素人", "KOC", "中腰部达人"]
CATEGORIES_POOL = ["美妆", "食品", "家居", "数码", "母婴", "服饰", "运动", "旅游", "教育", "健康"]
CHANNELS = ["自主开发", "同行推荐", "平台推荐", "展会认识", "朋友介绍"]
TASK_ACTIONS = [
    "联系达人-小杨说事，确认合作意向",
    "跟进达人-美妆Lisa，发送产品样品",
    "准备赵宜主产品报价方案",
    "更新达人资源库-新增5条记录",
    "与客户电话沟通需求",
    "整理本周达人合作数据",
    "提交日报-完成今日工作总结",
    "制作达人合作PPT",
    "审核达人佣金结算单",
    "对接达人-吃货大魔王，确认直播时间",
    "整理达人BD话术模板",
    "分析竞品达人合作策略",
    "更新SOP流程文档",
    "培训新人-达人开发流程",
    "处理达人售后问题",
    "跟进达人-科技宅小明，协商佣金比例",
    "整理月度达人合作复盘",
    "策划下周达人直播排期",
    "与供应链确认发货计划",
    "录制产品介绍短视频素材",
    "筛选新达人-小红书平台",
    "联系达人-旅行达人小周",
    "准备双周汇报材料",
    "核对上月佣金发放明细",
    "优化达人筛选标准",
]

COMPANIES = ["上海分公司", "北京分公司", "广州分公司", "深圳分公司"]


def seed_users(db):
    """填充用户表"""
    existing = {r[0] for r in db.query(User.account).all()}
    added = 0
    for account, name, role, company, avatar in EMPLOYEES:
        if account in existing:
            continue
        user = User(
            id=str(uuid.uuid4()) if account not in ("admin", "xujianxu") else (
                "admin-001" if account == "admin" else str(uuid.uuid4())
            ),
            account=account,
            name=name,
            password=get_password_hash("123456"),  # 统一默认密码
            role=role,
            company=company,
            status="active",
            avatar=avatar,
        )
        db.add(user)
        added += 1
    db.commit()
    print(f"  ✅ users: 新增 {added} 条 (已有 {len(existing)} 条)")


def get_user_map(db):
    """获取用户 id→name 映射"""
    users = db.query(User).all()
    return {u.id: {"name": u.name, "role": u.role, "company": u.company, "account": u.account} for u in users}


def seed_work_reports(db, user_map):
    """填充工作报告"""
    existing_count = db.query(WorkReport).count()
    if existing_count >= 20:
        print(f"  ⏭ work_reports: 已有 {existing_count} 条，跳过")
        return

    added = 0
    user_ids = list(user_map.keys())

    # 过去7天的日报
    for day_offset in range(7):
        date = (datetime.now() - timedelta(days=day_offset)).strftime("%Y-%m-%d")
        for uid in user_ids:
            # 70%概率提交了日报（模拟有人没交的情况）
            if random() < 0.3 and day_offset > 0:
                continue
            info = user_map[uid]
            is_admin = info["role"] in ("集团管理员", "admin", "分公司管理员")

            work_items = []
            for _ in range(randint(2, 5)):
                work_items.append({
                    "task": choice(TASK_ACTIONS),
                    "result": choice(["已完成", "进行中", "待跟进"]),
                    "progress": randint(30, 100)
                })

            report = WorkReport(
                id=f"report_{uuid.uuid4().hex[:12]}",
                title=f"{date}日报",
                type="daily",
                date=date,
                period=date,
                summary=f"{info['name']}的{date}工作日报，完成{randint(3,8)}项工作内容。",
                achievements=f"1. 完成达人对接{randint(2,5)}个\n2. 更新资源库{randint(5,20)}条\n3. 跟进合作意向{randint(1,3)}个",
                problems=f"1. 部分达人回复较慢\n2. 样品物流有延迟",
                plans=f"1. 继续跟进未回复达人\n2. 准备下周直播排期\n3. 整理月度数据",
                work_items=json.dumps(work_items, ensure_ascii=False),
                target_amount=str(randint(5000, 50000)),
                completed_amount=str(randint(3000, 45000)),
                customer_count=str(randint(10, 50)),
                new_customer_count=str(randint(1, 10)),
                author=info["name"],
                author_id=uid,
                department="BD部",
                company=info["company"],
                company_id="",
                status="submitted",
                approval_status="approved" if is_admin else choice(["pending", "approved"]),
                approver="超级管理员" if is_admin else "",
                approved_at=NOW_ISO if is_admin else "",
                approval_comments="[]",
                attachments="[]",
            )
            db.add(report)
            added += 1

    # 过去2周的周报
    for week_offset in range(2):
        week_start = (datetime.now() - timedelta(weeks=week_offset+1, days=datetime.now().weekday())).strftime("%Y-%m-%d")
        week_end_date = datetime.now() - timedelta(weeks=week_offset+1, days=datetime.now().weekday()) + timedelta(days=4)
        week_end = week_end_date.strftime("%Y-%m-%d")

        for uid in user_ids:
            # 80%概率提交了周报
            if random() < 0.2 and week_offset > 0:
                continue
            info = user_map[uid]
            report = WorkReport(
                id=f"report_{uuid.uuid4().hex[:12]}",
                title=f"周报 {week_start}~{week_end}",
                type="weekly",
                date=week_start,
                period=f"{week_start}~{week_end}",
                summary=f"{info['name']}的周报，本周完成主要工作{randint(5,15)}项。",
                achievements=f"1. 新增达人资源{randint(10,30)}条\n2. 签约合作达人{randint(2,8)}个\n3. 达成GMV {randint(1,10)}万元",
                problems="1. 部分达人佣金谈判困难\n2. 新人培训进度偏慢",
                plans="1. 加大达人开发力度\n2. 推进重点达人签约\n3. 优化工作流程",
                work_items="[]",
                target_amount=str(randint(30000, 200000)),
                completed_amount=str(randint(20000, 180000)),
                customer_count=str(randint(30, 100)),
                new_customer_count=str(randint(5, 25)),
                author=info["name"],
                author_id=uid,
                department="BD部",
                company=info["company"],
                company_id="",
                status="submitted",
                approval_status="approved",
                approver="超级管理员",
                approved_at=NOW_ISO,
                approval_comments="[]",
                attachments="[]",
            )
            db.add(report)
            added += 1

    db.commit()
    print(f"  ✅ work_reports: 新增 {added} 条")


def seed_calendar_tasks(db, user_map):
    """填充日历任务"""
    existing_count = db.query(CalendarTask).count()
    if existing_count >= 50:
        print(f"  ⏭ calendar_tasks: 已有 {existing_count} 条，跳过")
        return

    added = 0
    user_ids = list(user_map.keys())

    # 过去7天 + 未来7天的任务
    for day_offset in range(-7, 8):
        date = (datetime.now() + timedelta(days=day_offset)).strftime("%Y-%m-%d")
        # 每天20-70条任务（保证有的员工满60，有的不满）
        task_count = randint(20, 70)
        for _ in range(task_count):
            uid = choice(user_ids)
            info = user_map[uid]
            is_past = day_offset < 0
            is_today = day_offset == 0

            task = CalendarTask(
                id=f"task_{uuid.uuid4().hex[:12]}",
                date_key=date,
                action=choice(TASK_ACTIONS),
                responsible=info["name"],
                risk=choice(["无", "无", "无", "达人回复慢", "佣金谈判难", "样品不足", "时间紧迫"]),
                status=choice(["completed"] * 3 + ["in_progress", "pending"]) if is_past else choice(["pending"] * 3 + ["in_progress"]),
                amount=round(uniform(500, 20000), 2),
                target_amount=round(uniform(10000, 100000), 2),
                completed_amount=round(uniform(5000, 90000), 2) if is_past else 0,
                created_by=uid,
            )
            db.add(task)
            added += 1

    db.commit()
    print(f"  ✅ calendar_tasks: 新增 {added} 条")


def seed_daily_targets(db, user_map):
    """填充每日目标"""
    existing_count = db.query(DailyTarget).count()
    if existing_count >= 10:
        print(f"  ⏭ daily_targets: 已有 {existing_count} 条，跳过")
        return

    # 获取已有日期
    existing_dates = {r[0] for r in db.query(DailyTarget.date_key).all()}

    added = 0
    for day_offset in range(-7, 8):
        date = (datetime.now() + timedelta(days=day_offset)).strftime("%Y-%m-%d")
        if date in existing_dates:
            continue
        target = DailyTarget(
            id=str(uuid.uuid4()),
            date_key=date,
            target_amount=round(uniform(50000, 200000), 2),
            completed_amount=round(uniform(30000, 180000), 2),
            created_by="admin-001",
        )
        db.add(target)
        added += 1

    db.commit()
    print(f"  ✅ daily_targets: 新增 {added} 条")


def seed_daren_resources(db, user_map):
    """填充达人资源库"""
    existing_count = db.query(DarenResource).count()
    if existing_count >= 30:
        print(f"  ⏭ daren_resources: 已有 {existing_count} 条，跳过")
        return

    added = 0
    user_ids = list(user_map.keys())

    for i, daren_name in enumerate(DAREN_NAMES[:60]):  # 60个达人资源
        uid = choice(user_ids)
        info = user_map[uid]
        platform = choice(PLATFORMS)
        followers = choice(["1-5万", "5-10万", "10-50万", "50-100万", "100万+", "500万+"])
        cats = [choice(CATEGORIES_POOL) for _ in range(randint(1, 3))]
        tags = [choice(["优质", "活跃", "潜力", "稳定", "高ROI", "复播", "新合作", "重点跟进"]) for _ in range(randint(1, 3))]

        first_contact = (datetime.now() - timedelta(days=randint(7, 90))).strftime("%Y-%m-%d")
        latest_follow = (datetime.now() - timedelta(days=randint(0, 14))).strftime("%Y-%m-%d")
        next_follow = (datetime.now() + timedelta(days=randint(1, 7))).strftime("%Y-%m-%d")

        resource = DarenResource(
            id=f"daren_{uuid.uuid4().hex[:12]}",
            name=info["name"],
            date=TODAY,
            daren_id=f"D{10000+i}",
            daren_name=daren_name,
            platform=platform,
            contact=f"wx_{daren_name[:3]}{randint(100,999)}",
            position=choice(POSITIONS),
            position_other="",
            followers=followers,
            categories=cats,
            fan_portrait=choice(["18-35岁女性为主", "25-40岁家庭用户", "18-25岁年轻群体", "30-50岁高消费群体", "全年龄段"]),
            gmv=choice(["0-5万", "5-20万", "20-50万", "50-100万", "100万+"]),
            channel=choice(CHANNELS),
            first_contact_date=first_contact,
            latest_follow_date=latest_follow,
            next_follow_date=next_follow,
            tags=tags,
            special_requirement=choice(["无", "需要样品", "需开票", "独家合作", "定制方案"]),
            special_requirement_note="",
            remarks=f"通过{choice(CHANNELS)}渠道认识，{choice(['首次沟通顺利', '需进一步跟进', '有合作意向', '暂无档期'])}",
            created_by=uid,
            updated_by=uid,
        )
        db.add(resource)
        added += 1

    db.commit()
    print(f"  ✅ daren_resources: 新增 {added} 条")


def seed_influencer_records(db, user_map):
    """填充达人合作台账"""
    existing_count = db.query(InfluencerRecord).count()
    if existing_count >= 20:
        print(f"  ⏭ influencer_records: 已有 {existing_count} 条，跳过")
        return

    added = 0
    user_ids = list(user_map.keys())

    for i, daren_name in enumerate(DAREN_NAMES[:30]):
        uid = choice(user_ids)
        info = user_map[uid]
        coop_start = (datetime.now() - timedelta(days=randint(30, 180))).strftime("%Y-%m-%d")
        coop_end = (datetime.now() + timedelta(days=randint(30, 180))).strftime("%Y-%m-%d")
        gmv_val = round(uniform(5000, 500000), 2)

        record = InfluencerRecord(
            id=f"inf_{uuid.uuid4().hex[:12]}",
            user_id=uid,
            user_name=info["name"],
            date=TODAY,
            influencer_id=f"D{10000+i}",
            influencer_name=daren_name,
            contact=f"wx_{daren_name[:3]}{randint(100,999)}",
            platform=choice(PLATFORMS),
            platform_uid=f"uid_{randint(100000, 999999)}",
            commission_rate=round(uniform(10, 40), 1),
            traffic_method=choice(["直播", "短视频", "图文", "直播+短视频"]),
            cooperation_start=coop_start,
            cooperation_end=coop_end,
            compliance_status=choice(["合规", "合规", "合规", "待审核", "已过期"]),
            gmv=gmv_val,
            roi=round(uniform(1.5, 8.0), 2),
            conversion_rate=round(uniform(0.5, 5.0), 2),
            return_rate=round(uniform(1, 15), 2),
            payment_status=choice(["已结算", "已结算", "待结算", "部分结算"]),
            re_broadcast_willingness=choice(["愿意", "愿意", "愿意", "待确认", "不愿意"]),
            re_broadcast_date=(datetime.now() + timedelta(days=randint(3, 30))).strftime("%Y-%m-%d"),
            remarks=choice(["合作稳定，持续跟进", "首次合作效果良好", "需优化选品策略", "佣金谈判中"]),
        )
        db.add(record)
        added += 1

    db.commit()
    print(f"  ✅ influencer_records: 新增 {added} 条")


def seed_training_docs(db, user_map):
    """填充培训知识库文档"""
    existing_count = db.query(TrainingDoc).count()
    if existing_count >= 10:
        print(f"  ⏭ training_docs: 已有 {existing_count} 条，跳过")
        return

    docs_data = [
        ("BD自查手册-品牌核心信息", "bd", "knowledge", 1, """## 品牌定位
赵宜主专注国人体质的高性价比每日营养包，致力于让每个中国人都能轻松获得科学营养补充。

## 品牌实力
- 合作品牌达人超过5000+
- 月均GMV突破2000万
- 供应链全自有，品质可控
- 获得多项行业认证

## 核心优势
1. 高性价比：同品质产品价格低30%
2. 出片率高：产品效果可视化强
3. 复购率好：月度复购率达65%
4. 佣金丰厚：行业领先佣金比例

## 介绍口径
"赵宜主是专注国人体质的每日营养品牌，我们的产品经过权威认证，性价比极高，非常适合您的粉丝群体。"
"""),
        ("BD自查手册-产品体系", "bd", "knowledge", 2, """## 核心产品线
1. 每日营养包（明星产品）- 适合所有人群
2. 儿童成长营养包 - 适合母婴达人
3. 中老年骨关节营养包 - 适合中老年粉丝达人
4. 女性美容营养包 - 适合美妆达人

## 卖点速查
- 每日营养包：全营养、易冲泡、口感好
- 儿童成长包：DHA+钙+锌，一包搞定
- 中老年包：氨糖+钙+VD，关节骨双护

## 适配达人
| 达人类型 | 推荐产品 | 佣金区间 |
|---------|---------|---------|
| 美妆博主 | 女性美容包 | 25-35% |
| 母婴博主 | 儿童成长包 | 20-30% |
| 健康博主 | 每日营养包 | 22-32% |
"""),
        ("BD自查手册-合作政策", "bd", "knowledge", 3, """## 佣金规则
- 开票：佣金20%-30%
- 不开票：佣金25%-35%
- 独家合作额外+5%

## 合作模式
1. 纯佣金：按成交金额×佣金比例
2. 长期合作：签约3个月以上享优惠
3. 品牌专场：保底+佣金模式

## 达人福利
- 首次合作赠送产品体验装
- 月度GMV达标奖励
- 季度优秀合作伙伴奖金
- 专属素材包支持
"""),
        ("SOP-达人筛选标准", "sop", "knowledge", 4, """## 获客渠道
1. 平台搜索：抖音/快手/小红书关键词搜索
2. 竞品关注：观察竞品合作达人
3. 行业社群：加入达人BD交流群
4. 展会活动：参加行业展会

## 判定标准
- 粉丝量：1万以上（KOC可放宽至5000）
- 互动率：≥3%
- 内容质量：原创内容占比≥80%
- 带货记录：有同类产品带货经验优先

## 筛选动作
1. 初筛：查看主页数据
2. 深筛：分析近30天直播数据
3. 验证：联系确认合作意向
"""),
        ("SOP-首次触达开发", "sop", "knowledge", 5, """## 事前准备
1. 了解达人内容风格和粉丝画像
2. 准备品牌资料包（产品图+卖点+佣金方案）
3. 确定沟通话术模板

## 沟通要点
1. 自我介绍+品牌亮点（30秒内）
2. 粉丝匹配度分析
3. 合作方案初稿
4. 解答达人疑问

## 跟进时效
- 首次沟通后24h内发送详细方案
- 方案发送后48h内确认意向
- 确认意向后3个工作日内签约
"""),
        ("产品知识-核心卖点", "product", "knowledge", 6, """## 产品卖点对照表

### 每日营养包
- 🎯 卖点1：科学配比，37种营养素一包搞定
- 🎯 卖点2：口感好，比冲剂好喝10倍
- 🎯 卖点3：独立包装，随身携带

### 儿童成长包
- 🎯 卖点1：DHA+钙+锌，三效合一
- 🎯 卖点2：无糖配方，不伤牙
- 🎯 卖点3：水果味，孩子爱喝

### 对比优势
| 维度 | 赵宜主 | 竞品A | 竞品B |
|-----|-------|------|------|
| 价格 | ¥89/月 | ¥129/月 | ¥159/月 |
| 营养素数量 | 37种 | 21种 | 28种 |
| 口感评分 | 4.8 | 3.9 | 4.2 |
"""),
        ("常见问题FAQ", "other", "knowledge", 7, """## Q1: 佣金什么时候结算？
A: 每月15号结算上月佣金，T+15到账。

## Q2: 样品怎么申请？
A: 首次合作可申请1份体验装，填写申请表后3个工作日内发货。

## Q3: 可以独家合作吗？
A: 可以，独家合作佣金额外+5%，需签约3个月以上。

## Q4: 产品保质期多久？
A: 18个月，建议开封后60天内用完。

## Q5: 退换货政策？
A: 7天无理由退换，质量问题全额退款。

## Q6: 直播间怎么介绍产品？
A: 参考话术模板，核心3分钟讲解：痛点→方案→效果→优惠。
"""),
        ("销售规范-沟通话术", "销售规范", "knowledge", 8, """## 开场话术
"您好，我是赵宜主BD经理XX，关注您的内容很久了，您粉丝画像和我们的产品非常匹配..."

## 产品介绍话术
"赵宜主每日营养包，37种营养素一包搞定，只需89元/月，性价比远超同类产品..."

## 异议处理
- "价格太贵" → "89元/月，每天不到3元，比一杯奶茶还便宜"
- "没听过这个品牌" → "我们是新锐品牌，重点投入达人合作，所以佣金力度很大"
- "粉丝不匹配" → "我们有多款产品，可以针对您的粉丝群体定制方案"

## 促单话术
"本月签约额外送价值299元的产品体验装，名额有限哦..."
"""),
        ("客服规范-常见售后问题", "客服规范", "knowledge", 9, """## 物流问题
- 发货时效：下单后48小时内
- 快递公司：默认中通/圆通
- 查询方式：订单号+快递100

## 退换货流程
1. 客户提交退换申请
2. 客服审核（1个工作日）
3. 审核通过后发送退货地址
4. 收到退货后3个工作日内处理

## 质量问题处理
- 拍照取证
- 登记问题类型
- 补发或退款
- 反馈供应链改进
"""),
        ("公司制度-考勤与绩效", "公司制度", "knowledge", 10, """## 考勤制度
- 工作时间：9:00-18:00（午休12:00-13:00）
- 打卡方式：企业微信打卡
- 迟到：9:00后打卡视为迟到
- 早退：18:00前离开视为早退

## 绩效考核
### 月度考核指标
1. 达人开发数量（权重30%）
2. 合作签约数量（权重25%）
3. GMV贡献（权重25%）
4. 日报周报提交率（权重10%）
5. 培训学习完成度（权重10%）

### 评级标准
- S级：总分≥95
- A级：85≤总分<95
- B级：70≤总分<85
- C级：60≤总分<70
- D级：总分<60
"""),
    ]

    added = 0
    user_ids = list(user_map.keys())
    for title, category, source_type, chapter, content in docs_data:
        uid = choice(user_ids)
        info = user_map[uid]
        doc = TrainingDoc(
            id=f"doc_{uuid.uuid4().hex[:12]}",
            title=title,
            content=content,
            category=category,
            source_type=source_type,
            author=info["name"],
            author_id=uid,
            chapter_number=chapter,
            views=randint(10, 500),
        )
        db.add(doc)
        added += 1

    db.commit()
    print(f"  ✅ training_docs: 新增 {added} 条")


def seed_quiz_questions(db):
    """填充刷题库"""
    existing_count = db.query(QuizQuestion).count()
    if existing_count >= 20:
        print(f"  ⏭ quiz_questions: 已有 {existing_count} 条，跳过")
        return

    questions = [
        # 销售规范
        ("赵宜主每日营养包包含多少种营养素？", ["21种", "28种", "37种", "45种"], "C", "赵宜主每日营养包科学配比37种营养素，一包搞定每日所需。", "销售规范", "easy"),
        ("赵宜主每日营养包月费是多少？", ["59元", "89元", "129元", "159元"], "B", "赵宜主每日营养包每月只需89元，每天不到3元。", "销售规范", "easy"),
        ("达人首次触达后，方案发送时效要求是多久？", ["12小时内", "24小时内", "48小时内", "72小时内"], "B", "首次沟通后24h内必须发送详细方案。", "销售规范", "medium"),
        ("独家合作佣金额外增加多少？", ["3%", "5%", "8%", "10%"], "B", "独家合作额外+5%佣金，需签约3个月以上。", "销售规范", "medium"),
        ("不开票佣金比例区间是？", ["15%-25%", "20%-30%", "25%-35%", "30%-40%"], "C", "不开票佣金25%-35%，开票佣金20%-30%。", "销售规范", "medium"),
        # 技术文档
        ("达人筛选时粉丝量最低要求是多少？", ["3000", "5000", "10000", "20000"], "C", "达人筛选粉丝量要求1万以上，KOC可放宽至5000。", "技术文档", "medium"),
        ("达人互动率合格线是多少？", ["≥1%", "≥2%", "≥3%", "≥5%"], "C", "互动率≥3%为合格，过低说明粉丝质量差。", "技术文档", "medium"),
        ("确认合作意向后签约时效要求？", ["1个工作日", "3个工作日", "5个工作日", "7个工作日"], "B", "确认意向后3个工作日内完成签约。", "技术文档", "medium"),
        # 客服规范
        ("客户下单后多久发货？", ["24小时内", "48小时内", "72小时内", "5天内"], "B", "下单后48小时内发货，默认中通/圆通。", "客服规范", "easy"),
        ("退货审核处理时限？", ["1个工作日", "3个工作日", "5个工作日", "7个工作日"], "A", "退货申请1个工作日内审核完毕。", "客服规范", "easy"),
        ("赵宜主产品保质期多久？", ["6个月", "12个月", "18个月", "24个月"], "C", "产品保质期18个月，开封后建议60天内用完。", "客服规范", "easy"),
        ("7天无理由退换的条件是什么？", ["未开封", "不影响二次销售", "任意条件", "仅限质量问题"], "B", "7天无理由退换要求不影响二次销售。", "客服规范", "medium"),
        # 公司制度
        ("月度绩效考核中，达人开发数量权重占比多少？", ["20%", "25%", "30%", "35%"], "C", "达人开发数量权重30%，是最大权重指标。", "公司制度", "medium"),
        ("S级绩效评级需要总分达到多少？", ["90分", "93分", "95分", "98分"], "C", "S级要求总分≥95分。", "公司制度", "medium"),
        ("每日任务配额标准是多少条？", ["30条", "40条", "50条", "60条"], "D", "每日任务配额标准为60条，不足会触发告警。", "公司制度", "hard"),
        # 产品知识
        ("儿童成长营养包的核心卖点是什么？", ["高钙配方", "DHA+钙+锌三效合一", "有机原料", "进口品质"], "B", "儿童成长包核心卖点是DHA+钙+锌，三效合一。", "产品知识", "easy"),
        ("赵宜主相比竞品A每月便宜多少？", ["20元", "40元", "60元", "80元"], "B", "赵宜主89元/月，竞品A 129元/月，便宜40元。", "产品知识", "medium"),
        ("赵宜主每日营养包的口感评分为？", ["3.9", "4.2", "4.5", "4.8"], "D", "赵宜主口感评分4.8分，远高于竞品。", "产品知识", "medium"),
        ("佣金结算日是每月几号？", ["1号", "10号", "15号", "20号"], "C", "每月15号结算上月佣金，T+15到账。", "公司制度", "hard"),
        ("首次合作可以申请几份体验装？", ["1份", "2份", "3份", "5份"], "A", "首次合作可申请1份体验装，3个工作日内发货。", "销售规范", "easy"),
    ]

    added = 0
    for question, options, answer, explanation, category, difficulty in questions:
        q = QuizQuestion(
            id=f"quiz_{uuid.uuid4().hex[:12]}",
            question=question,
            options=options,
            answer=answer,
            explanation=explanation,
            category=category,
            difficulty=difficulty,
        )
        db.add(q)
        added += 1

    db.commit()
    print(f"  ✅ quiz_questions: 新增 {added} 条")


def seed_quiz_records(db, user_map):
    """填充答题记录"""
    existing_count = db.query(QuizRecord).count()
    if existing_count >= 30:
        print(f"  ⏭ quiz_records: 已有 {existing_count} 条，跳过")
        return

    questions = db.query(QuizQuestion).all()
    if not questions:
        print("  ⏭ quiz_records: 无题目，跳过")
        return

    added = 0
    user_ids = list(user_map.keys())

    for uid in user_ids:
        # 每人答5-15题
        for q in [choice(questions) for _ in range(randint(5, 15))]:
            is_correct = random() < 0.7  # 70%正确率
            user_answer = q.answer if is_correct else choice([o for o in ["A", "B", "C", "D"] if o != q.answer])
            record = QuizRecord(
                id=str(uuid.uuid4()),
                user_id=uid,
                question_id=q.id,
                user_answer=user_answer,
                is_correct=1 if is_correct else 0,
                category=q.category,
            )
            db.add(record)
            added += 1

    db.commit()
    print(f"  ✅ quiz_records: 新增 {added} 条")


def seed_training_problems(db, user_map):
    """填充难题库"""
    existing_count = db.query(TrainingProblem).count()
    if existing_count >= 10:
        print(f"  ⏭ training_problems: 已有 {existing_count} 条，跳过")
        return

    problems = [
        ("达人佣金谈判陷入僵局", "达人坚持35%佣金，而公司最高只能给30%，双方无法达成一致。", "1. 分析达人数据，评估ROI\n2. 提出保底+佣金方案\n3. 增加非金钱福利（素材包、优先选品）\n4. 请上级审批特殊佣金", "客户谈判", "approved"),
        ("达人直播效果低于预期", "达人首播GMV仅完成目标的30%，转化率0.8%远低于行业平均。", "1. 分析直播回放，找出问题点\n2. 优化选品策略，调整产品组合\n3. 提前沟通话术要点\n4. 安排二次直播测试", "直播运营", "approved"),
        ("新人BD转化率过低", "入职3个月的新人BD，达人签约转化率仅5%，远低于团队平均15%。", "1. 安排师傅一对一辅导\n2. 增加模拟训练频次\n3. 分析失败案例，总结经验\n4. 调整KPI目标，设置阶段性目标", "团队管理", "pending"),
        ("达人样品物流丢失", "价值2000元的产品样品在物流过程中丢失，达人对此不满。", "1. 立即联系物流公司理赔\n2. 同步补发样品，加急配送\n3. 向达人致歉并提供额外优惠\n4. 更换更可靠的物流渠道", "物流售后", "approved"),
        ("竞争对手挖角合作达人", "竞品以更高佣金挖走了3个长期合作达人。", "1. 分析达人流失原因\n2. 制定达人留存计划\n3. 提供独家福利增加粘性\n4. 加强关系维护，定期回访", "竞争策略", "pending"),
        ("达人内容违规下架", "达人发布的合作短视频因违规被平台下架，影响推广效果。", "1. 分析违规原因\n2. 指导达人修改内容\n3. 加强发布前审核流程\n4. 制定内容合规指引", "合规风控", "approved"),
        ("月底GMV冲刺压力", "距离月底还有5天，GMV完成率仅75%，需要冲刺完成目标。", "1. 盘点可调用达人资源\n2. 安排加场直播\n3. 推出限时促销活动\n4. 激励头部达人加大推广", "业绩管理", "pending"),
        ("多平台达人数据汇总困难", "抖音、快手、小红书三个平台数据格式不统一，月度汇总耗时长。", "1. 制定统一数据模板\n2. 使用数据采集工具\n3. 建立自动化汇总流程\n4. 培训团队数据录入规范", "工作流程", "approved"),
    ]

    added = 0
    user_ids = list(user_map.keys())
    for title, desc, solution, category, status in problems:
        uid = choice(user_ids)
        info = user_map[uid]
        problem = TrainingProblem(
            id=f"problem_{uuid.uuid4().hex[:12]}",
            title=title,
            description=desc,
            solution=solution,
            category=category,
            status=status,
            review_comment="方案可行，请执行" if status == "approved" else "",
            created_by=uid,
        )
        db.add(problem)
        added += 1

    db.commit()
    print(f"  ✅ training_problems: 新增 {added} 条")


def seed_meetings(db, user_map):
    """填充会议记录"""
    existing_count = db.query(Meeting).count()
    if existing_count >= 5:
        print(f"  ⏭ meetings: 已有 {existing_count} 条，跳过")
        return

    meetings_data = [
        ("6月第1周BD团队周会", "1. 回顾上周GMV完成情况\n2. 分析达人开发进度\n3. 本周重点任务分配\n4. 新人培训进展汇报", "本周哪个达人合作案例最值得借鉴？"),
        ("Q2季度业绩复盘会", "1. Q2 GMV达成率分析\n2. 各分公司业绩对比\n3. 达人合作效率评估\n4. Q3目标制定讨论", "Q3增长的最大机会点在哪里？"),
        ("达人合作政策调整讨论", "1. 当前佣金体系分析\n2. 竞品政策对比\n3. 新政策方案讨论\n4. 实施时间表确认", "新佣金政策对现有达人会有什么影响？"),
        ("新人培训方案评审", "1. 培训课程体系介绍\n2. 实战项目安排\n3. 考核标准制定\n4. 导师分配方案", "如何衡量新人培训的效果？"),
        ("618大促方案讨论", "1. 618活动方案\n2. 达人直播排期\n3. 库存备货计划\n4. 应急预案制定", "618期间如何保证达人直播质量？"),
    ]

    added = 0
    user_ids = list(user_map.keys())

    for title, content, question in meetings_data:
        uid = choice(user_ids)
        meeting = Meeting(
            id=f"meeting_{uuid.uuid4().hex[:12]}",
            title=title,
            content=content,
            question=question,
            created_by=uid,
        )
        db.add(meeting)
        db.flush()  # 获取meeting.id

        # 每个会议3-6个人回答
        answerers = [choice(user_ids) for _ in range(randint(3, 6))]
        answerers = list(set(answerers))[:6]  # 去重
        for auid in answerers:
            info = user_map[auid]
            answer = MeetingAnswer(
                id=str(uuid.uuid4()),
                meeting_id=meeting.id,
                user_id=auid,
                user_name=info["name"],
                answer=choice([
                    "我认为重点是提升达人筛选效率，降低无效沟通成本。",
                    "建议优化佣金阶梯方案，激励头部达人产出更多。",
                    "需要加强新人培训，特别是话术和异议处理能力。",
                    "建议建立达人分级管理制度，差异化投入资源。",
                    "关键是要提升复播率，单次合作ROI还有提升空间。",
                    "可以尝试引入达人推荐达人机制，扩大资源池。",
                ]),
            )
            db.add(answer)
            added += 1

        added += 1

    db.commit()
    print(f"  ✅ meetings + meeting_answers: 新增 {added} 条")


def main():
    print("=" * 50)
    print("  X10 V2 种子数据填充")
    print("=" * 50)
    print()

    db = SessionLocal()
    try:
        # 1. 用户
        print("📝 [1/9] 填充用户...")
        seed_users(db)
        user_map = get_user_map(db)

        # 2. 工作报告
        print("📝 [2/9] 填充工作报告...")
        seed_work_reports(db, user_map)

        # 3. 日历任务
        print("📝 [3/9] 填充日历任务...")
        seed_calendar_tasks(db, user_map)

        # 4. 每日目标
        print("📝 [4/9] 填充每日目标...")
        seed_daily_targets(db, user_map)

        # 5. 达人资源库
        print("📝 [5/9] 填充达人资源库...")
        seed_daren_resources(db, user_map)

        # 6. 达人合作台账
        print("📝 [6/9] 填充达人合作台账...")
        seed_influencer_records(db, user_map)

        # 7. 培训文档
        print("📝 [7/9] 填充培训文档...")
        seed_training_docs(db, user_map)

        # 8. 刷题库 + 答题记录
        print("📝 [8/9] 填充刷题库...")
        seed_quiz_questions(db)
        seed_quiz_records(db, user_map)

        # 9. 难题库 + 会议
        print("📝 [9/9] 填充难题库和会议...")
        seed_training_problems(db, user_map)
        seed_meetings(db, user_map)

        # 统计结果
        print()
        print("=" * 50)
        print("  📊 数据填充完成，最终统计：")
        print("=" * 50)

        from sqlalchemy import text
        tables = ["users", "work_reports", "calendar_tasks", "daily_targets",
                  "daren_resources", "influencer_records",
                  "training_docs", "quiz_questions", "quiz_records",
                  "training_problems", "meetings", "meeting_answers"]
        for t in tables:
            result = db.execute(text(f"SELECT COUNT(*) FROM [{t}]"))
            count = result.scalar()
            print(f"  {t}: {count} 条")

        print()
        print("  🔑 默认密码统一为: 123456")
        print()

    except Exception as e:
        print(f"❌ 错误: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
