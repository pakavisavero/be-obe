#!/usr/bin/env python3.7

from db.middleware import ValidatePermission
from routes.route import app
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

origins = [
    "http://localhost:3000",
]   

app.add_middleware(ValidatePermission)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
