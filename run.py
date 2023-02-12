import uvicorn
from src import fastapi_app


if __name__ == '__main__':
    uvicorn.run(fastapi_app, port=9001, host="0.0.0.0")
