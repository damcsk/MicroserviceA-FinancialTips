import zmq
import json

# Sample financial tips database
FINANCIAL_TIPS = [
    {
        "tip": "Create a monthly budget",
        "link": "https://example.com/budgeting",
        "category": "Budgeting",
        "tip_id": "0001",
        "ratings": [5,4,4]
     },
    {
        "tip": "Start an emergency fund",
        "link": "https://example.com/emergency-fund",
        "category": "Savings",
        "tip_id": "0002",
        "ratings": [5,5]
    },
    {
        "tip": "Pay off high-interest debt first",
        "link": "https://example.com/debt-management",
        "category": "Debt Management",
        "tip_id": "0003",
        "ratings": [3]
    },
    {
        "tip": "Invest in low-cost index funds",
        "link": "https://example.com/investing",
        "category": "Investing",
        "tip_id": "0004",
        "ratings": []
    },
    {
        "tip": "Track your expenses weekly",
        "link": "https://example.com/track-expenses",
        "category": "Budgeting",
        "tip_id": "0005",
        "ratings": [4]
    },
]


# Setup ZeroMQ REQ socket (for sending requests)
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

print("Financial Tips Microservice is running...")

while True:
    # Receive a request
    request = socket.recv_json()
    print("Received request:", request)

    operation = request.get("operation")
    response = {"message": "Invalid operation"}

    if operation == "get_tips":
        # Category is optional
        category = request.get("category")
        if category:
            # Filter tips by category (lower for case-insensitive)
            filtered_tips = [tip for tip in FINANCIAL_TIPS if tip["category"].lower() == category.lower()]
        else:
            # Return all tips if no category is specified
            filtered_tips = FINANCIAL_TIPS

        # Ensure at least 3 tips are sent;
        # Will probably need to update this for no found tips and to randomize the found tips
        response = {
            "tips": filtered_tips[:3]
        }
    elif operation == "rate_tip":
        tip_id = request.get("tip_id")
        rating = request.get("rating")

        # Find the tip by ID
        tip = next((tip for tip in FINANCIAL_TIPS if tip["tip_id"] == tip_id), None)

        if tip:
            if 0 <= rating <= 5:
                # Update ratings and calculate new average
                tip["ratings"].append(rating)
                average_rating = sum(tip["ratings"]) / len(tip["ratings"])

                response = {
                    "message": "Rating submitted successfully",
                    "tip_id": tip_id,
                    "new_average_rating": round(average_rating, 2),
                }
            else:
                response = {"message": "Invalid rating"}
        else:
            response = {"message": "Invalid tip_id or tip_id not found"}

    # Send the response
    socket.send_json(response)
