from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from routers import stories

app = FastAPI()
app.include_router(stories.router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.exception_handler(Exception)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"message": str(exc)},
    )