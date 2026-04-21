from fastapi import APIRouter, HTTPException, UploadFile, File

router = APIRouter(prefix="/file", tags=["File"])

@router.post("/import-csv")
async def import_csv_file(file: UploadFile = File(...)):
    try:
        from app.services.file_service import import_csv_file_vocabulary
        from app.core.websocket import push_dashboard_refresh_to_all_sessions
        import_csv_file_vocabulary(file)
        await push_dashboard_refresh_to_all_sessions()
        return {"message": "CSV file imported successfully"}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/import-json")
async def import_json_file(file: UploadFile = File(...)):
    try:
        from app.services.file_service import import_json_file_vocabulary
        from app.core.websocket import push_dashboard_refresh_to_all_sessions
        import_json_file_vocabulary(file)
        await push_dashboard_refresh_to_all_sessions()
        return {"message": "JSON file imported successfully"}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
