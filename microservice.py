import zmq
import random

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:8888")

while True:
    message = socket.recv_string()
    if message == "easy":
        num1 = random.randint(0, 9)
        num2 = random.randint(0, 9)
        socket.send_json({"num1": num1, "num2": num2})
    elif message == "medium":
        num1 = random.randint(10, 99)
        num2 = random.randint(10, 99)
        socket.send_json({"num1": num1, "num2": num2})
    elif message == "hard":
        num1 = random.randint(100, 999)
        num2 = random.randint(100, 999)
        socket.send_json({"num1": num1, "num2": num2})
    else:
        socket.send_string("Invalid request")
