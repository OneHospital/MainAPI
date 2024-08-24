import re

from fastapi import HTTPException
from loguru import logger


class BaseHttpException(HTTPException):
    def __init__(self, status_code: int, message: str, detail: dict | str):
        class_name = self.__class__.__name__
        self.message = f'[{status_code} {self.format_name(class_name)}] -> {message}'
        logger.opt(depth=2).error(self.message)
        super().__init__(status_code=status_code, detail=detail)

    def __str__(self):
        return self.message

    @staticmethod
    def format_name(exception_name: str) -> str:
        # Remove the "Exception" suffix if it exists
        if exception_name.endswith('Exception'):
            exception_name = exception_name[:-len('Exception')]

        # Add a space before each uppercase letter (except the first one)
        snake_case_name = re.sub(r'(?<!^)(?<!_)([A-Z])', r' \1', exception_name)

        return snake_case_name
