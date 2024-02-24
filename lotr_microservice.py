import zmq
import random


def generate_numbers():
    num1 = random.randint(1, 933)
    num2 = random.randint(1, 2384)
    return {"num1": num1, "num2": num2}


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:8888")

    while True:
        try:
            message = socket.recv_string()
            if message == "generate_numbers":
                numbers = generate_numbers()
                socket.send_json(numbers)
            else:
                socket.send_string("Invalid request")
        except Exception as e:
            # Print error message directly to the console
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
