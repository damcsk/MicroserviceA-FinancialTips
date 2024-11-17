import zmq
import json

# Setup ZeroMQ REQ socket (for sending requests)
context = zmq.Context()
socket = context.socket(zmq.REQ)  # REQ socket for sending requests
socket.connect("tcp://localhost:5555")  # Connecting to the microservice

# Create a test request
request_data = {
    "operation": "get_tips",
    "user_id": "12345"
}

# Send the request
socket.send_json(request_data)

# Receive the response
response = socket.recv_json()

# Print the response
print("Received response:", response)