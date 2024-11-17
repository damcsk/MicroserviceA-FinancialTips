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


### Example Request

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


## UML Sequence Diagram

Below is a UML sequence diagram that illustrates the flow of requesting and receiving data from the microservice:



## Important Notes

    Session Management: Each client interaction is tracked by a session ID. If no session ID is provided, a new one is created.
    Error Handling: If an operation fails (e.g., invalid tip ID), the server will return an appropriate error message.
