import os
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from src.core import NLPExtract
from fastapi import FastAPI
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

@app.get("/health")
async def read_root():
    return {"status": True}

@app.post("/analyze")
async def analyzer(body: Message):
    payload = body.dict()
    return NLPExtract(open_api_key=os.environ.get("OPEN_API_TOKEN")).analyze(sentence=payload["message"])
