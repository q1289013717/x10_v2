import uuid
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.core.config import settings
from app.core.database import engine, Base
from app.models import *  # noqa: 确保所有模型被导入
from app.api import auth, tasks, reports, training, daren, influencers, meetings, admin


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 注册路由
    app.include_router(auth.router)
    app.include_router(tasks.router)
    app.include_router(reports.router)
    app.include_router(training.router)
    app.include_router(daren.router)
    app.include_router(influencers.router)
    app.include_router(meetings.router)
    app.include_router(meetings.router_config)
    app.include_router(admin.router)

    @app.on_event("startup")
    def startup():
        Base.metadata.create_all(bind=engine)
        # 初始化默认数据
        init_default_data()

    @app.get("/")
    def root():
        return {
            "name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "docs": "/docs",
        }

    @app.get("/api/health")
    def health_check():
        return {"status": "ok"}

    # =====================================================
    # 前端静态文件（生产环境：Docker 多阶段构建产出）
    # 注意：StaticFiles 必须在所有 API 路由之后注册
    # =====================================================
    STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    if os.path.isdir(STATIC_DIR):
        # 挂载 /assets 目录（Vite 打包的 JS/CSS/图片）
        assets_dir = os.path.join(STATIC_DIR, "assets")
        if os.path.isdir(assets_dir):
            app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

        # SPA 回退：所有非 API 路径返回 index.html
        index_path = os.path.join(STATIC_DIR, "index.html")
        if os.path.isfile(index_path):

            @app.get("/{full_path:path}")
            async def serve_spa(full_path: str):
                # 只对非 API 路径做 SPA 回退
                return FileResponse(index_path)

    return app


def init_default_data():
    """初始化默认管理员账号、分类数据及种子数据"""
    from app.core.database import SessionLocal
    from app.core.security import get_password_hash
    from app.models.user import User
    from app.models.training import TrainingCategory, TrainingDoc, QuizQuestion, QuizRecord, TrainingProblem
    from app.models.report import WorkReport
    from app.models.task import CalendarTask, DailyTarget
    from app.models.influencer import DarenResource, InfluencerRecord
    from app.models.meeting import Meeting, MeetingAnswer, SystemConfig
    from random import choice, randint, uniform, random as rand_float

    db = SessionLocal()
    try:
        # 检查是否已有数据
        existing_admin = db.query(User).filter(User.account == "admin").first()
        if not existing_admin:
            # 创建默认管理员
            admin = User(
                id="admin-001",
                account="admin",
                name="管理员",
                password=get_password_hash("123123"),
                role="集团管理员",
                company="集团总部",
                status="active",
                avatar="A",
            )
            db.add(admin)

            # 初始化默认分类
            knowledge_cats = [
                ("销售规范", "knowledge", 1),
                ("技术文档", "knowledge", 2),
                ("客服规范", "knowledge", 3),
                ("公司制度", "knowledge", 4),
                ("产品知识", "knowledge", 5),
            ]
            personal_cats = [
                ("个人笔记", "personal", 1),
                ("学习心得", "personal", 2),
                ("工作经验", "personal", 3),
                ("技术总结", "personal", 4),
            ]
            problem_cats = [
                ("技术故障", "problem", 1),
                ("客服问题", "problem", 2),
                ("销售难题", "problem", 3),
                ("流程问题", "problem", 4),
                ("沟通障碍", "problem", 5),
                ("其他问题", "problem", 6),
            ]
            quiz_cats = [
                ("销售规范", "quiz", 1),
                ("技术文档", "quiz", 2),
                ("客服规范", "quiz", 3),
                ("公司制度", "quiz", 4),
                ("产品知识", "quiz", 5),
            ]

            for name, t, order in knowledge_cats + personal_cats + problem_cats + quiz_cats:
                db.add(TrainingCategory(name=name, type=t, sort_order=order))

            # 系统默认配置
            db.add(SystemConfig(config_key="system_name", config_value="X10增长引擎"))
            db.add(SystemConfig(config_key="company_name", config_value="让目标清晰，让过程可见，让增长可复制"))

            db.commit()
            print("[init] 默认数据初始化完成")

            # ===== 种子数据填充（仅当环境变量 SEED_DEMO_DATA=true 时执行） =====
            if os.getenv("SEED_DEMO_DATA", "").lower() == "true":
                _seed_demo_data(db)
            else:
                print("[init] SEED_DEMO_DATA 未启用，跳过演示数据填充")
        else:
            print("[init] 数据库已有数据，跳过初始化")

    except Exception as e:
        db.rollback()
        print(f"[init] 初始化失败: {e}")
    finally:
        db.close()


