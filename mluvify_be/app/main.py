import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routers.analyze import router as analyze_router
from pathlib import Path

app = FastAPI(
    title="Mluvify",
    docs_url="/",
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

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)