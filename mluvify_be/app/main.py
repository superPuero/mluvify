from fastapi import FastAPI


app = FastAPI(
    title="Mluvify",
    docs_url="/",
)


@app.get("/hello")
async def hello():
    return {"hello": "world"}
