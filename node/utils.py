import random 
from time import sleep
import httpx
import json


def delay_machine():
    # Model the delay over the network
    delay = random.choice([0, 1, 2, 4 , 8, 16])
    sleep(delay)

# Atomic operation Read last line, get result. Append op with result
def perform_operation(operation: str, value: int):
    # Use a+ to create file if it doesn't exist
    with open("data/log.txt", 'a+') as log:
        # Set the position in the beginning of the file
        log.seek(0)

        _, _, result = _search_for_last_operation(log)
        
        if operation == "ADD":
            result = result + value
        elif operation == "SUB":
            result = result - value
        elif operation == "MUL":
            result = result * value
            
        _append_new_operation(log, operation, value, result)
        return {"result": result}

def _search_for_last_operation(file):
    last_line = None
    for line in file:
        last_line = line
    if last_line:
        op, value, result = last_line.split(',')
        return op, int(value), int(result)
    return "INIT", 0, 0

def _append_new_operation(file, op: str, value: int, result: int):
    file.write(f"\n{op},{value},{result}")

async def send_request(host: str, type: str, data=None):
    timeout = httpx.Timeout(60.0, connect=60.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        if type == "POST":
            response = await client.post(host, data=json.dumps(data))
        elif type == "GET":
            response = await client.get(host)
