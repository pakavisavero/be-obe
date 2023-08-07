from db.database import Session
from db.middleware import decode_token


def db():
    try:
        db = Session()
        yield db
    finally:
        db.close()


def getEmail(token):
    email = decode_token(token)["email"]
    return email


def getUsername(token):
    username = decode_token(token)["username"]
    return username


def getUserId(token):
    userId = decode_token(token)["user_id"]
    return userId
