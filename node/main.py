from typing import Optional

from fastapi import FastAPI,  HTTPException
from pydantic import BaseModel
import uvicorn
import os
import asyncio
import json

from utils import delay_machine, perform_operation, send_request

NODE_LIST = [n for n in ["node1", "node2", "node3"] if n != os.getenv("NODE")]
FILEPATH = "data/log.txt"
leader = False
class Operation(BaseModel):
    op: str
    value: int
    requester: str


app = FastAPI()

@app.get("/clear")
async def clear():
    with open(FILEPATH, 'w+') as log:
        pass
    return {"result": "clear"}

@app.post("/write")
async def write(operation: Operation):
    # When the request comes from the orchestrator and the node is not leader don't do nothing
    if not leader and operation.requester != "leader":
        return {}
    # When the request comes from the leader and the node is the leader then simulate a delay
    if not leader and operation.requester == "leader":
        delay_machine()    
    result = perform_operation(operation.op, operation.value)
    #If the node is the leader send requests to the rest
    if leader:
        data = {"op": operation.op,
        "value": operation.value,
        "requester": "leader"}
        for node in NODE_LIST:
            url = f"http://{node}:8080" + "/write"
            await send_request(host=url, type="POST", data=data)
    return {"result": result}

@app.get("/read")
async def read():
    try:
        with open(FILEPATH, "r") as file:
            last_line = file.readlines()[-1]
        return {"result": last_line}
    except IOError:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/set-leader")
async def set_leader():
    global leader
    async with asyncio.Lock():
        leader = True
    return {"result": "leader set"}

@app.get("/get-leader")
async def get_leader():
    global leader
    async with asyncio.Lock():
        return {"result" :leader}


if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=False, root_path="/")