from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/exam", tags=["Exam"])

@router.get("/exam-object-flashcard")
def get_exam_object_flashcard(word_id: str):
    try:
        from app.services.exam_service import get_exam_flashcard
        exam_object = get_exam_flashcard(word_id)
        return {"exam_object": exam_object}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/exam-object-multiple-choices")
def get_exam_object(word_id: str):
    try:
        from app.services.exam_service import get_exam_multiple_choices
        exam_object = get_exam_multiple_choices(word_id)
        return {"exam_object": exam_object}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/exam-object-sr")
def get_exam_object_sr(session_id: str):
    try:
        from app.services.exam_service import get_exam_sr
        exam_object = get_exam_sr(session_id)
        return {"exam_object": exam_object}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))