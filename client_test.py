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

# Test rate_tip operation
rate_tip_request = {
    "operation": "rate_tip",
    "tip_id": "0001",
    "rating": 5,
}
socket.send_json(rate_tip_request)
rate_tip_response = socket.recv_json()
print("Response (rate tip):", rate_tip_response)