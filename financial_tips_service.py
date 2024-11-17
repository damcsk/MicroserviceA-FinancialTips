import zmq
import json

# Setup ZeroMQ REP socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

print("Financial Tips Microservice is running...")

while True:
    # Receive a request from the client (in JSON format)
    request = socket.recv_json()

    print("Received request:", request)

    # Default response
    response = {
        "message": "This is a placeholder response from the microservice"
    }

    # Send the response back to the client
    socket.send_json(response)
    