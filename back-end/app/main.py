from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import check_database_connection
from app.core.websocket import router as websocket_router
from app.routes.vocabulary_routes import router as vocabulary_router
from app.routes.learned_list_routes import router as learned_router
from app.routes.exam_routes import router as exam_router
from app.routes.pages_routes import router as dashboard_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    check_database_connection()


@app.get("/")
async def root():
    return {"message": "Backend is running with PostgreSQL!"}


app.include_router(vocabulary_router)
app.include_router(learned_router)
app.include_router(websocket_router)
app.include_router(exam_router)
app.include_router(dashboard_router)
