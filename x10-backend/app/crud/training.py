from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.training import TrainingDoc, QuizQuestion, QuizRecord, TrainingProblem, TrainingCategory


# ========== 培训文档 ==========

def get_training_docs(db: Session, category: Optional[str] = None,
                      source_type: Optional[str] = None,
                      skip: int = 0, limit: int = 100) -> List[TrainingDoc]:
    q = db.query(TrainingDoc)
    if category:
        q = q.filter(TrainingDoc.category == category)
    if source_type:
        q = q.filter(TrainingDoc.source_type == source_type)
    return q.order_by(TrainingDoc.chapter_number.asc(), TrainingDoc.created_at.desc()) \
            .offset(skip).limit(limit).all()


def get_training_doc_by_id(db: Session, doc_id: str) -> Optional[TrainingDoc]:
    return db.query(TrainingDoc).filter(TrainingDoc.id == doc_id).first()


def create_training_doc(db: Session, title: str, content: str = "",
                        category: str = "公司制度", source_type: str = "knowledge",
                        chapter_number: int = 0, author: str = "", author_id: str = "") -> TrainingDoc:
    doc = TrainingDoc(
        title=title, content=content, category=category,
        source_type=source_type, chapter_number=chapter_number,
        author=author, author_id=author_id,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def update_training_doc(db: Session, doc_id: str, **kwargs) -> Optional[TrainingDoc]:
    doc = get_training_doc_by_id(db, doc_id)
    if not doc:
        return None
    for key, value in kwargs.items():
        if hasattr(doc, key) and value is not None:
            setattr(doc, key, value)
    db.commit()
    db.refresh(doc)
    return doc


def delete_training_doc(db: Session, doc_id: str) -> bool:
    doc = get_training_doc_by_id(db, doc_id)
    if not doc:
        return False
    db.delete(doc)
    db.commit()
    return True


def increment_doc_views(db: Session, doc_id: str) -> None:
    doc = get_training_doc_by_id(db, doc_id)
    if doc:
        doc.views = (doc.views or 0) + 1
        db.commit()


def get_doc_categories(db: Session, source_type: str = "knowledge") -> List[str]:
    results = db.query(TrainingDoc.category).filter(
        TrainingDoc.source_type == source_type
    ).distinct().all()
    return [r[0] for r in results if r[0]]


# ========== 刷题 ==========

def get_quiz_questions(db: Session, category: Optional[str] = None,
                       difficulty: Optional[str] = None,
                       skip: int = 0, limit: int = 50) -> List[QuizQuestion]:
    q = db.query(QuizQuestion)
    if category:
        q = q.filter(QuizQuestion.category == category)
    if difficulty:
        q = q.filter(QuizQuestion.difficulty == difficulty)
    return q.order_by(QuizQuestion.created_at.desc()).offset(skip).limit(limit).all()


def get_quiz_question_by_id(db: Session, question_id: str) -> Optional[QuizQuestion]:
    return db.query(QuizQuestion).filter(QuizQuestion.id == question_id).first()


def create_quiz_question(db: Session, **kwargs) -> QuizQuestion:
    q = QuizQuestion(**kwargs)
    db.add(q)
    db.commit()
    db.refresh(q)
    return q


def delete_quiz_question(db: Session, question_id: str) -> bool:
    q = get_quiz_question_by_id(db, question_id)
    if not q:
        return False
    db.delete(q)
    db.commit()
    return True


def submit_quiz_answer(db: Session, user_id: str, question_id: str,
                       user_answer: str, category: str = "") -> QuizRecord:
    question = get_quiz_question_by_id(db, question_id)
    is_correct = 1 if question and question.answer == user_answer else 0
    record = QuizRecord(
        user_id=user_id, question_id=question_id,
        user_answer=user_answer, is_correct=is_correct, category=category,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_quiz_records(db: Session, user_id: Optional[str] = None,
                     skip: int = 0, limit: int = 100) -> List[QuizRecord]:
    q = db.query(QuizRecord)
    if user_id:
        q = q.filter(QuizRecord.user_id == user_id)
    return q.order_by(QuizRecord.created_at.desc()).offset(skip).limit(limit).all()


def get_quiz_stats(db: Session, user_id: str) -> dict:
    records = db.query(QuizRecord).filter(QuizRecord.user_id == user_id).all()
    total = len(records)
    correct = sum(1 for r in records if r.is_correct)

    # 计算连胜
    streak = 0
    for r in reversed(records):
        if r.is_correct:
            streak += 1
        else:
            break

    return {
        "total": total,
        "correct": correct,
        "accuracy": round(correct / total * 100, 1) if total > 0 else 0,
        "streak": streak,
    }


def get_quiz_categories(db: Session) -> List[str]:
    results = db.query(QuizQuestion.category).distinct().all()
    return [r[0] for r in results if r[0]]


# ========== 难题库 ==========

def get_problems(db: Session, user_id: Optional[str] = None,
                 category: Optional[str] = None, status: Optional[str] = None,
                 is_admin: bool = False, skip: int = 0, limit: int = 50) -> List[TrainingProblem]:
    q = db.query(TrainingProblem)
    if not is_admin and user_id:
        q = q.filter(TrainingProblem.created_by == user_id)
    if category:
        q = q.filter(TrainingProblem.category == category)
    if status and status != "all":
        q = q.filter(TrainingProblem.status == status)
    return q.order_by(TrainingProblem.created_at.desc()).offset(skip).limit(limit).all()


def get_problem_by_id(db: Session, problem_id: str) -> Optional[TrainingProblem]:
    return db.query(TrainingProblem).filter(TrainingProblem.id == problem_id).first()


def create_problem(db: Session, title: str, description: str = "",
                   solution: str = "", category: str = "技术故障",
                   created_by: str = "") -> TrainingProblem:
    problem = TrainingProblem(
        title=title, description=description, solution=solution,
        category=category, created_by=created_by, status="pending",
    )
    db.add(problem)
    db.commit()
    db.refresh(problem)
    return problem


def update_problem(db: Session, problem_id: str, **kwargs) -> Optional[TrainingProblem]:
    problem = get_problem_by_id(db, problem_id)
    if not problem:
        return None
    for key, value in kwargs.items():
        if hasattr(problem, key) and value is not None:
            setattr(problem, key, value)
    db.commit()
    db.refresh(problem)
    return problem


def approve_problem(db: Session, problem_id: str, status: str,
                    comment: str = "") -> Optional[TrainingProblem]:
    problem = get_problem_by_id(db, problem_id)
    if not problem:
        return None
    problem.status = status
    problem.review_comment = comment
    db.commit()
    db.refresh(problem)
    return problem


def delete_problem(db: Session, problem_id: str) -> bool:
    problem = get_problem_by_id(db, problem_id)
    if not problem:
        return False
    db.delete(problem)
    db.commit()
    return True


def get_problem_categories(db: Session) -> List[str]:
    results = db.query(TrainingProblem.category).distinct().all()
    return [r[0] for r in results if r[0]]


# ========== 分类管理 ==========

def get_categories(db: Session, cat_type: Optional[str] = None) -> List[TrainingCategory]:
    q = db.query(TrainingCategory)
    if cat_type:
        q = q.filter(TrainingCategory.type == cat_type)
    return q.order_by(TrainingCategory.sort_order.asc()).all()


def create_category(db: Session, name: str, cat_type: str, sort_order: int = 0) -> TrainingCategory:
    cat = TrainingCategory(name=name, type=cat_type, sort_order=sort_order)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


def delete_category(db: Session, cat_id: str) -> bool:
    cat = db.query(TrainingCategory).filter(TrainingCategory.id == cat_id).first()
    if not cat:
        return False
    db.delete(cat)
    db.commit()
    return True
