import zmq
import json
import collections
import random
import uuid
import sqlite3

# Create a database connection
conn = sqlite3.connect("financial_tips.db")
cursor = conn.cursor()

# Create tables if it does not exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tips (
        tip_id TEXT PRIMARY KEY,
        tip TEXT,
        link TEXT,
        category TEXT,
        average_rating REAL,
        rating_count INTEGER
    )
""")
conn.commit()

# In-memory session tracking - not the best, but without user ids and logins this is what I
# decided to go with
sessions = {}

# Setup ZeroMQ REQ socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

print("Financial Tips Microservice is running...")


# Function to load tips from the database
def get_filtered_tips(category=None):
    try:
        if category:
            # Filter tips based on category
            cursor.execute("SELECT * FROM tips WHERE category = ?", (category,))
        else:
            # Get all tips if no category selected
            # Might want to rethink as DB scales
            cursor.execute("SELECT * FROM tips")

        # Reads all records into memory, and then returns that list
        rows = cursor.fetchall()
        return [{"tip_id": row[0], "tip": row[1], "link": row[2], "category": row[3],
                 "average_rating": row[4], "rating_count": row[5]} for row in rows]
    except sqlite3.DatabaseError as e:
        # TODO: more robust error handling
        print(f"Error fetching tips: {e}")
        return []


# Handle requests
while True:
    # Receive a request
    request = socket.recv_json()
    print("Received request:", request)

    operation = request.get("operation")
    response = {"message": "Invalid operation"}

    # Generate a session ID for each request. If not provided, it's a new session
    # Not quite familiar enough with UUID - need to study further
    session_id = request.get("session_id") or str(uuid.uuid4())

    # Initialize session data if it's a new session
    if session_id not in sessions:
        sessions[session_id] = {
            'shown_tips': collections.deque(maxlen=5),  # For tracking shown tips
            'rated_tips': set()  # For tracking rated tips
        }

    if operation == "get_tips":
        category = request.get("category")

        # Filter tips based on the requested category, or return all tips if no category selected
        filtered_tips = get_filtered_tips(category)

        # Filter out tips already shown in this session
        # Create an empty list to store the new tips
        new_tips = []

        # Get the list of IDs of the tips that have already been shown
        shown_tip_ids = []
        for shown_tip in sessions[session_id]["shown_tips"]:
            shown_tip_ids.append(shown_tip["tip_id"])

        # Go through each tip in filtered_tips
        for tip in filtered_tips:
            # Check if the tip's ID is not in the list of shown tip IDs
            if tip["tip_id"] not in shown_tip_ids:
                new_tips.append(tip)  # Add the tip to the new_tips list

        # If fewer than 3 unique tips are available, select more from the filtered list
        if len(new_tips) < 3:
            new_tips.extend(filtered_tips)

        # Randomly shuffle to prevent ordering bias, then pick first 3
        random.shuffle(new_tips)
        selected_tips = new_tips[:3]

        # Update the session cache with the selected tips
        sessions[session_id]["shown_tips"].extend(selected_tips)

        # Respond with the selected tips
        response = {
            "tips": [{"tip": tip["tip"], "link": tip["link"], "category": tip["category"]} for tip in selected_tips],
            "session_id": session_id
        }

    # Handle "rate_tip" operation
    elif operation == "rate_tip":
        tip_id = request.get("tip_id")
        rating = request.get("rating")

        if 0 <= rating <= 5:
            try:
                # Find the tip by ID
                cursor.execute("SELECT average_rating, rating_count FROM tips WHERE tip_id = ?", (tip_id,))
                tip = cursor.fetchone()

                if tip:
                    # Check if the tip has already been rated in this session
                    if tip_id in sessions[session_id]["rated_tips"]:
                        response = {"message": "You have already rated this tip"}
                    else:
                        # Calculate the new average rating
                        current_avg, count = tip
                        new_avg = ((current_avg * count) + rating) / (count + 1) if current_avg is not None else rating
                        new_count = count + 1

                        # Update the database with the new average and count
                        cursor.execute("""
                            UPDATE tips SET average_rating = ?, rating_count = ? WHERE tip_id = ?
                        """, (new_avg, new_count, tip_id))
                        conn.commit()

                        # Mark tip as rated
                        sessions[session_id]["rated_tips"].add(tip_id)

                        response = {
                            "message": "Rating submitted successfully",
                            "tip_id": tip_id,
                            "new_average_rating": round(new_avg, 2),
                        }
                else:
                    response = {"message": "Invalid tip id or tip id not found"}
            except sqlite3.DatabaseError as e:
                print(f"Error processing rating: {e}")
                response = {"message": "Error processing rating"}
        else:
            response = {"message": "Invalid rating"}

    # Send the response
    socket.send_json(response)


