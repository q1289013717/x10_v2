from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.core.database import get_db
from app.core.deps import get_current_user, get_current_admin_user, is_admin_user
from app.models.user import User
from app.schemas.training import (
    TrainingDocCreate, TrainingDocUpdate, TrainingDocResponse,
    QuizQuestionCreate, QuizQuestionResponse, QuizQuestionClientResponse,
    QuizSubmitRequest, QuizRecordResponse, QuizStats,
    ProblemCreate, ProblemUpdate, ProblemResponse, ProblemApproval,
    CategoryResponse,
)
from app.crud import training as training_crud

router = APIRouter(prefix="/api/training", tags=["培训中心"])


# ========== 知识库文档 ==========

@router.get("/docs", response_model=list[TrainingDocResponse])
def list_docs(
    category: Optional[str] = Query(default=None),
    source_type: Optional[str] = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    docs = training_crud.get_training_docs(
        db, category=category, source_type=source_type, skip=skip, limit=limit,
    )
    return [TrainingDocResponse.model_validate(d.to_dict()) for d in docs]


@router.get("/docs/categories")
def get_doc_categories(source_type: str = Query(default="knowledge"),
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    return training_crud.get_doc_categories(db, source_type)


@router.get("/docs/{doc_id}", response_model=TrainingDocResponse)
def get_doc(doc_id: str, db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)):
    doc = training_crud.get_training_doc_by_id(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="文档不存在")
    training_crud.increment_doc_views(db, doc_id)
    return TrainingDocResponse.model_validate(doc.to_dict())


@router.post("/docs", response_model=TrainingDocResponse)
def create_doc(doc_data: TrainingDocCreate,
               db: Session = Depends(get_db),
               current_user: User = Depends(get_current_admin_user)):
    doc = training_crud.create_training_doc(
        db,
        title=doc_data.title,
        content=doc_data.content,
        category=doc_data.category,
        source_type=doc_data.source_type,
        chapter_number=doc_data.chapter_number,
        author=current_user.name,
        author_id=current_user.id,
    )
    return TrainingDocResponse.model_validate(doc.to_dict())


@router.put("/docs/{doc_id}", response_model=TrainingDocResponse)
def update_doc(doc_id: str, doc_data: TrainingDocUpdate,
               db: Session = Depends(get_db),
               current_user: User = Depends(get_current_admin_user)):
    update_data = doc_data.model_dump(exclude_unset=True)
    doc = training_crud.update_training_doc(db, doc_id, **update_data)
    if not doc:
        raise HTTPException(status_code=404, detail="文档不存在")
    return TrainingDocResponse.model_validate(doc.to_dict())


@router.delete("/docs/{doc_id}")
def delete_doc(doc_id: str, db: Session = Depends(get_db),
               current_user: User = Depends(get_current_admin_user)):
    success = training_crud.delete_training_doc(db, doc_id)
    if not success:
        raise HTTPException(status_code=404, detail="文档不存在")
    return {"message": "删除成功"}


# ========== 刷题系统 ==========

@router.get("/quiz/questions", response_model=list[QuizQuestionClientResponse])
def list_quiz_questions(
    category: Optional[str] = Query(default=None),
    difficulty: Optional[str] = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """普通用户获取题目列表(不含答案)"""
    questions = training_crud.get_quiz_questions(
        db, category=category, difficulty=difficulty, skip=skip, limit=limit,
    )
    return [QuizQuestionClientResponse.model_validate(q.to_dict()) for q in questions]


@router.get("/quiz/questions/admin", response_model=list[QuizQuestionResponse])
def list_quiz_questions_admin(
    category: Optional[str] = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """管理员获取题目列表(含答案)"""
    questions = training_crud.get_quiz_questions(db, category=category, skip=skip, limit=limit)
    return [QuizQuestionResponse.model_validate(q.to_dict()) for q in questions]


@router.get("/quiz/categories")
def get_quiz_categories(db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    return training_crud.get_quiz_categories(db)


@router.post("/quiz/questions", response_model=QuizQuestionResponse)
def create_quiz_question(question_data: QuizQuestionCreate,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_admin_user)):
    q = training_crud.create_quiz_question(db, **question_data.model_dump())
    return QuizQuestionResponse.model_validate(q.to_dict())


@router.delete("/quiz/questions/{question_id}")
def delete_quiz_question(question_id: str,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_admin_user)):
    success = training_crud.delete_quiz_question(db, question_id)
    if not success:
        raise HTTPException(status_code=404, detail="题目不存在")
    return {"message": "删除成功"}


@router.post("/quiz/submit", response_model=QuizRecordResponse)
def submit_quiz(submit: QuizSubmitRequest,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    record = training_crud.submit_quiz_answer(
        db, current_user.id, submit.question_id, submit.answer, submit.category,
    )
    return QuizRecordResponse.model_validate(record.to_dict())


@router.get("/quiz/records")
def get_my_quiz_records(db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    records = training_crud.get_quiz_records(db, user_id=current_user.id)
    return [r.to_dict() for r in records]


@router.get("/quiz/stats", response_model=QuizStats)
def get_my_quiz_stats(db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    stats = training_crud.get_quiz_stats(db, current_user.id)
    return QuizStats(**stats)


# ========== 难题库 ==========

@router.get("/problems", response_model=list[ProblemResponse])
def list_problems(
    category: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    problems = training_crud.get_problems(
        db, user_id=current_user.id, category=category, status=status,
        is_admin=is_admin_user(current_user), skip=skip, limit=limit,
    )
    return [ProblemResponse.model_validate(p.to_dict()) for p in problems]


@router.get("/problems/categories")
def get_problem_categories(db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_user)):
    return training_crud.get_problem_categories(db)


@router.get("/problems/{problem_id}", response_model=ProblemResponse)
def get_problem(problem_id: str, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    problem = training_crud.get_problem_by_id(db, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="问题不存在")
    return ProblemResponse.model_validate(problem.to_dict())


@router.post("/problems", response_model=ProblemResponse)
def create_problem(problem_data: ProblemCreate,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    problem = training_crud.create_problem(
        db,
        title=problem_data.title,
        description=problem_data.description,
        solution=problem_data.solution,
        category=problem_data.category,
        created_by=current_user.id,
    )
    return ProblemResponse.model_validate(problem.to_dict())


@router.put("/problems/{problem_id}", response_model=ProblemResponse)
def update_problem(problem_id: str, problem_data: ProblemUpdate,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    update_data = problem_data.model_dump(exclude_unset=True)
    problem = training_crud.update_problem(db, problem_id, **update_data)
    if not problem:
        raise HTTPException(status_code=404, detail="问题不存在")
    return ProblemResponse.model_validate(problem.to_dict())


@router.put("/problems/{problem_id}/approve", response_model=ProblemResponse)
def approve_problem(problem_id: str, approval: ProblemApproval,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_admin_user)):
    problem = training_crud.approve_problem(db, problem_id, approval.status, approval.comment)
    if not problem:
        raise HTTPException(status_code=404, detail="问题不存在")
    return ProblemResponse.model_validate(problem.to_dict())


@router.delete("/problems/{problem_id}")
def delete_problem(problem_id: str,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_admin_user)):
    success = training_crud.delete_problem(db, problem_id)
    if not success:
        raise HTTPException(status_code=404, detail="问题不存在")
    return {"message": "删除成功"}
