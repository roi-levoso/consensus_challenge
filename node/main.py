from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os
import json
import random
from time import sleep
import httpx
import asyncio

NODE_LIST = [n for n in ["node1", "node2", "node3"] if n != os.getenv("NODE")]
leader = False
class Operation(BaseModel):
    op: str
    value: int
    requester: str


app = FastAPI()

@app.get("/clear")
async def clear():
    with open("data/log.txt", 'w+') as log:
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
    result = perform_operation(operation)
    #If the node is the leader send requests to the rest
    if leader:
        data = {"op": operation.op,
        "value": operation.value,
        "requester": "leader"}
        for node in NODE_LIST:
            url = f"http://{node}:8080" + "/write"
            await send_request(host=url, type="POST", data=data)
    return {"result": result}

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

# Atomic operation. Read last line, get result. Append op with result
def perform_operation(operation: Operation):
    # Use a+ to create file if it doesn't exist
    with open("data/log.txt", 'a+') as log:
        # Set the position in the beginning of the file
        log.seek(0)

        _, _, result = search_for_last_operation(log)
        
        if operation.op == "ADD":
            result = result + operation.value
        elif operation.op == "SUB":
            result = result - operation.value
        elif operation.op == "MUL":
            result = result * operation.value
            
        append_new_operation(log, operation.op, operation.value, result)
        return {"result": result}

async def send_request(host: str, type: str, data=None):
    timeout = httpx.Timeout(60.0, connect=60.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        if type == "POST":
            response = await client.post(host, data=json.dumps(data))
        elif type == "GET":
            response = await client.get(host)

def delay_machine():
    delay = random.choice([0, 1, 2, 4 , 8, 16])
    sleep(delay)

def search_for_last_operation(file):
    last_line = None
    for line in file:
        last_line = line
    if last_line:
        op, value, result = last_line.split(',')
        return op, int(value), int(result)
    return "INIT", 0, 0

def append_new_operation(file, op: str, value: int, result: int):
    file.write(f"\n{op},{value},{result}")

if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=False, root_path="/")