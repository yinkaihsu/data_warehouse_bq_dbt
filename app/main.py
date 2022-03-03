import uvicorn
import os
import re
import base64
import json
from imp import reload
from typing import Optional, Dict
from fastapi import FastAPI, Request, Depends, HTTPException
from pydantic import BaseModel
from enum import Enum

class DBTAction(str, Enum):
    dbt_run = "run"
    dbt_test = "test"
    dbt_seed = "seed"
    dbt_snapshot = "snapshot"
    dbt_ls = "ls"
    dbt_compile = "compile"
    dbt_freshness = "freshness"
    dbt_build = "build"

class Selection(BaseModel):
    arguments: Optional[str] = None

async def handle_pubsub_message(request: Request):
    payload = await request.json()
    print(payload)
    if payload.get('message') and type(payload.get('message')) == dict:
        message = payload.get('message')
        # Please add attribute - [channel: pubsub] to Pub/Sub messages for FastAPI
        if message.get('attributes') and type(message.get('attributes')) == dict and message.get('attributes').get('channel') == 'pubsub':
            print("Start decoding pub/sub messages...")
            try:
                data = message.get('data')
            except:
                raise HTTPException(status_code=404, detail="Google Pub/Sub Message data not found.")
            converted_payload = json.loads(base64.b64decode(data))
            return converted_payload
    return payload


app = FastAPI()

@app.get("/")
def hello_world():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/dbt-script")
def run_dbt_script():
    stream = os.popen(f'cd dbt && sh dbt_script.sh')
    output = stream.readlines()
    print(output)
    return output

@app.post("/dbt/{action}")
def execute_dbt(action: DBTAction, selection: Selection):
    stream = os.popen(f"cd dbt && dbt {action} --profiles-dir . --select {selection.arguments}")
    output = stream.readlines()
    print(output)
    return output

@app.post("/convert-pubsub-payload")
async def get_body(request: Dict = Depends(handle_pubsub_message)):
    print(request)
    return request

@app.post("/pubsub/dbt/{action}")
def execute_dbt(action: DBTAction, selection: Dict = Depends(handle_pubsub_message)):
    stream = os.popen(f"cd dbt && dbt {action} --profiles-dir . --select {selection.get('arguments')}")
    output = stream.readlines()
    print(output)
    return output


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)