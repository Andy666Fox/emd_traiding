from fastapi import FastAPI, HTTPException
import sys 
import os 

from core.sloper import get_data_slope
from api.models import SlopeResponse


app = FastAPI(
    title="EMD trading API",
    description="EMD trading API",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": app.description, "version": app.version}

@app.get("/get_slope_of/{ticket}", response_model=SlopeResponse)
async def get_slope(ticket: str):
    try:
        result = get_data_slope(ticket)
        return SlopeResponse(
            ticket=ticket, 
            slope=result[0], 
            dslope=result[1],
            status='200')
    except Exception as e:
        return SlopeResponse(
            ticket=str(ticket), 
            slope=None,dslope=None, 
            status='400',
            message='Invalid ticket name')
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)