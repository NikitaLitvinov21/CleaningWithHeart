from pydantic import BaseModel


class Scheme(BaseModel):

    class Config:
        orm_mode = False
