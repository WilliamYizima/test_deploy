import os
import traceback
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from src.auth.auth_bearer import JWTBearer
from src.auth.auth_handler import signJWT
from src.core import NLPExtract
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

description="""This api is a project to analyze Sentences and extract Entities with Spacy and ChatGPT"""
origins = ["*"]

app = FastAPI(
    title="Analyzer",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Dev.Will",
        "url": "https://github.com/WilliamYizima",
        "email": "william.yizima@hotmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },)

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

class Message(BaseModel):
    message: str

async def check_user(user, password):
    """_summary_

    Args:
        user (_type_): _description_
        password (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        if user == "test_user" and password==os.environ.get("PASSWORD"):
            return True

        return False
    except Exception as error:
        return False

@app.get("/health")
async def read_root():
    return {"status": True}

@app.post("/analyze", dependencies=[Depends(JWTBearer())])
async def analyzer(body: Message):
    payload = body.dict()
    t = NLPExtract(open_api_key=os.environ.get("OPEN_API_TOKEN")).analyze(sentence=payload["message"])
    return t

@app.post(
    "/login"
)
async def login(request: Request):
    try:
        request_body = await request.json()
        validate_user = await check_user(request_body["username"], request_body["password"])
        if validate_user:
            token = signJWT(request_body["username"])
            return JSONResponse(
                status_code=200,
                content={
                    "access_token": token["access_token"],
                    "token_type": "Bearer",
                    "refresh": token["refresh"],
                },
            )
        return JSONResponse(
            status_code=401,
            content={"error": "Invalid Credentials", "error_code": "401"},
        )

    except Exception as error:
        return JSONResponse(
            status_code=503, content={"error_message": f"{error} - {traceback.format_exc()}", "error_code": "503"}
        )
