from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import check_database_connection
from app.routes.vocabulary_routes import router as vocabulary_router

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

