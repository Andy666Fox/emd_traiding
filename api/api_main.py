from fastapi import FastAPI

from sloper import get_data_slope
from models import SlopeResponse

import os


app = FastAPI(title="EMD trading API", 
              description="EMD trading API", 
              version="1.0.0",
              root_path=os.getenv("ROOT_PATH", ""))


@app.get("/")
def root():
    return {"message": app.description, "version": app.version}


@app.get("/get_slope_of/{ticket}", response_model=SlopeResponse)
def get_slope(ticket: str):
    try:
        result = get_data_slope(ticket)
        return {
            "ticket": ticket,
            "slope": result[0],
            "dslope": result[1],
            "status": "200",
        }
    except Exception as e:
        return {
            "ticket": str(ticket),
            "slope": None,
            "dslope": None,
            "status": "400",
            "message": "Invalid ticket name",
        }
    
@app.get('/health')
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host=host, port=port, log_level="info")
