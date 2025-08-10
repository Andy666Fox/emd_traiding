from pydantic import BaseModel

class SlopeResponse(BaseModel):
    ticket: str
    slope: float | None
    dslope: float | None
    status: str
    message: str=None 

class SlopeRequest(BaseModel):
    ticket: str 
    