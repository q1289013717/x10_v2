import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Integer, Float, JSON
from app.core.database import Base


class TrainingDoc(Base):
    """培训知识库文档"""
    __tablename__ = "training_docs"

    id = Column(String, primary_key=True, default=lambda: f"doc_{uuid.uuid4().hex[:12]}")
    title = Column(String(500), nullable=False)
    content = Column(Text, default="")
    category = Column(String(100), default="公司制度", index=True)  # 销售规范、技术文档、客服规范等
    source_type = Column(String(20), default="knowledge")  # knowledge(知识库), personal(个人文档)
    author = Column(String(100), default="")
    author_id = Column(String(100), default="")
    chapter_number = Column(Integer, default=0)  # 章节号(BD自查手册26章)
    views = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "source_type": self.source_type,
            "author": self.author,
            "author_id": self.author_id,
            "chapter_number": self.chapter_number,
            "views": self.views,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class QuizQuestion(Base):
    """培训刷题 - 题目"""
    __tablename__ = "quiz_questions"

    id = Column(String, primary_key=True, default=lambda: f"quiz_{uuid.uuid4().hex[:12]}")
    question = Column(Text, nullable=False)
    options = Column(JSON, default=list)  # ["选项A", "选项B", "选项C", "选项D"]
    answer = Column(String(10), default="")  # "A" / "B" / "C" / "D"
    explanation = Column(Text, default="")  # 解析
    category = Column(String(100), default="公司制度")
    difficulty = Column(String(20), default="medium")  # easy, medium, hard
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "question": self.question,
            "options": self.options,
            "answer": self.answer,
            "explanation": self.explanation,
            "category": self.category,
            "difficulty": self.difficulty,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class QuizRecord(Base):
    """培训刷题 - 答题记录"""
    __tablename__ = "quiz_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(100), nullable=False, index=True)
    question_id = Column(String(100), nullable=False)
    user_answer = Column(String(10), default="")
    is_correct = Column(Integer, default=0)  # 0/1
    category = Column(String(100), default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "question_id": self.question_id,
            "user_answer": self.user_answer,
            "is_correct": self.is_correct,
            "category": self.category,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class TrainingProblem(Base):
    """难题库"""
    __tablename__ = "training_problems"

    id = Column(String, primary_key=True, default=lambda: f"problem_{uuid.uuid4().hex[:12]}")
    title = Column(String(500), nullable=False)
    description = Column(Text, default="")
    solution = Column(Text, default="")
    category = Column(String(100), default="技术故障")
    status = Column(String(20), default="pending", index=True)  # pending, approved, rejected
    review_comment = Column(Text, default="")
    created_by = Column(String(100), default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "solution": self.solution,
            "category": self.category,
            "status": self.status,
            "review_comment": self.review_comment,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class TrainingCategory(Base):
    """培训分类配置"""
    __tablename__ = "training_categories"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    type = Column(String(20), nullable=False)  # knowledge, personal, problem, quiz
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "sort_order": self.sort_order,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
