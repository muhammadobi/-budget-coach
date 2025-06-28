import unittest
import pandas as pd
import tempfile
import os
from database import BudgetDatabase
from financial_advisor import FinancialAdvisor

class TestBudgetLogic(unittest.TestCase):
    
    def setUp(self):
        """Set up test database and advisor"""
        self.test_db_path = tempfile.mktemp()
        self.db = BudgetDatabase(self.test_db_path)
        self.advisor = FinancialAdvisor()
    
    def tearDown(self):
        """Clean up test database"""
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
    
    def test_database_initialization(self):
        """Test that database initializes correctly with tables and default categories"""
        categories = self.db.get_categories()
        self.assertGreater(len(categories), 0)
        
        # Check that we have both income and expense categories
        income_categories = self.db.get_categories('income')
        expense_categories = self.db.get_categories('expense')
        self.assertGreater(len(income_categories), 0)
        self.assertGreater(len(expense_categories), 0)
    
    def test_add_transaction(self):
        """Test adding transactions to the database"""
        # Add income transaction
        self.db.add_transaction('2024-01-15', 'Test Salary', 3000.00, 'Salary', 'income')
        
        # Add expense transaction
        self.db.add_transaction('2024-01-16', 'Test Groceries', 100.00, 'Food & Dining', 'expense')
        
        # Retrieve transactions
        transactions = self.db.get_transactions()
        self.assertEqual(len(transactions), 2)
        
        # Check transaction details
        income_transaction = transactions[transactions['type'] == 'income'].iloc[0]
        self.assertEqual(income_transaction['amount'], 3000.00)
        self.assertEqual(income_transaction['category'], 'Salary')
        
        expense_transaction = transactions[transactions['type'] == 'expense'].iloc[0]
        self.assertEqual(expense_transaction['amount'], 100.00)
        self.assertEqual(expense_transaction['category'], 'Food & Dining')
    
    def test_budget_analysis_no_data(self):
        """Test budget analysis with no data"""
        empty_df = pd.DataFrame()
        analysis = self.advisor.analyze_budget(empty_df)
        self.assertEqual(analysis['status'], 'insufficient_data')
    
    def test_budget_analysis_with_data(self):
        """Test budget analysis with sample data"""
        # Create sample data
        sample_data = pd.DataFrame([
            {'date': '2024-01-15', 'amount': 3000, 'type': 'income', 'category': 'Salary'},
            {'date': '2024-01-16', 'amount': 1200, 'type': 'expense', 'category': 'Housing'},
            {'date': '2024-01-17', 'amount': 300, 'type': 'expense', 'category': 'Food & Dining'},
            {'date': '2024-01-18', 'amount': 150, 'type': 'expense', 'category': 'Entertainment'},
        ])
        
        analysis = self.advisor.analyze_budget(sample_data)
        self.assertEqual(analysis['status'], 'success')
        self.assertEqual(analysis['total_income'], 3000)
        self.assertEqual(analysis['total_expenses'], 1650)
        self.assertEqual(analysis['savings_potential'], 1350)
        self.assertGreater(len(analysis['advice']), 0)
    
    def test_50_30_20_rule_analysis(self):
        """Test 50/30/20 rule calculations"""
        # Test with income of $3000
        # Needs: $1200 (40%) - within 50% target
        # Wants: $150 (5%) - within 30% target  
        # Savings: $1650 (55%) - exceeds 20% target
        
        sample_data = pd.DataFrame([
            {'date': '2024-01-15', 'amount': 3000, 'type': 'income', 'category': 'Salary'},
            {'date': '2024-01-16', 'amount': 1200, 'type': 'expense', 'category': 'Housing'},  # Need
            {'date': '2024-01-17', 'amount': 150, 'type': 'expense', 'category': 'Entertainment'},  # Want
        ])
        
        analysis = self.advisor.analyze_budget(sample_data)
        
        # Should be successful analysis
        self.assertEqual(analysis['status'], 'success')
        
        # Check expense ratio is reasonable (not spending too much)
        self.assertLess(analysis['expense_ratio'], 0.8)  # Less than 80% spending is good
    
    def test_csv_export_import(self):
        """Test CSV export and import functionality"""
        # Add some test data
        self.db.add_transaction('2024-01-15', 'Test Income', 1000.00, 'Salary', 'income')
        self.db.add_transaction('2024-01-16', 'Test Expense', 100.00, 'Food & Dining', 'expense')
        
        # Export to CSV
        csv_path = tempfile.mktemp(suffix='.csv')
        count = self.db.export_to_csv(csv_path)
        self.assertEqual(count, 2)
        
        # Verify file exists and has content
        self.assertTrue(os.path.exists(csv_path))
        
        # Create new database and import
        new_db_path = tempfile.mktemp()
        new_db = BudgetDatabase(new_db_path)
        
        # Import the CSV
        import_count = new_db.import_from_csv(csv_path)
        self.assertEqual(import_count, 2)
        
        # Verify imported data
        imported_transactions = new_db.get_transactions()
        self.assertEqual(len(imported_transactions), 2)
        
        # Clean up
        os.remove(csv_path)
        os.remove(new_db_path)
    
    def test_delete_transaction(self):
        """Test deleting transactions"""
        # Add a transaction
        self.db.add_transaction('2024-01-15', 'Test Transaction', 100.00, 'Food & Dining', 'expense')
        
        # Get the transaction ID
        transactions = self.db.get_transactions()
        self.assertEqual(len(transactions), 1)
        transaction_id = transactions.iloc[0]['id']
        
        # Delete the transaction
        self.db.delete_transaction(transaction_id)
        
        # Verify it's deleted
        transactions_after = self.db.get_transactions()
        self.assertEqual(len(transactions_after), 0)
    
    def test_savings_goals_advice(self):
        """Test savings goals advice calculation"""
        monthly_income = 3000
        current_savings = 1000
        
        goals = self.advisor.get_savings_goals_advice(monthly_income, current_savings)
        
        # Should have at least emergency fund goal
        self.assertGreater(len(goals), 0)
        
        # Check emergency fund goal
        emergency_goal = next((g for g in goals if g['title'] == 'Emergency Fund'), None)
        self.assertIsNotNone(emergency_goal)
        self.assertEqual(emergency_goal['target'], monthly_income * 6)  # 6 months of income
        self.assertEqual(emergency_goal['current'], current_savings)

class TestFinancialTips(unittest.TestCase):
    
    def setUp(self):
        self.advisor = FinancialAdvisor()
    
    def test_get_random_tip(self):
        """Test getting random financial tips"""
        tip = self.advisor.get_random_tip()
        self.assertIsInstance(tip, dict)
        self.assertIn('title', tip)
        self.assertIn('content', tip)
    
    def test_tips_contain_expected_content(self):
        """Test that tips contain expected financial concepts"""
        # Get all tips and check for key concepts
        all_tips = [self.advisor.get_random_tip() for _ in range(20)]  # Get multiple tips
        tip_titles = [tip['title'] for tip in all_tips]
        
        # Should contain some core financial concepts
        has_emergency_fund = any('Emergency' in title for title in tip_titles)
        has_compound_interest = any('Compound' in title for title in tip_titles)
        has_50_30_20 = any('50/30/20' in title for title in tip_titles)
        
        # At least one of these should be present in our sample
        self.assertTrue(has_emergency_fund or has_compound_interest or has_50_30_20)

if __name__ == '__main__':
    print("🧪 Running Budget Coach Unit Tests...")
    unittest.main() 