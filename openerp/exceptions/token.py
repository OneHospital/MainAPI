from openerp.exceptions.base import BaseHttpException


class InvalidTokenException(BaseHttpException):
    def __init__(self, message: str):
        super().__init__(status_code=401, message=message, detail="Invalid login session, please login again")
