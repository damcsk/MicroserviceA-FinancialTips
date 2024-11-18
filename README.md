# Financial Tips Microservice

This document outlines how to interact with the Financial Tips Microservice. 
The service supports a few key operations that allow clients to request tips, rate them, and manage the tip database. 
All communication happens over ZeroMQ using the REQ/REP protocol.

## Requesting Data:

To request data from the Financial Tips Microservice, you will need to send a JSON request to the server using ZeroMQ. Each request contains an operation type and relevant data, depending on the operation.

### Request Structure:

The request should be a JSON object with the following keys:

    - operation (Required): A string representing the operation you wish to perform. Possible values:
        get_tips
        rate_tip
        get_tip_by_id
        insert_tip
        delete_tip

    - session_id (Optional for all operations): A string representing the session ID. If not provided, a new session is created. Every response will provide the current session ID, which you can then use for this field.

    - category (Optional for get_tips, Required for insert_tip): The category of tips you want to filter by.

    - tip_id (Required for rate_tip, get_tip_by_id, and delete_tip): The ID of the tip (get_tips will include the ID of the tips in the response)

    - rating (Required for rate_tip): The rating score (between 0 and 5) for a tip.

    - tip (Required for insert_tip): The text of the tip (i.e. the name or title).

    - link (Required for insert_tip): A link associated with the tip.


### Example Requests

Requests will use json objects sent to the connected zmq socket

    request = {"operation": "get_tips"}
    socket.send_json(request)
    response = socket.recv_json()

**Request json objects examples below:**

To request tips a random sample of tips:

    {
        "operation": "get_tips",
    }

To request tips filtered by category:

    {
        "operation": "get_tips",
        "session_id": "abc123",
        "category": "Finance"
    }

To request a specific tip:

    {
        "operation": "get_tip_by_id",
        "session_id": "abc123",
        "tip_id": "123abc"
    }

To rate a specific tip:

    {
        "operation": "rate_tip",
        "session_id": "abc123",
        "tip_id": "id-of-tip",
        "rating": 4
    }

To insert a new tip:

    {
        "operation": "insert_tip",
        "session_id": "abc123",
        "tip": "Supersize your Retirement Savings!"
        "category": "Retirement"
        "link": "http://example.com/supersize-retirement
    }

## Receiving Data:

After you send a request, the server will process it and respond with a JSON object. The response will include the requested data, or a message indicating the result of the operation.

Additionally, every response will include the current session id. In order to diversify the tips provided, the session id should be saved and used in any future requests for a persistent session, as well as to prevent a user from rating an article multiple times in a session.

### Response Structure:

The response will be a JSON object with the following keys:

    message: A string indicating the result of the operation.
    session_id: The session ID associated with the request.
    tips (Optional for get_tips): An array of tips returned by the request.
    tip (Optional for get_tip_by_id): A single tip object with details.
    new_average_rating (Optional for rate_tip): The new average rating after submitting a rating.

Example Response for get_tips

    {
        "tips": [
            {
                "tip_id": "id-of-tip-1",
                "tip": "Save more by tracking expenses",
                "link": "http://example.com/track-expenses",
                "category": "Saving",
                "average_rating": 4.52
            },
            {
                "tip_id": "id-of-tip-2",
                "tip": "Invest early and often",
                "link": "http://example.com/early-investment",
                "category": "Investing",
                "average_rating": 4.01
            }
        ],
        "session_id": "abc123"
    }

Example Response for rate_tip

    {
        "message": "Rating submitted successfully",
        "tip_id": "id-of-tip",
        "new_average_rating": 4.25,
        "session_id": "abc123"
    }

Example Response for get_tip_by_id

    {
        "tip": {
          "tip_id": "id-of-tip",
          "tip": "Save more by tracking expenses",
          "link": "http://example.com",
          "category": "Saving",
          "average_rating": 4.52
        },
        "session_id": "abc123"
    }

Example Response for an invalid request

    {
        "message": "Error message",
        "session_id": "abc123"
    }

## Database Instructions

The microservice currently includes the financial_tips.db, a sqllite database. This is populated by dummy article names and links to non-existant articles.

To create a new database, tools have been included to help: db_seed.py in the root directory, and FormatDBSeedData.xlsx in the seed_tool directory

1. Delete the database, if no longer wanted/needed
2. Use the excel file tool to generate the correct DB seed data based on you article names, links, categories, ratings, and ratings counts. The db_seed.py formatting column (column F) has a simple excel formula that will format the article data for you.
3. Open the db_seed.py file and copy/paste the formatted article data into the example_tips variable (paste the data between the brackets, creating a list)
4. Run the db_seed.py file. It will create a new financial_tips.db based on the example_tips variable data you provided.

**Example variable data:**

    example_tips = [
        ("Save for Retirement Early to Maximize Compound Interest", "https://example.com/retirement-early", "Retirement", 5, 1),
        ("How to Build a Solid Emergency Fund", "https://example.com/emergency-fund", "Saving", 3.5, 25),
        ("Understanding the Importance of Your Net Worth", "https://example.com/net-worth", "Finance", 1.25, 15),
    ]

## UML Sequence Diagram

Below is a UML sequence diagram that illustrates the flow of requesting and receiving data from the microservice:

![UML_Sequence](https://github.com/user-attachments/assets/b5bbf7d8-fc5d-47d3-9235-bd6c4a683464)

## Important Notes

    Session Management: Each client interaction is tracked by a session ID. If no session ID is provided, a new one is created.
    Error Handling: If an operation fails (e.g., invalid tip ID), the server will return an appropriate error message.
    Article Links: Article links currently do not lead to any actual articles
