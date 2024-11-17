import sqlite3
import uuid


def create_example_entries():
    # Connect to SQLite database
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

    # Example data for seeding
    example_tips = [
        (
        "Save for Retirement Early to Maximize Compound Interest", "https://example.com/retirement-early", "Retirement",
        5, 1),
        ("How to Build a Solid Emergency Fund", "https://example.com/emergency-fund", "Saving", 5, 1),
        ("Understanding the Importance of Your Net Worth", "https://example.com/net-worth", "Finance", 5, 1),
        ("How to Diversify Your Investment Portfolio", "https://example.com/diversify-investments", "Investment", 5, 1),
        ("Tips for Paying Off Debt Faster", "https://example.com/pay-debt", "Debt", 5, 1),
        ("Mastering the Basics of Budgeting", "https://example.com/budgeting-basics", "Budgeting", 5, 1),
        ("The Best Retirement Accounts for Tax Savings", "https://example.com/tax-savings-retirement", "Taxes", 5, 1),
        ("5 Steps to Improve Your Credit Score", "https://example.com/improve-credit-score", "Credit", 5, 1),
        ("The Power of Automatic Savings for Long-Term Goals", "https://example.com/automatic-savings", "Saving", 5, 1),
        ("How to Choose the Right Insurance for Your Needs", "https://example.com/right-insurance", "Insurance", 5, 1),
        (
        "Understanding IRAs and 401(k)s: Which is Better for You?", "https://example.com/iras-vs-401k", "Retirement", 5,
        1),
        ("How to Save on Household Bills and Utilities", "https://example.com/save-utilities", "Saving", 5, 1),
        ("Investing in Real Estate: Key Considerations", "https://example.com/real-estate-investing", "Real Estate", 5,
         1),
        ("The Role of Estate Planning in Your Financial Future", "https://example.com/estate-planning",
         "Estate Planning", 5, 1),
        ("How to Build Wealth as a Millennial", "https://example.com/millennial-wealth", "Investment", 5, 1),
        ("How to Maximize Your Tax Deductions", "https://example.com/tax-deductions", "Taxes", 5, 1),
        (
        "Planning for Healthcare Costs in Retirement", "https://example.com/healthcare-retirement", "Healthcare", 5, 1),
        ("Why You Should Invest in a Tax-Free Savings Account", "https://example.com/tfsa-investing", "Investment", 5,
         1),
        (
        "Why Financial Literacy is Critical for Parents", "https://example.com/financial-literacy-parents", "Education",
        5, 1),
        ("The Benefits of Working with a Fee-Only Financial Advisor", "https://example.com/fee-only-advisor", "Finance",
         5, 1),
        ("How to Cut Costs without Sacrificing Quality", "https://example.com/cut-costs", "Budgeting", 5, 1),
        (
        "Managing Your Investment Risk in Volatile Markets", "https://example.com/investment-risk", "Investment", 5, 1),
        ("Should You Refinance Your Mortgage?", "https://example.com/refinance-mortgage", "Real Estate", 5, 1),
        (
        "How to Take Advantage of Employer Retirement Plans", "https://example.com/employer-plans", "Retirement", 5, 1),
        (
        "How to Protect Your Wealth with Insurance", "https://example.com/protect-wealth-insurance", "Insurance", 5, 1),
        ("The Best Time to Start Saving for College", "https://example.com/college-saving", "Education", 5, 1),
        ("How to Maximize Your Social Security Benefits", "https://example.com/social-security", "Retirement", 5, 1),
        ("Understanding Bonds: A Beginner’s Guide", "https://example.com/understanding-bonds", "Investment", 5, 1),
        ("How to Invest in Cryptocurrency Safely", "https://example.com/cryptocurrency-investing", "Investment", 5, 1),
        ("The Basics of Filing Your Taxes", "https://example.com/filing-taxes", "Taxes", 5, 1),
        (
        "How to Start Investing with Little Money", "https://example.com/invest-with-little-money", "Investment", 5, 1),
        ("Protecting Your Assets with Estate Planning Tools", "https://example.com/estate-planning-tools",
         "Estate Planning", 5, 1),
        ("How to Maximize Your 401(k) Contributions", "https://example.com/401k-contributions", "Retirement", 5, 1),
        ("How to Build a Sustainable Monthly Budget", "https://example.com/sustainable-budget", "Budgeting", 5, 1),
        ("Investing in Stocks vs. Bonds: What You Need to Know", "https://example.com/stocks-vs-bonds", "Investment", 5,
         1),
        (
        "Protecting Your Family’s Future with Life Insurance", "https://example.com/life-insurance", "Insurance", 5, 1),
        (
        "How to Start Saving for Your Child’s College Education", "https://example.com/college-savings", "Education", 5,
        1),
        ("How to Make the Most of Your Tax Refund", "https://example.com/tax-refund", "Taxes", 5, 1),
        ("The Importance of Having a Financial Plan", "https://example.com/financial-plan", "Finance", 5, 1),
        ("Maximizing Your Investment Portfolio with ETFs", "https://example.com/max-etfs", "Investment", 5, 1),
        ("How to Build Wealth with Real Estate", "https://example.com/real-estate-wealth", "Real Estate", 5, 1),
        ("Why You Should Reevaluate Your Budget Every Year", "https://example.com/re-evaluate-budget", "Budgeting", 5,
         1),
        (
        "How to Protect Your Wealth in Retirement", "https://example.com/retirement-wealth-protection", "Retirement", 5,
        1),
        ("The Best Investment Strategies for Beginners", "https://example.com/investment-strategies", "Investment", 5,
         1),
        ("How to Manage Debt During Economic Uncertainty", "https://example.com/manage-debt-uncertainty", "Debt", 5, 1),
        ("How to Invest in Real Estate with Little Capital", "https://example.com/real-estate-small-capital",
         "Real Estate", 5, 1),
        ("Why You Should Consider a Roth IRA", "https://example.com/roth-ira", "Retirement", 5, 1),
        ("The Benefits of a High-Yield Savings Account", "https://example.com/high-yield-savings", "Saving", 5, 1),
        ("How to Use Credit Wisely and Improve Your Score", "https://example.com/credit-wisely", "Credit", 5, 1),
        ("How to Prepare for Major Financial Expenses", "https://example.com/prepare-major-expenses", "Finance", 5, 1),
        ("Top Strategies for Paying Off Student Loans", "https://example.com/pay-student-loans", "Debt", 5, 1),
        ("How to Invest in Index Funds for Steady Growth", "https://example.com/index-fund-investing", "Investment", 5,
         1),
        ("How to Understand Your Tax Bracket", "https://example.com/tax-bracket", "Taxes", 5, 1),
        ("How to Plan for Retirement as a Freelancer", "https://example.com/freelancer-retirement", "Retirement", 5, 1),
        ("The Importance of Disability Insurance", "https://example.com/disability-insurance", "Insurance", 5, 1),
        ("Building a Strong Investment Foundation with ETFs", "https://example.com/etf-investment", "Investment", 5, 1),
        (
        "How to Buy Your First Home Without Overstretching", "https://example.com/buy-first-home", "Real Estate", 5, 1),
        ("Understanding Capital Gains Tax", "https://example.com/capital-gains-tax", "Taxes", 5, 1),
        (
        "How to Create a Comprehensive Estate Plan", "https://example.com/comprehensive-estate-plan", "Estate Planning",
        5, 1),
        ("Why You Should Regularly Review Your Insurance Policies", "https://example.com/review-insurance", "Insurance",
         5, 1),
        ("How to Start Investing with $500 or Less", "https://example.com/start-investing-500", "Investment", 5, 1),
        ("How to Build Your Financial Safety Net", "https://example.com/financial-safety-net", "Saving", 5, 1),
        ("How to Plan for a Comfortable Retirement", "https://example.com/comfortable-retirement", "Retirement", 5, 1),
        ("The Basics of Real Estate Tax Deductions", "https://example.com/real-estate-deductions", "Taxes", 5, 1),
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
