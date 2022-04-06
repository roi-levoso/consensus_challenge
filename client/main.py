import requests
import json
import random

def read():
    pass

def write(operation: str, value: int):
    data = {"op": operation,"value": value}
    r = send_request(path="write", type="POST", data=data)

def send_request(path:str, type: str, data=None):
    host = "http://127.0.0.1:80/" + path
    if type == "POST":
        response = requests.post(host, data=json.dumps(data))
        return response
    elif type == "GET":
        response = requests.get(host)
        return response

if __name__ == "__main__":
    for _ in range(1,10):
        operation = random.choice(["MUL", "ADD", "SUB"])
        value = random.randint(1,10)
        write(operation=operation, value=value)
