from fastapi import FastAPI
from fastapi import Depends
from db.session import db

app = FastAPI(dependencies=[Depends(db)])
