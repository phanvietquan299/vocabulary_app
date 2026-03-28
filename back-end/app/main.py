from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import check_database_connection
from app.patterns.factory.factory_provider import FactoryProvider

app = FastAPI()
factory_provider = FactoryProvider()

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

@app.get("/vocabulary/")
async def get_vocabulary_by_topic(topic: str):
    try:
        factory = factory_provider.get_factory(topic)
        vocabulary_list = factory.get_vocabulary_topic()
        return {"vocabulary": [vocab.__dict__ for vocab in vocabulary_list]}
    except ValueError as e:
        return {"error": str(e)}
    pass


