from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import timedelta
from botocore.exceptions import ClientError
from utils import load_audio, prepare_text, force_align, clean_dir


app = FastAPI(
    title="Aeneas Audio Aligmnent",
)


class PayLoad(BaseModel):
    bucket_id: str
    sub_dir: str = None
    file_name: str
    text: str


class Fragment(BaseModel):
    begin: timedelta
    end: timedelta
    children: List = []
    id: str
    language: str = None
    lines: List[str]


class Response(BaseModel):
    file_name: str
    alignment: List[Fragment]


@app.get("/")
def read_root():
    return {"Hello: World!"}


@app.post("/audio/", response_model=Response)
def align_audio(payload: PayLoad):
    try:
        load_audio(payload.bucket_id, payload.sub_dir, payload.file_name)
    except ClientError:
        raise HTTPException(status_code=404, detail="Item not found")
    prepare_text(payload.text)
    sync_map = force_align()
    clean_dir()

    response = Response(alignment=sync_map, file_name=payload.file_name)
    return response
