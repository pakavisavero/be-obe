from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from routes.route import app


class HandlerCustom(Exception):
    def __init__(self, data: str):
        self.data = data


@app.exception_handler(HandlerCustom)
async def my_exception_handler(request: Request, exc: HandlerCustom):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": exc.data["message"],
        },
    )