def _seed_demo_data(db):
    """填充演示数据（仅当 SEED_DEMO_DATA=true 时执行，默认不填充）"""
    import json as _json
    from datetime import datetime, timedelta
    from random import choice as _choice, randint as _randint, uniform as _uniform

    try:
        # ── 员工 ──
        employees = [
            ("zhangwei", "张伟", "分公司管理员", "上海分公司"),
            ("liuna", "刘娜", "员工", "上海分公司"),
            ("wangfang", "王芳", "员工", "上海分公司"),
            ("chenming", "陈明", "员工", "北京分公司"),
            ("liuyang", "刘洋", "员工", "北京分公司"),
            ("zhaoli", "赵丽", "员工", "广州分公司"),
            ("sunqiang", "孙强", "员工", "广州分公司"),
            ("huangjie", "黄杰", "分公司管理员", "深圳分公司"),
            ("wumin", "吴敏", "员工", "深圳分公司"),
        ]
        user_map = {"admin-001": {"name": "管理员", "role": "集团管理员", "company": "集团总部"}}
        for account, name, role, company in employees:
            uid = str(uuid.uuid4())
            db.add(User(
                id=uid, account=account, name=name,
                password=get_password_hash("123456"),
                role=role, company=company, status="active", avatar=name[0],
            ))
            user_map[uid] = {"name": name, "role": role, "company": company}
        db.flush()
        user_ids = list(user_map.keys())

        # ── 达人资源库 (60条) ──
        daren_names = [
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
        ]
        platforms = ["抖音", "快手", "小红书", "B站", "微博", "视频号"]
        positions = ["头部达人", "腰部达人", "素人", "KOC", "中腰部达人"]
        cat_pool = ["美妆", "食品", "家居", "数码", "母婴", "服饰", "运动", "旅游", "教育", "健康"]
        channels = ["自主开发", "同行推荐", "平台推荐", "展会认识", "朋友介绍"]

        for i, dname in enumerate(daren_names):
            uid = _choice(user_ids)
            info = user_map[uid]
            first_contact = (datetime.now() - timedelta(days=_randint(7, 90))).strftime("%Y-%m-%d")
            latest_follow = (datetime.now() - timedelta(days=_randint(0, 14))).strftime("%Y-%m-%d")
            next_follow = (datetime.now() + timedelta(days=_randint(1, 7))).strftime("%Y-%m-%d")
            db.add(DarenResource(
                id=f"daren_{uuid.uuid4().hex[:12]}", name=info["name"], date=datetime.now().strftime("%Y-%m-%d"),
                daren_id=f"D{10000+i}", daren_name=dname, platform=_choice(platforms),
                contact=f"wx_{dname[:3]}{_randint(100,999)}", position=_choice(positions),
                followers=_choice(["1-5万", "5-10万", "10-50万", "50-100万", "100万+"]),
                categories=[_choice(cat_pool) for _ in range(_randint(1, 3))],
                fan_portrait=_choice(["18-35岁女性为主", "25-40岁家庭用户", "18-25岁年轻群体", "30-50岁高消费群体"]),
                gmv=_choice(["0-5万", "5-20万", "20-50万", "50-100万", "100万+"]),
                channel=_choice(channels), first_contact_date=first_contact,
                latest_follow_date=latest_follow, next_follow_date=next_follow,
                tags=[_choice(["优质", "活跃", "潜力", "稳定", "高ROI", "复播"]) for _ in range(_randint(1, 3))],
                special_requirement=_choice(["无", "需要样品", "需开票", "独家合作"]),
                remarks=f"通过{_choice(channels)}渠道认识",
                created_by=uid, updated_by=uid,
            ))

        # ── 达人合作台账 (30条) ──
        for i, dname in enumerate(daren_names[:30]):
            uid = _choice(user_ids)
            info = user_map[uid]
            coop_start = (datetime.now() - timedelta(days=_randint(30, 180))).strftime("%Y-%m-%d")
            coop_end = (datetime.now() + timedelta(days=_randint(30, 180))).strftime("%Y-%m-%d")
            db.add(InfluencerRecord(
                id=f"inf_{uuid.uuid4().hex[:12]}", user_id=uid, user_name=info["name"],
                date=datetime.now().strftime("%Y-%m-%d"), influencer_id=f"D{10000+i}",
                influencer_name=dname, contact=f"wx_{dname[:3]}{_randint(100,999)}",
                platform=_choice(platforms), platform_uid=f"uid_{_randint(100000, 999999)}",
                commission_rate=round(_uniform(10, 40), 1),
                traffic_method=_choice(["直播", "短视频", "图文", "直播+短视频"]),
                cooperation_start=coop_start, cooperation_end=coop_end,
                compliance_status=_choice(["合规", "合规", "合规", "待审核"]),
                gmv=round(_uniform(5000, 500000), 2), roi=round(_uniform(1.5, 8.0), 2),
                conversion_rate=round(_uniform(0.5, 5.0), 2), return_rate=round(_uniform(1, 15), 2),
                payment_status=_choice(["已结算", "已结算", "待结算"]),
                re_broadcast_willingness=_choice(["愿意", "愿意", "待确认"]),
                re_broadcast_date=(datetime.now() + timedelta(days=_randint(3, 30))).strftime("%Y-%m-%d"),
                remarks=_choice(["合作稳定", "首次合作效果良好", "需优化选品", "佣金谈判中"]),
            ))

        # ── 培训文档 (10篇) ──
        docs_data = [
            ("BD自查手册-品牌核心信息", "bd", 1, "## 品牌定位\n赵宜主专注国人体质的高性价比每日营养包。\n\n## 品牌实力\n- 合作品牌达人超过5000+\n- 月均GMV突破2000万\n- 供应链全自有，品质可控\n\n## 核心优势\n1. 高性价比：同品质产品价格低30%\n2. 出片率高：产品效果可视化强\n3. 复购率好：月度复购率达65%\n4. 佣金丰厚：行业领先佣金比例"),
            ("BD自查手册-产品体系", "bd", 2, "## 核心产品线\n1. 每日营养包（明星产品）\n2. 儿童成长营养包\n3. 中老年骨关节营养包\n4. 女性美容营养包\n\n## 适配达人\n| 达人类型 | 推荐产品 | 佣金区间 |\n|---------|---------|--------|\n| 美妆博主 | 女性美容包 | 25-35% |\n| 母婴博主 | 儿童成长包 | 20-30% |"),
            ("BD自查手册-合作政策", "bd", 3, "## 佣金规则\n- 开票：佣金20%-30%\n- 不开票：佣金25%-35%\n- 独家合作额外+5%\n\n## 达人福利\n- 首次合作赠送产品体验装\n- 月度GMV达标奖励\n- 专属素材包支持"),
            ("SOP-达人筛选标准", "sop", 4, "## 获客渠道\n1. 平台搜索：抖音/快手/小红书关键词搜索\n2. 竞品关注：观察竞品合作达人\n3. 行业社群：加入达人BD交流群\n\n## 判定标准\n- 粉丝量：1万以上\n- 互动率：≥3%\n- 原创内容占比≥80%"),
            ("SOP-首次触达开发", "sop", 5, "## 事前准备\n1. 了解达人内容风格和粉丝画像\n2. 准备品牌资料包\n3. 确定沟通话术模板\n\n## 跟进时效\n- 首次沟通后24h内发送详细方案\n- 方案发送后48h内确认意向\n- 确认意向后3个工作日内签约"),
            ("产品知识-核心卖点", "product", 6, "## 每日营养包卖点\n- 37种营养素一包搞定\n- 口感好，比冲剂好喝10倍\n- 独立包装，随身携带\n\n## 儿童成长包卖点\n- DHA+钙+锌，三效合一\n- 无糖配方，不伤牙\n- 水果味，孩子爱喝"),
            ("常见问题FAQ", "other", 7, "## Q1: 佣金什么时候结算？\nA: 每月15号结算上月佣金，T+15到账。\n\n## Q2: 样品怎么申请？\nA: 首次合作可申请1份体验装，3个工作日内发货。\n\n## Q3: 可以独家合作吗？\nA: 可以，独家合作佣金额外+5%，需签约3个月以上。"),
            ("销售规范-沟通话术", "销售规范", 8, "## 开场话术\n\"您好，我是赵宜主BD经理XX，关注您的内容很久了...\"\n\n## 异议处理\n- \"价格太贵\" → \"89元/月，每天不到3元\"\n- \"没听过这个品牌\" → \"我们是新锐品牌，佣金力度很大\"\n\n## 促单话术\n\"本月签约额外送价值299元体验装...\""),
            ("客服规范-常见售后问题", "客服规范", 9, "## 物流问题\n- 发货时效：下单后48小时内\n- 快递公司：默认中通/圆通\n\n## 退换货流程\n1. 客户提交退换申请\n2. 客服审核（1个工作日）\n3. 审核通过后发送退货地址\n4. 收到退货后3个工作日内处理"),
            ("公司制度-考勤与绩效", "公司制度", 10, "## 考勤制度\n- 工作时间：9:00-18:00\n- 打卡方式：企业微信打卡\n\n## 绩效考核\n1. 达人开发数量（权重30%）\n2. 合作签约数量（权重25%）\n3. GMV贡献（权重25%）\n4. 日报周报提交率（权重10%）\n5. 培训学习完成度（权重10%）"),
        ]
        for title, category, chapter, content in docs_data:
            uid = _choice(user_ids)
            info = user_map[uid]
            db.add(TrainingDoc(
                id=f"doc_{uuid.uuid4().hex[:12]}", title=title, content=content,
                category=category, source_type="knowledge", author=info["name"],
                author_id=uid, chapter_number=chapter, views=_randint(10, 500),
            ))

        # ── 刷题库 (20题) ──
        questions_data = [
            ("赵宜主每日营养包包含多少种营养素？", ["21种", "28种", "37种", "45种"], "C", "科学配比37种营养素。", "销售规范", "easy"),
            ("赵宜主每日营养包月费是多少？", ["59元", "89元", "129元", "159元"], "B", "每月只需89元，每天不到3元。", "销售规范", "easy"),
            ("达人首次触达后方案发送时效？", ["12小时内", "24小时内", "48小时内", "72小时内"], "B", "首次沟通后24h内发送详细方案。", "销售规范", "medium"),
            ("独家合作佣金额外增加多少？", ["3%", "5%", "8%", "10%"], "B", "独家合作额外+5%佣金。", "销售规范", "medium"),
            ("不开票佣金比例区间是？", ["15%-25%", "20%-30%", "25%-35%", "30%-40%"], "C", "不开票佣金25%-35%。", "销售规范", "medium"),
            ("达人筛选时粉丝量最低要求？", ["3000", "5000", "10000", "20000"], "C", "粉丝量1万以上，KOC可放宽至5000。", "技术文档", "medium"),
            ("达人互动率合格线？", ["≥1%", "≥2%", "≥3%", "≥5%"], "C", "互动率≥3%为合格。", "技术文档", "medium"),
            ("确认合作意向后签约时效？", ["1个工作日", "3个工作日", "5个工作日", "7个工作日"], "B", "确认意向后3个工作日内签约。", "技术文档", "medium"),
            ("客户下单后多久发货？", ["24小时内", "48小时内", "72小时内", "5天内"], "B", "下单后48小时内发货。", "客服规范", "easy"),
            ("退货审核处理时限？", ["1个工作日", "3个工作日", "5个工作日", "7个工作日"], "A", "1个工作日内审核完毕。", "客服规范", "easy"),
            ("产品保质期多久？", ["6个月", "12个月", "18个月", "24个月"], "C", "保质期18个月。", "客服规范", "easy"),
            ("7天无理由退换的条件？", ["未开封", "不影响二次销售", "任意条件", "仅限质量问题"], "B", "要求不影响二次销售。", "客服规范", "medium"),
            ("达人开发数量权重占比？", ["20%", "25%", "30%", "35%"], "C", "权重30%，最大权重指标。", "公司制度", "medium"),
            ("S级绩效评级总分要求？", ["90分", "93分", "95分", "98分"], "C", "S级要求总分≥95分。", "公司制度", "medium"),
            ("每日任务配额标准是多少条？", ["30条", "40条", "50条", "60条"], "D", "每日任务配额标准为60条。", "公司制度", "hard"),
            ("儿童成长营养包的核心卖点？", ["高钙配方", "DHA+钙+锌三效合一", "有机原料", "进口品质"], "B", "DHA+钙+锌，三效合一。", "产品知识", "easy"),
            ("赵宜主相比竞品A每月便宜多少？", ["20元", "40元", "60元", "80元"], "B", "赵宜主89元，竞品A 129元，便宜40元。", "产品知识", "medium"),
            ("赵宜主每日营养包口感评分？", ["3.9", "4.2", "4.5", "4.8"], "D", "口感评分4.8分。", "产品知识", "medium"),
            ("佣金结算日是每月几号？", ["1号", "10号", "15号", "20号"], "C", "每月15号结算。", "公司制度", "hard"),
            ("首次合作可以申请几份体验装？", ["1份", "2份", "3份", "5份"], "A", "首次合作可申请1份体验装。", "销售规范", "easy"),
        ]
        for q_text, options, answer, explanation, category, difficulty in questions_data:
            db.add(QuizQuestion(
                id=f"quiz_{uuid.uuid4().hex[:12]}", question=q_text,
                options=options, answer=answer, explanation=explanation,
                category=category, difficulty=difficulty,
            ))

        # ── 答题记录 ──
        db.flush()
        quiz_list = db.query(QuizQuestion).all()
        for uid in user_ids[:6]:
            for _ in range(_randint(5, 15)):
                q = _choice(quiz_list)
                is_correct = rand_float() < 0.7
                user_answer = q.answer if is_correct else _choice([o for o in ["A", "B", "C", "D"] if o != q.answer])
                db.add(QuizRecord(
                    id=str(uuid.uuid4()), user_id=uid, question_id=q.id,
                    user_answer=user_answer, is_correct=1 if is_correct else 0,
                    category=q.category,
                ))

        # ── 难题库 (8条) ──
        problems_data = [
            ("达人佣金谈判陷入僵局", "达人坚持35%佣金，公司最高只能给30%。", "1. 分析达人数据评估ROI\n2. 提出保底+佣金方案\n3. 增加非金钱福利", "客户谈判", "approved"),
            ("达人直播效果低于预期", "首播GMV仅完成目标30%。", "1. 分析直播回放\n2. 优化选品策略\n3. 提前沟通话术要点", "直播运营", "approved"),
            ("新人BD转化率过低", "入职3个月新人签约转化率仅5%。", "1. 安排师傅一对一辅导\n2. 增加模拟训练\n3. 调整KPI目标", "团队管理", "pending"),
            ("达人样品物流丢失", "价值2000元样品物流中丢失。", "1. 联系物流理赔\n2. 补发样品\n3. 向达人致歉", "物流售后", "approved"),
            ("竞争对手挖角合作达人", "竞品以更高佣金挖走3个长期合作达人。", "1. 分析达人流失原因\n2. 制定留存计划\n3. 加强关系维护", "竞争策略", "pending"),
            ("达人内容违规下架", "合作短视频因违规被下架。", "1. 分析违规原因\n2. 指导达人修改\n3. 加强发布前审核", "合规风控", "approved"),
            ("月底GMV冲刺压力", "距月底5天，GMV完成率75%。", "1. 盘点可调用达人\n2. 安排加场直播\n3. 推出限时促销", "业绩管理", "pending"),
            ("多平台数据汇总困难", "三个平台数据格式不统一。", "1. 制定统一数据模板\n2. 使用数据采集工具\n3. 建立自动化汇总", "工作流程", "approved"),
        ]
        for title, desc, solution, category, status in problems_data:
            uid = _choice(user_ids)
            db.add(TrainingProblem(
                id=f"problem_{uuid.uuid4().hex[:12]}", title=title,
                description=desc, solution=solution, category=category,
                status=status, review_comment="方案可行" if status == "approved" else "",
                created_by=uid,
            ))

        # ── 工作报告 + 日历任务 ──
        task_actions = [
            "联系达人-确认合作意向", "跟进达人-发送产品样品", "准备产品报价方案",
            "更新达人资源库-新增5条记录", "与客户电话沟通需求", "整理本周合作数据",
            "提交日报-完成今日总结", "制作合作PPT", "审核佣金结算单",
            "对接达人-确认直播时间", "整理BD话术模板", "分析竞品合作策略",
            "更新SOP流程文档", "培训新人-达人开发流程", "处理达人售后问题",
            "跟进达人-协商佣金比例", "整理月度复盘", "策划直播排期",
            "与供应链确认发货计划", "筛选新达人-小红书平台",
        ]
        now = datetime.now()
        # 过去3天日报
        for day_offset in range(3):
            date = (now - timedelta(days=day_offset)).strftime("%Y-%m-%d")
            for uid in user_ids:
                if rand_float() < 0.25 and day_offset > 0:
                    continue  # 模拟有人未提交
                info = user_map[uid]
                work_items = []
                for _ in range(_randint(2, 5)):
                    work_items.append({"task": _choice(task_actions), "result": _choice(["已完成", "进行中", "待跟进"]), "progress": _randint(30, 100)})
                db.add(WorkReport(
                    id=f"report_{uuid.uuid4().hex[:12]}", title=f"{date}日报", type="daily",
                    date=date, period=date,
                    summary=f"{info['name']}的{date}工作日报。",
                    achievements=f"1. 完成达人对接{_randint(2,5)}个\n2. 更新资源库{_randint(5,20)}条",
                    problems="1. 部分达人回复较慢\n2. 样品物流有延迟",
                    plans="1. 继续跟进达人\n2. 准备下周排期",
                    work_items=_json.dumps(work_items, ensure_ascii=False),
                    target_amount=str(_randint(5000, 50000)),
                    completed_amount=str(_randint(3000, 45000)),
                    customer_count=str(_randint(10, 50)),
                    new_customer_count=str(_randint(1, 10)),
                    author=info["name"], author_id=uid,
                    department="BD部", company=info["company"],
                    status="submitted",
                    approval_status=_choice(["pending", "approved"]),
                ))
        # 过去1周周报
        for week_offset in range(2):
            ws = (now - timedelta(weeks=week_offset+1, days=now.weekday())).strftime("%Y-%m-%d")
            we = (now - timedelta(weeks=week_offset+1, days=now.weekday()) + timedelta(days=4)).strftime("%Y-%m-%d")
            for uid in user_ids:
                if rand_float() < 0.15:
                    continue
                info = user_map[uid]
                db.add(WorkReport(
                    id=f"report_{uuid.uuid4().hex[:12]}", title=f"周报 {ws}~{we}", type="weekly",
                    date=ws, period=f"{ws}~{we}",
                    summary=f"{info['name']}的周报。",
                    achievements=f"1. 新增达人资源{_randint(10,30)}条\n2. 签约达人{_randint(2,8)}个",
                    problems="1. 部分达人佣金谈判困难",
                    plans="1. 加大达人开发力度",
                    work_items="[]",
                    target_amount=str(_randint(30000, 200000)),
                    completed_amount=str(_randint(20000, 180000)),
                    customer_count=str(_randint(30, 100)),
                    new_customer_count=str(_randint(5, 25)),
                    author=info["name"], author_id=uid,
                    department="BD部", company=info["company"],
                    status="submitted", approval_status="approved",
                ))

        # 日历任务（过去7天+未来7天）
        for day_offset in range(-7, 8):
            date = (now + timedelta(days=day_offset)).strftime("%Y-%m-%d")
            for _ in range(_randint(20, 60)):
                uid = _choice(user_ids)
                info = user_map[uid]
                is_past = day_offset < 0
                db.add(CalendarTask(
                    id=f"task_{uuid.uuid4().hex[:12]}", date_key=date,
                    action=_choice(task_actions), responsible=info["name"],
                    risk=_choice(["无", "无", "无", "达人回复慢", "佣金谈判难"]),
                    status=_choice(["completed"]*3 + ["in_progress", "pending"]) if is_past else "pending",
                    amount=round(_uniform(500, 20000), 2),
                    target_amount=round(_uniform(10000, 100000), 2),
                    completed_amount=round(_uniform(5000, 90000), 2) if is_past else 0,
                    created_by=uid,
                ))

        # 每日目标
        for day_offset in range(-7, 8):
            date = (now + timedelta(days=day_offset)).strftime("%Y-%m-%d")
            db.add(DailyTarget(
                id=str(uuid.uuid4()), date_key=date,
                target_amount=round(_uniform(50000, 200000), 2),
                completed_amount=round(_uniform(30000, 180000), 2),
                created_by="admin-001",
            ))

        # ── 会议 (5条) ──
        meetings_data = [
            ("6月第1周BD团队周会", "1. 回顾上周GMV\n2. 分析达人开发进度\n3. 本周重点任务", "本周哪个达人合作案例最值得借鉴？"),
            ("Q2季度业绩复盘会", "1. Q2 GMV达成率\n2. 各分公司业绩对比\n3. Q3目标制定", "Q3增长的最大机会点在哪里？"),
            ("达人合作政策调整讨论", "1. 当前佣金体系分析\n2. 竞品政策对比\n3. 新政策方案", "新佣金政策对现有达人会有什么影响？"),
            ("新人培训方案评审", "1. 培训课程体系\n2. 实战项目安排\n3. 考核标准", "如何衡量新人培训的效果？"),
            ("618大促方案讨论", "1. 618活动方案\n2. 达人直播排期\n3. 库存备货计划", "618期间如何保证达人直播质量？"),
        ]
        for title, content, question in meetings_data:
            uid = _choice(user_ids)
            meeting = Meeting(id=f"meeting_{uuid.uuid4().hex[:12]}", title=title, content=content, question=question, created_by=uid)
            db.add(meeting)
            db.flush()
            for auid in _choice(user_ids, k=min(_randint(3, 6), len(user_ids))):
                ainfo = user_map.get(auid, {"name": "未知"})
                db.add(MeetingAnswer(
                    id=str(uuid.uuid4()), meeting_id=meeting.id,
                    user_id=auid, user_name=ainfo["name"],
                    answer=_choice([
                        "我认为重点是提升达人筛选效率。",
                        "建议优化佣金阶梯方案。",
                        "需要加强新人培训能力。",
                        "建议建立达人分级管理制度。",
                        "关键是要提升复播率。",
                    ]),
                ))

        db.commit()
        print("[init] 种子数据填充完成")

    except Exception as e:
        db.rollback()
        print(f"[init] 种子数据填充失败: {e}")


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
