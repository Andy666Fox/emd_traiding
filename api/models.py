from pydantic import BaseModel

# Basic http response model
class SlopeResponse(BaseModel):
    ticket: str
    slope: float | None
    dslope: float | None
    status: str
    message: str = None


# Basic http request model
class SlopeRequest(BaseModel):
    ticket: str
