import os
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

class Selection(BaseModel):
    name: Optional[str] = None

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/dbt_script")
def run_dbt_script():
    stream = os.popen(f'cd crypto_data_warehouse && sh dbt_script.sh')
    output = stream.read()
    return output

@app.post("/dbt/run")
def dbt_run(selection: Selection):
    stream = os.popen(f'cd crypto_data_warehouse && dbt run --profiles-dir . --select {selection.name}')
    output = stream.read()
    return output
