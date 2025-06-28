import pandas as pd
from datetime import datetime, timedelta
import random
import json
import os

class FinancialAdvisor:
    def __init__(self):
        self.financial_tips = self.load_tips_from_json()
    
    def load_tips_from_json(self):
        """Load financial tips from tips.json file"""
        try:
            if os.path.exists('tips.json'):
                with open('tips.json', 'r') as f:
                    data = json.load(f)
                    return data.get('tips', [])
            else:
                # Fallback to embedded tips if JSON file doesn't exist
                return self.get_fallback_tips()
        except Exception as e:
            print(f"Error loading tips from JSON: {e}")
            return self.get_fallback_tips()
    
    def get_fallback_tips(self):
        """Fallback tips if JSON loading fails"""
        return [
            {
                "title": "The 50/30/20 Rule",
                "content": "**The 50/30/20 budgeting rule is a simple way to manage your money:**\n\n- **50% for Needs**: Essential expenses like rent, groceries, utilities\n- **30% for Wants**: Entertainment, dining out, hobbies\n- **20% for Savings**: Emergency fund, retirement, debt payment\n\nThis rule helps ensure you're living within your means while building wealth!",
                "category": "budgeting"
            },
            {
                "title": "Emergency Fund Basics",
                "content": "**An emergency fund is your financial safety net:**\n\n- Aim for 3-6 months of expenses\n- Keep it in a separate, easily accessible account\n- Only use for true emergencies (job loss, medical bills, major repairs)\n- Start small - even $500 can help avoid debt\n\nBuilding an emergency fund reduces financial stress and prevents debt!",
                "category": "savings"
            }
        ]
    
    def get_random_tip(self):
        """Get a random financial tip"""
        return random.choice(self.financial_tips)
    
    def analyze_budget(self, transactions_df):
        """Analyze spending patterns and provide advice"""
        if transactions_df.empty:
            return {
                "status": "insufficient_data",
                "message": "Add some transactions to get personalized budget advice!",
                "advice": []
            }
        
        # Calculate monthly totals
        current_month = datetime.now().strftime('%Y-%m')
        monthly_data = transactions_df[transactions_df['date'].str.startswith(current_month)]
        
        if monthly_data.empty:
            return {
                "status": "no_current_month_data",
                "message": "No transactions found for this month. Add some data to get advice!",
                "advice": []
            }
        
        total_income = monthly_data[monthly_data['type'] == 'income']['amount'].sum()
        total_expenses = monthly_data[monthly_data['type'] == 'expense']['amount'].sum()
        
        if total_income == 0:
            return {
                "status": "no_income",
                "message": "Add your income to get comprehensive budget analysis!",
                "advice": []
            }
        
        # Calculate percentages
        expense_ratio = total_expenses / total_income
        remaining_ratio = 1 - expense_ratio
        
        # Analyze by category
        expense_by_category = (monthly_data[monthly_data['type'] == 'expense']
                              .groupby('category')['amount'].sum()
                              .sort_values(ascending=False))
        
        advice = []
        
        # Overall spending analysis
        if expense_ratio > 0.8:
            advice.append({
                "type": "warning",
                "title": "High Spending Alert",
                "message": f"You're spending {expense_ratio:.1%} of your income. Consider reducing expenses to build savings."
            })
        elif expense_ratio > 0.5:
            advice.append({
                "type": "caution",
                "title": "Moderate Spending",
                "message": f"You're spending {expense_ratio:.1%} of your income. You have some room for savings and investments."
            })
        else:
            advice.append({
                "type": "success",
                "title": "Great Spending Control",
                "message": f"Excellent! You're only spending {expense_ratio:.1%} of your income. Keep up the good work!"
            })
        
        # 50/30/20 rule analysis
        if not expense_by_category.empty:
            needs_categories = ['Housing', 'Utilities', 'Food & Dining', 'Healthcare', 'Transportation']
            wants_categories = ['Entertainment', 'Shopping', 'Other']
            
            needs_spending = sum(expense_by_category.get(cat, 0) for cat in needs_categories)
            wants_spending = sum(expense_by_category.get(cat, 0) for cat in wants_categories)
            
            needs_ratio = needs_spending / total_income
            wants_ratio = wants_spending / total_income
            savings_ratio = remaining_ratio
            
            # 50/30/20 rule advice
            rule_advice = {
                "type": "info",
                "title": "50/30/20 Rule Analysis",
                "message": f"""
                **Your Current Split:**
                - Needs: {needs_ratio:.1%} (Target: 50%)
                - Wants: {wants_ratio:.1%} (Target: 30%)
                - Available for Savings: {savings_ratio:.1%} (Target: 20%)
                """
            }
            
            if needs_ratio > 0.5:
                rule_advice["message"] += "\n\n💡 Consider reducing essential expenses or increasing income."
            elif wants_ratio > 0.3:
                rule_advice["message"] += "\n\n💡 Try reducing discretionary spending to free up money for savings."
            elif savings_ratio >= 0.2:
                rule_advice["message"] += "\n\n🎉 Great job! You're meeting the 50/30/20 rule!"
            
            advice.append(rule_advice)
        
        # Category-specific advice
        if not expense_by_category.empty:
            top_category = expense_by_category.index[0]
            top_amount = expense_by_category.iloc[0]
            top_percentage = top_amount / total_income
            
            if top_percentage > 0.3:
                advice.append({
                    "type": "warning",
                    "title": f"High {top_category} Spending",
                    "message": f"Your {top_category.lower()} expenses are {top_percentage:.1%} of your income. Consider ways to reduce this category."
                })
        
        return {
            "status": "success",
            "total_income": total_income,
            "total_expenses": total_expenses,
            "savings_potential": total_income - total_expenses,
            "expense_ratio": expense_ratio,
            "advice": advice
        }
    
    def get_savings_goals_advice(self, monthly_income, current_savings=0):
        """Provide savings goals advice"""
        if monthly_income <= 0:
            return []
        
        goals = []
        
        # Emergency fund goal
        emergency_target = monthly_income * 6
        if current_savings < emergency_target:
            goals.append({
                "title": "Emergency Fund",
                "target": emergency_target,
                "current": current_savings,
                "progress": (current_savings / emergency_target) * 100 if emergency_target > 0 else 0,
                "monthly_needed": max(0, (emergency_target - current_savings) / 12),
                "description": "Build 6 months of expenses for emergencies"
            })
        
        # Retirement savings (assuming 10% of income target)
        retirement_monthly = monthly_income * 0.1
        goals.append({
            "title": "Retirement Savings",
            "target": retirement_monthly * 12,
            "monthly_needed": retirement_monthly,
            "description": "Save 10% of income for retirement"
        })
        
        return goals 