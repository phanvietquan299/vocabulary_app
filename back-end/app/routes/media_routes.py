from fastapi import APIRouter, HTTPException

from app.services.media_service import generate_vocabulary_media

router = APIRouter(prefix="/media", tags=["Media"])


@router.post("/vocabulary/{word_id}")
async def generate_vocabulary_media_api(word_id: str, session_id: str | None = None):
    try:
        return generate_vocabulary_media(word_id, session_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
