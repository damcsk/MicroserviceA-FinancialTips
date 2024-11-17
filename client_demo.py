import zmq
import json

# Setup ZeroMQ REQ socket
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")


def test_get_tips_no_category():
    """Fetching tips"""
    print("Requesting tips with no category filtering:")
    request = {"operation": "get_tips"}
    print("Request: ", json.dumps(request, indent=4))

    socket.send_json(request)
    response = socket.recv_json()
    print("Response (no category tips):", json.dumps(response, indent=4), "\n\n")


def test_get_tips_filtered_by_category():
    """Fetching tips by Category."""
    print("Requesting tips from the category 'Finance' (testing filtered requests):")
    request = {"operation": "get_tips", "category": "Finance"}
    print("Request: ", json.dumps(request, indent=4))

    socket.send_json(request)
    response = socket.recv_json()
    print("Response (filtered by category):", json.dumps(response, indent=4), "\n\n")


def test_rate_tip_valid():
    """Rating a tip"""
    # Use the first tip, any will do for testing
    print("Rating a tip (uses unfiltered get_tips operation to retrieve random tip id):")
    get_tips_request = {"operation": "get_tips"}
    socket.send_json(get_tips_request)
    tips_response = socket.recv_json()
    first_tip_id = tips_response["tips"][0]["tip_id"]

    request = {
        "operation": "rate_tip",
        "tip_id": first_tip_id,
        "rating": 2
    }
    print("Request: ", json.dumps(request, indent=4))

    socket.send_json(request)
    response = socket.recv_json()
    print("Response (rate tip):", json.dumps(response, indent=4), "\n\n")


def test_rate_tip_invalid_rating():
    """Test submitting an invalid rating."""
    get_tips_request = {"operation": "get_tips"}
    socket.send_json(get_tips_request)
    tips_response = socket.recv_json()
    first_tip_id = tips_response["tips"][0]["tip_id"]

    request = {
        "operation": "rate_tip",
        "tip_id": first_tip_id,
        "rating": 6  # Invalid rating
    }
    print("Request: ", json.dumps(request, indent=4))
    socket.send_json(request)
    response = socket.recv_json()
    print("Response (invalid rating):", json.dumps(response, indent=4), "\n\n")


def test_invalid_operation():
    """Test sending an invalid operation."""
    request = {"operation": "invalid_operation"}
    print("Request: ", json.dumps(request, indent=4))
    socket.send_json(request)
    response = socket.recv_json()
    print("Response (invalid operation):", json.dumps(response, indent=4), "\n\n")


def test_rate_and_get_updated_tip():
    """Test retrieving a tip, rating it, and verifying the updated rating."""
    # Step 1: Get tips
    request = {"operation": "get_tips"}
    print("Request: ", json.dumps(request, indent=4))
    socket.send_json(request)
    response = socket.recv_json()
    print("Response (get tips):", json.dumps(response, indent=4), "\n\n")

    # Step 2: Display the first tip and its associated rating
    first_tip = response["tips"][0]
    print(f"Displaying Tip: {first_tip['tip']} - Rating: {first_tip.get('average_rating', 'No rating')}\n\n")

    # Step 3: Rate the tip
    request = {
        "operation": "rate_tip",
        "tip_id": first_tip["tip_id"],  # Get the ID from the first tip
        "rating": 5
    }
    print("Request: ", json.dumps(request, indent=4))
    socket.send_json(request)
    rate_tip_response = socket.recv_json()
    print("Response (rate tip):", json.dumps(response, indent=4), "\n\n")

    # Step 4: Retrieve the same tip again to check if the rating was updated
    request = {
        "operation": "get_tip_by_id",
        "tip_id": first_tip["tip_id"]
    }
    print("Request: ", json.dumps(request, indent=4))
    socket.send_json(request)
    get_tip_response = socket.recv_json()
    print("Response (get updated tip):", json.dumps(response, indent=4), "\n\n")

    updated_tip = get_tip_response["tip"]
    print(f"Updated Tip: {updated_tip['tip']} - New Rating: {updated_tip['average_rating']}\n\n")


def test_insert_tip():
    """Test inserting a new tip."""
    # Prepare the request for inserting a new tip
    request = {
        "operation": "insert_tip",
        "tip": "Invest in stocks for long-term growth",
        "link": "https://example.com/stocks-tips",
        "category": "Investing"
    }
    print("Request: ", json.dumps(request, indent=4))
    socket.send_json(request)
    response = socket.recv_json()
    print("Response (insert tip):", json.dumps(response, indent=4), "\n\n")

    request = {"operation": "get_tip_by_id", "tip_id": response['tip_id']}
    socket.send_json(request)
    response = socket.recv_json()
    print("Response (get tip by id):", json.dumps(response, indent=4), "\n\n")


def test_delete_tip():
    """Test deleting a tip."""
    # Insert a new tip to be deleted later
    insert_request = {
        "operation": "insert_tip",
        "tip": "Save money by budgeting",
        "link": "https://example.com/budgeting-tips",
        "category": "Finance"
    }
    socket.send_json(insert_request)
    insert_response = socket.recv_json()
    tip_id_to_delete = insert_response["tip_id"]  # Get the inserted tip's ID

    # Now, delete the inserted tip
    delete_request = {
        "operation": "delete_tip",
        "tip_id": tip_id_to_delete
    }
    print("Request: ", json.dumps(delete_request, indent=4))
    socket.send_json(delete_request)
    delete_response = socket.recv_json()
    print("Response (delete tip):", json.dumps(delete_response, indent=4), "\n\n")


if __name__ == "__main__":
    print("Testing Financial Tips Microservice...\n\n")

    try:
        test_get_tips_no_category()
        test_get_tips_no_category()
        test_get_tips_filtered_by_category()
        test_rate_tip_valid()
        test_rate_tip_invalid_rating()
        test_invalid_operation()
        test_rate_and_get_updated_tip()
        test_insert_tip()
        test_delete_tip()

        print("\nAll tests passed!")
    except AssertionError as e:
        print("\nTest failed:", e)
