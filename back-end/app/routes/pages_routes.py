from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/user")
async def get_user_dashboard(session_id: str):
    try:
        from app.services.pages_service import get_dashboard_by_user
        dashboard_data = await get_dashboard_by_user(session_id)
        return {"dashboard_data": dashboard_data}
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error while fetching user dashboard.")