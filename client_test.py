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


def test_get_tips():
    request = {
        "operation": "get_tips",
        "category": "finance"
    }
    socket.send_json(request)
    response = socket.recv_json()
    print("get_tips response:", response)


def test_rate_tip():
    request = {
        "operation": "rate_tip",
        "tip_id": "1",
        "rating": 4
    }
    socket.send_json(request)
    response = socket.recv_json()
    print("rate_tip response:", response)


def test_invalid_operation():
    request = {
        "operation": "invalid_operation"
    }
    socket.send_json(request)
    response = socket.recv_json()
    print("invalid_operation response:", response)


if __name__ == "__main__":
    test_get_tips()
    test_rate_tip()
    test_invalid_operation()
