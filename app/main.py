import uvicorn
import os
import re
import base64
import json
from typing import Optional, Callable, List, Dict
from fastapi import FastAPI, Request, Response, Body, Depends, HTTPException
from fastapi.routing import APIRoute
from pydantic import BaseModel
from enum import Enum

class PubsubRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            payload = json.loads(body)
            # print(payload)
            if payload.get('message') and type(payload.get('message')) == dict:
                message = payload.get('message')
                # Please add attribute - [channel: pubsub] to Pub/Sub messages for FastAPI
                if message.get('attributes') and type(message.get('attributes')) == dict and message.get('attributes').get('channel') == 'pubsub':
                    print("Start decoding pub/sub messages...")
                    try:
                        data = message.get('data')
                    except:
                        raise HTTPException(status_code=404, detail="Google Pub/Sub Message data not found.")
                    body = base64.b64decode(data)
                    # print(json.loads(body))
            self._body = body
            print(json.loads(self._body))
        return self._body

class PubsubRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = PubsubRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler

class DBTAction(str, Enum):
    dbt_run = "run"
    dbt_test = "test"
    dbt_seed = "seed"
    dbt_snapshot = "snapshot"
    dbt_ls = "ls"
    dbt_compile = "compile"
    dbt_freshness = "freshness"
    dbt_build = "build"

class DBTSelection(BaseModel):
    arguments: Optional[str] = None


app = FastAPI()
app.router.route_class = PubsubRoute

# @app.get("/")
# def hello_world():
#     return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}

# check payload after processing (will auto handle pub/sub messages)
@app.post("/payload-check")
async def check_payload(request: Request):
    payload = await request.json()
    print(payload)
    return payload

### DBT Methods define below ###
@app.post("/dbt/{action}")
def execute_dbt(action: DBTAction, selection: DBTSelection):
    stream = os.popen(f"cd dbt && dbt {action} --profiles-dir . --select {selection.arguments}")
    output = stream.readlines()
    print(output)
    return output

@app.get("/dbt-run-script")
def run_dbt_script():
    stream = os.popen(f'cd dbt && sh dbt_script.sh')
    output = stream.readlines()
    print(output)
    return output


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)