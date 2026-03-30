from fastapi import APIRouter, HTTPException

from app.services.vocabulary_service import get_vocabulary_by_topic as get_vocabulary_by_topic_service

router = APIRouter(prefix="/vocabulary", tags=["Vocabulary"])


@router.get("")
async def get_vocabulary_by_topic(topic: str):
    try:
        return get_vocabulary_by_topic_service(topic)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
