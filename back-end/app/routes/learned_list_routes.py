from fastapi import APIRouter, HTTPException

from app.services.learn_service import add_learned_word, check_all_learned, get_learned_words, reset_learned_progress

router = APIRouter(prefix="/learned", tags=["Learned"])

@router.post("/add")
async def add_learned_word_api(session_id: str, word_id: str):
    try: 
        return await add_learned_word(session_id, word_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error while adding learned word.")
    
@router.get("/reset")
async def reset_learned_progress_api(session_id: str):
    return await reset_learned_progress(session_id)

@router.get("/words")
async def get_learned_words_api(session_id: str):
    try:
        return await get_learned_words(session_id)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error while fetching learned words.")

@router.get("/all")
async def get_all_learned_words():
    try:
        return await check_all_learned()
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error while fetching all learned progress.")
