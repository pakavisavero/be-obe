from fastapi import Depends, status, Form, Header
from fastapi.responses import JSONResponse

from routes.route import app

from db.session import db
from db.database import Session
from db.middleware import (
    authLogin,
    decode_token,
    decode_user_access,
    authLogout,
    decode_group,
)

LOGIN = "/login"


@app.post(LOGIN)
async def login(
    email: str = Form(),
    password: str = Form(),
    db: Session = Depends(db),
):
    return JSONResponse(authLogin(db, email, password))


@app.post("/logout")
async def Logout(
    token: str = Header(default=None),
    db: Session = Depends(db),
):
    return JSONResponse(authLogout(token, db))


@app.get("/me")
async def get_me(
    token: str = Header(default=None),
    access: str = Header(default=None),
    groups: str = Header(default=None),
):
    data = decode_token(token, True)
    data_access = decode_user_access(access)
    groups = decode_group(groups)

    return {
        "code": status.HTTP_200_OK,
        "message": "Success",
        "data": data,
        "user_access": data_access,
        "groups": groups,
    }