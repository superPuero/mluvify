import uvicorn
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app.routers.analyze import router as analyze_router
from app.core.ollama import ollama_service


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await ollama_service.startup()

    yield

    await ollama_service.shutdown()


app = FastAPI(
    title="Mluvify",
    docs_url="/docs",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI()

ROOT_DIR = Path(__file__).parent.parent.parent
FRONTEND_BUILD_DIR = ROOT_DIR / "mluvify_fe" / "build"

app.mount("/", StaticFiles(directory=str(FRONTEND_BUILD_DIR), html=True), name="frontend")
app.include_router(analyze_router)