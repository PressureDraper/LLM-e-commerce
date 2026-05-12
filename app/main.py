from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.infrastructure.database.session import init_db
from app.infrastructure.cache.redis import init_redis, close_redis

from app.modules.products.router import router as products_router
from app.modules.orders.router import router as orders_router
from app.modules.cart.router import router as cart_router
from app.modules.auth.router import router as auth_router
from app.modules.ai.router import router as ai_router
from app.modules.search.router import router as search_router


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


# ── Routers registration ─────────────────────────────────────────────────────
app.include_router(auth_router,     prefix="/api/v1/auth",     tags=["Auth"])
app.include_router(products_router, prefix="/api/v1/products", tags=["Products"])
app.include_router(orders_router,   prefix="/api/v1/orders",   tags=["Orders"])
app.include_router(cart_router,     prefix="/api/v1/cart",     tags=["Cart"])
app.include_router(search_router,   prefix="/api/v1/search",   tags=["Search"])
app.include_router(ai_router,       prefix="/api/v1/ai",       tags=["AI"])


@app.get("/", tags=["Health"])
async def health():
    return {"status": "ok", "version": app.version}
