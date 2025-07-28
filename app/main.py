from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, slack
from app.core.config import config
from app.utils.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup")
    yield
    logger.info("Application shutdown")

app = FastAPI(
    title=config.PROJECT_NAME,
    version=config.PROJECT_VERSION,
    description=config.PROJECT_DESCRIPTION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api")
app.include_router(slack.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to AutoAgent QA API"}
