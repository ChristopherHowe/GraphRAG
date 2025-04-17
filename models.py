from pydantic import BaseModel

class triplet(BaseModel):
    head: str
    type: str
    tail: str