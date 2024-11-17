import zmq
import json

# Setup ZeroMQ REQ socket
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")


def test_get_tips_no_category():
    """Test fetching tips with no category; minimal request"""
    request = {"operation": "get_tips"}
    socket.send_json(request)
    response = socket.recv_json()
    print("Response (no category tips):", json.dumps(response, indent=4))
    assert "tips" in response, "Response should contain 'tips' key"
    assert isinstance(response["tips"], list), "'tips' should be a list"
    assert len(response["tips"]) == 3, "Should return 3 tips (unless db has less # of tips)"


def test_get_tips_filtered_by_category():
    """Test fetching tips filtered by category."""
    request = {"operation": "get_tips", "category": "Finance"}
    socket.send_json(request)
    response = socket.recv_json()
    print("Response (filtered by Finance):", json.dumps(response, indent=4))
    assert "tips" in response, "Response should contain 'tips' key"
    for tip in response["tips"]:
        assert tip["category"] == "Finance", "Each tip should match the requested category"


def test_rate_tip_valid():
    """Test submitting a valid rating."""
    # Use the first tip from the Finance category for rating
    get_tips_request = {"operation": "get_tips", "category": "Finance"}
    socket.send_json(get_tips_request)
    tips_response = socket.recv_json()
    first_tip_id = tips_response["tips"][0]["tip_id"]

    request = {
        "operation": "rate_tip",
        "tip_id": first_tip_id,
        "rating": 5
    }
    socket.send_json(request)
    response = socket.recv_json()
    print("Response (rate tip):", json.dumps(response, indent=4))
    assert response["message"] == "Rating submitted successfully", "Rating should be successful"
    assert "new_average_rating" in response, "Response should include new average rating"


def test_rate_tip_invalid_rating():
    """Test submitting an invalid rating."""
    # Use the first tip from the Investing category for invalid rating
    get_tips_request = {"operation": "get_tips", "category": "Investment"}
    socket.send_json(get_tips_request)
    tips_response = socket.recv_json()
    first_tip_id = tips_response["tips"][0]["tip_id"]

    request = {
        "operation": "rate_tip",
        "tip_id": first_tip_id,
        "rating": 6  # Invalid rating
    }
    socket.send_json(request)
    response = socket.recv_json()
    print("Response (invalid rating):", json.dumps(response, indent=4))
    assert response["message"] == "Invalid rating", "Server should reject invalid ratings"


def test_invalid_operation():
    """Test sending an invalid operation."""
    request = {"operation": "invalid_operation"}
    socket.send_json(request)
    response = socket.recv_json()
    print("Response (invalid operation):", json.dumps(response, indent=4))
    assert response["message"] == "Invalid operation", "Server should reject invalid operations"


def test_rate_and_get_updated_tip():
    """Test retrieving a tip, rating it, and verifying the updated rating."""
    # Step 1: Get tips with no category filter
    request = {"operation": "get_tips"}
    socket.send_json(request)
    response = socket.recv_json()
    print("Response (get tips):", response)

    assert "tips" in response, "Response should contain 'tips' key"
    assert len(response["tips"]) > 0, "There should be at least one tip in the response"

    # Step 2: Display the first tip and its associated rating
    first_tip = response["tips"][0]
    print(f"Displaying Tip: {first_tip['tip']} - Rating: {first_tip.get('average_rating', 'No rating')}")

    # Step 3: Rate the tip
    rate_tip_request = {
        "operation": "rate_tip",
        "tip_id": first_tip["tip_id"],  # Get the ID from the first tip
        "rating": 5
    }
    socket.send_json(rate_tip_request)
    rate_tip_response = socket.recv_json()
    print("Response (rate tip):", rate_tip_response)
    assert rate_tip_response["message"] == "Rating submitted successfully", "Rating should be successful"

    # Step 4: Retrieve the same tip again to check if the rating was updated
    get_tip_request = {
        "operation": "get_tip_by_id",
        "tip_id": first_tip["tip_id"]
    }
    socket.send_json(get_tip_request)
    get_tip_response = socket.recv_json()
    print("Response (get updated tip):", get_tip_response)

    assert "tip" in get_tip_response, "Response should contain 'tip' key"
    updated_tip = get_tip_response["tip"]
    print(f"Updated Tip: {updated_tip['tip']} - New Rating: {updated_tip['average_rating']}")


def test_insert_tip():
    """Test inserting a new tip."""
    # Prepare the request for inserting a new tip
    request = {
        "operation": "insert_tip",
        "tip": "Invest in stocks for long-term growth",
        "link": "https://example.com/stocks-tips",
        "category": "Investing"
    }
    socket.send_json(request)
    response = socket.recv_json()
    print("Response (insert tip):", json.dumps(response, indent=4))

    # Check if the response contains the expected success message
    assert response["message"] == "Tip inserted successfully", "Tip insertion failed"
    assert "tip_id" in response, "Response should contain 'tip_id' key"
    assert response["session_id"] is not None, "Response should contain 'session_id'"


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
    socket.send_json(delete_request)
    delete_response = socket.recv_json()
    print("Response (delete tip):", json.dumps(delete_response, indent=4))

    # Check if the response confirms the tip deletion
    assert delete_response["message"] == "Tip deleted successfully", "Tip deletion failed"
    assert delete_response["tip_id"] == tip_id_to_delete, "Deleted tip ID does not match"
    assert delete_response["session_id"] is not None, "Response should contain 'session_id'"



if __name__ == "__main__":
    print("Testing Financial Tips Microservice...")

    try:
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
