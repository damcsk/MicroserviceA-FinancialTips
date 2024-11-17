import zmq

# Setup ZeroMQ REQ socket
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# Test 1: Request all tips
request_data = {"operation": "get_tips"}
socket.send_json(request_data)
response = socket.recv_json()
print("Response (all tips):", response)

# Test 2: Request tips filtered by category
request_data = {"operation": "get_tips", "category": "Budgeting"}
socket.send_json(request_data)
response = socket.recv_json()
print("Response (filtered by Budgeting):", response)
