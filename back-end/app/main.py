from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.database import check_database_connection, ensure_topic_image_configs_table, ensure_vocabulary_media_columns
from app.core.media import ensure_media_directories, MEDIA_ROOT, STATIC_ROOT
from app.core.websocket import router as websocket_router
from app.routes.image_routes import router as image_router
from app.routes.vocabulary_routes import router as vocabulary_router
from app.routes.learned_list_routes import router as learned_router
from app.routes.exam_routes import router as exam_router
from app.routes.pages_routes import router as dashboard_router

app = FastAPI()

ensure_media_directories()
app.mount("/static", StaticFiles(directory=str(STATIC_ROOT)), name="static")
app.mount("/media", StaticFiles(directory=str(MEDIA_ROOT)), name="media")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    check_database_connection()
    ensure_vocabulary_media_columns()
    ensure_topic_image_configs_table()


@app.get("/")
async def root():
    return {"message": "Backend is running with PostgreSQL!"}


app.include_router(vocabulary_router)
app.include_router(learned_router)
app.include_router(websocket_router)
app.include_router(exam_router)
app.include_router(dashboard_router)
app.include_router(image_router)
