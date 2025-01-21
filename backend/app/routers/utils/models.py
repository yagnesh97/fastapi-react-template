from pydantic import BaseModel


class APIStatus(BaseModel):
    status: str
