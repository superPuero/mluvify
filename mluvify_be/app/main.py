from fastapi import FastAPI

from app.routers.analyze import router as analyze_router


app = FastAPI(
    title="Mluvify",
    docs_url="/",
)


app.include_router(analyze_router)
