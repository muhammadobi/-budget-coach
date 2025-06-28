from database import BudgetDatabase
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Create sample transactions to demonstrate the app functionality"""
    db = BudgetDatabase()
    
    # Sample data for the last 3 months
    sample_transactions = [
        # Income transactions
        ("2024-01-15", "Monthly Salary", 3500.00, "Salary", "income"),
        ("2024-01-20", "Freelance Project", 800.00, "Freelance", "income"),
        ("2024-02-15", "Monthly Salary", 3500.00, "Salary", "income"),
        ("2024-02-28", "Tax Refund", 450.00, "Other Income", "income"),
        ("2024-03-15", "Monthly Salary", 3500.00, "Salary", "income"),
        ("2024-03-25", "Side Gig", 300.00, "Freelance", "income"),
        
        # Expense transactions - January
        ("2024-01-01", "Rent Payment", 1200.00, "Housing", "expense"),
        ("2024-01-02", "Grocery Shopping", 85.50, "Food & Dining", "expense"),
        ("2024-01-05", "Electric Bill", 120.00, "Utilities", "expense"),
        ("2024-01-08", "Gas Station", 45.00, "Transportation", "expense"),
        ("2024-01-10", "Movie Night", 25.00, "Entertainment", "expense"),
        ("2024-01-12", "Lunch Out", 15.80, "Food & Dining", "expense"),
        ("2024-01-15", "New Shoes", 89.99, "Shopping", "expense"),
        ("2024-01-18", "Doctor Visit", 75.00, "Healthcare", "expense"),
        ("2024-01-20", "Groceries", 92.30, "Food & Dining", "expense"),
        ("2024-01-22", "Internet Bill", 60.00, "Utilities", "expense"),
        ("2024-01-25", "Coffee Shop", 6.50, "Food & Dining", "expense"),
        ("2024-01-28", "Gas Station", 42.00, "Transportation", "expense"),
        ("2024-01-30", "Dinner Date", 68.00, "Entertainment", "expense"),
        
        # Expense transactions - February
        ("2024-02-01", "Rent Payment", 1200.00, "Housing", "expense"),
        ("2024-02-03", "Grocery Shopping", 78.20, "Food & Dining", "expense"),
        ("2024-02-05", "Electric Bill", 95.00, "Utilities", "expense"),
        ("2024-02-07", "Gas Station", 38.50, "Transportation", "expense"),
        ("2024-02-10", "Streaming Subscription", 12.99, "Entertainment", "expense"),
        ("2024-02-12", "Lunch Meeting", 22.50, "Food & Dining", "expense"),
        ("2024-02-14", "Valentine's Gifts", 125.00, "Shopping", "expense"),
        ("2024-02-17", "Pharmacy", 28.50, "Healthcare", "expense"),
        ("2024-02-20", "Groceries", 88.75, "Food & Dining", "expense"),
        ("2024-02-23", "Concert Tickets", 85.00, "Entertainment", "expense"),
        ("2024-02-25", "Coffee", 4.25, "Food & Dining", "expense"),
        ("2024-02-27", "Gas Station", 41.00, "Transportation", "expense"),
        
        # Expense transactions - March (Current month)
        ("2024-03-01", "Rent Payment", 1200.00, "Housing", "expense"),
        ("2024-03-02", "Grocery Shopping", 91.40, "Food & Dining", "expense"),
        ("2024-03-04", "Electric Bill", 110.00, "Utilities", "expense"),
        ("2024-03-06", "Gas Station", 44.20, "Transportation", "expense"),
        ("2024-03-08", "Book Purchase", 24.99, "Education", "expense"),
        ("2024-03-10", "Lunch", 18.75, "Food & Dining", "expense"),
        ("2024-03-12", "New Jacket", 75.00, "Shopping", "expense"),
        ("2024-03-15", "Gym Membership", 45.00, "Healthcare", "expense"),
        ("2024-03-17", "Groceries", 82.60, "Food & Dining", "expense"),
        ("2024-03-19", "Movie Theater", 15.50, "Entertainment", "expense"),
        ("2024-03-21", "Coffee Shop", 7.80, "Food & Dining", "expense"),
        ("2024-03-23", "Gas Station", 39.50, "Transportation", "expense"),
        ("2024-03-25", "Phone Bill", 55.00, "Utilities", "expense"),
    ]
    
    print("🚀 Adding sample data to demonstrate Budget Coach...")
    
    for date, description, amount, category, transaction_type in sample_transactions:
        try:
            db.add_transaction(date, description, amount, category, transaction_type)
        except Exception as e:
            print(f"Error adding transaction: {e}")
    
    print(f"✅ Successfully added {len(sample_transactions)} sample transactions!")
    print("💡 You can now see charts, analytics, and financial advice in the app.")
    
    return len(sample_transactions)

if __name__ == "__main__":
    create_sample_data() 