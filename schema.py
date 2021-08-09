from pydantic import BaseModel


class JobOut(BaseModel):
    key: str
    info: str