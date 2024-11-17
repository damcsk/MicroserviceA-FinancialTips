import sqlite3
import uuid


def create_example_entries():
    # Connect to SQLite database
    conn = sqlite3.connect("financial_tips.db")
    cursor = conn.cursor()

    # Example data for seeding
    example_tips = [
        ("Save for retirement", "http://example.com/retirement", "Finance", 4.5, 20),
        ("Create a budget", "http://example.com/budget", "Finance", 4.2, 15),
        ("Start an emergency fund", "http://example.com/emergency-fund", "Finance", 4.8, 10),
        ("Track your expenses", "http://example.com/expenses", "Finance", 4.0, 30),
        ("Invest in stocks", "http://example.com/stocks", "Investing", 4.7, 25),
        ("Diversify your portfolio", "http://example.com/diversify", "Investing", 4.6, 18),
        ("Don't time the market", "http://example.com/market-timing", "Investing", 4.4, 22),
        ("Use tax-advantaged accounts", "http://example.com/tax-advantage", "Finance", 4.5, 20),
        ("Pay off high-interest debt", "http://example.com/debt", "Finance", 4.3, 28),
        ("Invest in real estate", "http://example.com/real-estate", "Investing", 4.7, 12),
        ("Build your credit score", "http://example.com/credit", "Finance", 4.1, 35),
        ("Start a side hustle", "http://example.com/side-hustle", "Entrepreneurship", 4.5, 10),
        ("Learn about passive income", "http://example.com/passive-income", "Entrepreneurship", 4.8, 8),
        ("Understand taxes", "http://example.com/taxes", "Finance", 4.2, 40),
        ("Cut unnecessary expenses", "http://example.com/cut-expenses", "Finance", 4.3, 33),
        ("Invest in index funds", "http://example.com/index-funds", "Investing", 4.6, 19),
        ("Automate savings", "http://example.com/automate-savings", "Finance", 4.5, 14),
        ("Use a financial advisor", "http://example.com/advisor", "Finance", 4.0, 10),
        ("Track your net worth", "http://example.com/net-worth", "Finance", 4.4, 18),
        ("Save for a down payment", "http://example.com/down-payment", "Real Estate", 4.7, 15)
    ]

    # Insert example tips into the 'tips' table
    for tip in example_tips:
        tip_id = str(uuid.uuid4())  # Generate a unique ID for each tip
        cursor.execute("""
            INSERT INTO tips (tip_id, tip, link, category, average_rating, rating_count)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (tip_id, tip[0], tip[1], tip[2], tip[3], tip[4]))

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("20 example entries have been added to the database.")


if __name__ == "__main__":
    create_example_entries()
