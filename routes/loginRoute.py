# from fastapi import Depends, status, Form

# from routes.route import app
# from db.session import db
# from db.database import Session

# LOGIN = "/login"


# @app.post(LOGIN)
# # @check_access_module
# async def login(
#     username: str = Form(),
#     password: str = Form(),
#     db: Session = Depends(db),
# ):
#     data = ""
#     if data:
#         return {
#             "code": status.HTTP_200_OK,
#             "message": "Login success!",
#             "data": data,
#         }

#     else:
#         return {
#             "code": status.HTTP_400_BAD_REQUEST,
#             "message": "Login error. Something bad has occured!",
#         }
