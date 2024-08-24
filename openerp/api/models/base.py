from bson import ObjectId
from pydantic import BaseModel


class Base(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**self.serealize(kwargs))

    def serealize(self, data: dict) -> dict:
        final = {}
        for key, value in data.items():
            if isinstance(value, ObjectId):
                final[key] = str(value)
            elif isinstance(value, dict):
                final[key] = self.serealize(value)
            elif isinstance(value, list):
                final[key] = [self.serealize(item) for item in value]
            else:
                final[key] = value

        return final
