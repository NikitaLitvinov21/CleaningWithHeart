from pydantic import BaseModel


class Scheme(BaseModel):

    class Config:
        from_attributes = False
