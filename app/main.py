import os
import re
from typing import Optional
from fastapi import FastAPI, Request
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
    stream = os.popen(f'cd dbt && dbt {action} --profiles-dir . --select {selection.arguments}')
    output = stream.readlines()
    print(output)
    return output

@app.post("/check-payload")
async def get_body(request: Request):
    response = await request.json()
    print(response)
    return response
