from typing import Optional

from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
import json
import httpx
from uvicorn.config import LOGGING_CONFIG
import random


NODE_LIST = ["node1", "node2", "node3"]

class Operation(BaseModel):
    op: str
    value: int


app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Node 1 is our init leader
    url = f"http://node1:8080" + "/set-leader"
    result = await send_request(host=url, type="GET")

@app.get("/clear")
async def clear():
    for node in NODE_LIST:
        url = f"http://{node}:8080" + "/clear"
        result = await send_request(host=url, type="GET")
    return result

@app.get("/read")
async def read():
    node = random.choice(NODE_LIST)
    url = f"http://{node}:8080" + "/read"
    result = await send_request(host=url,
        type="GET")
    return result

@app.get("/read-all")
async def read_all():
    responses = []
    for node in NODE_LIST:
        url = f"http://{node}:8080" + "/read"
        result = await send_request(host=url,
            type="GET")
        responses.append(result)
    return responses

@app.post("/write")
async def write(operation: Operation):
    for node in NODE_LIST:
        url = f"http://{node}:8080" + "/write"
        result = await send_request(host=url,
        type="POST",
        data={"op": operation.op,"value": operation.value, "requester": "client"})     
    return result

async def send_request(host: str, type: str, data=None):
    timeout = httpx.Timeout(60.0, connect=60.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        if type == "POST":
            response = await client.post(host, data=json.dumps(data))
            return json.loads(response.text)
        elif type == "GET":
            response = await client.get(host)
            return json.loads(response.text)
    


if __name__ == "__main__":
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = '%(asctime)s [%(name)s] %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=False, root_path="/")
