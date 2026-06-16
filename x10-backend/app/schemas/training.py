from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ========== 培训文档 ==========
class TrainingDocBase(BaseModel):
    title: str
    content: str = ""
    category: str = "公司制度"
    source_type: str = "knowledge"
    chapter_number: int = 0


class TrainingDocCreate(TrainingDocBase):
    pass


class TrainingDocUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    chapter_number: Optional[int] = None


class TrainingDocResponse(BaseModel):
    id: str
    title: str
    content: str
    category: str
    source_type: str
    author: str
    author_id: str
    chapter_number: int
    views: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


# ========== 刷题题目 ==========
class QuizQuestionCreate(BaseModel):
    question: str
    options: List[str] = []
    answer: str = ""
    explanation: str = ""
    category: str = "公司制度"
    difficulty: str = "medium"


class QuizQuestionResponse(BaseModel):
    id: str
    question: str
    options: List[str]
    answer: str  # 管理员可见
    explanation: str
    category: str
    difficulty: str
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class QuizQuestionClientResponse(BaseModel):
    """返回给普通用户 - 不包含答案"""
    id: str
    question: str
    options: List[str]
    category: str
    difficulty: str

    class Config:
        from_attributes = True


class QuizSubmitRequest(BaseModel):
    question_id: str
    answer: str
    category: str = ""


class QuizRecordResponse(BaseModel):
    id: str
    user_id: str
    question_id: str
    user_answer: str
    is_correct: bool
    category: str
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class QuizStats(BaseModel):
    total: int
    correct: int
    accuracy: float
    streak: int = 0


# ========== 难题库 ==========
class ProblemCreate(BaseModel):
    title: str
    description: str = ""
    solution: str = ""
    category: str = "技术故障"


class ProblemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    solution: Optional[str] = None
    category: Optional[str] = None


class ProblemResponse(BaseModel):
    id: str
    title: str
    description: str
    solution: str
    category: str
    status: str
    review_comment: str
    created_by: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class ProblemApproval(BaseModel):
    status: str = Field(..., description="approved/rejected")
    comment: str = ""


# ========== 分类 ==========
class CategoryResponse(BaseModel):
    id: str
    name: str
    type: str
    sort_order: int

    class Config:
        from_attributes = True
