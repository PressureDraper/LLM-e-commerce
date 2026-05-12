from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.infrastructure.database.session import init_db
from app.infrastructure.cache.redis import init_redis, close_redis


@asynccontextmanager
async def lifespan(app: FastAPI):

    await init_db()
    await init_redis()

    yield

    await close_redis()

app = FastAPI(
    title="LLM e-commerce",
    description="Luxury e-commerce with AI stylist, semantic search and RAG",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", tags=["Health"])
async def health():
    return {"status": "ok", "version": app.version}
