from fastapi import APIRouter, HTTPException

from app.services.image_service import get_vocabulary_image

router = APIRouter(prefix="/images", tags=["Images"])


@router.get("/{word_id}")
def get_vocabulary_image_api(word_id: str, refresh: bool = True):
    try:
        return get_vocabulary_image(word_id, refresh=refresh)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
