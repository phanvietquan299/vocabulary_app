from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/exam", tags=["Exam"])

@router.get("/random-words")
def get_random_words():
    try:
        from app.services.exam_service import get_exam_multiple_choices
        random_words = get_exam_multiple_choices()
        return {"random_words": random_words}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/exam-object")
def get_exam_object(word: str):
    try:
        from app.services.exam_service import get_exam_multiple_choices
        exam_object = get_exam_multiple_choices(word)
        return {"exam_object": exam_object}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))