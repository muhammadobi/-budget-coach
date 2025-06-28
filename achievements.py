import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from database import BudgetDatabase

class AchievementSystem:
    def __init__(self, db):
        self.db = db
        self.init_achievements_table()
        self.achievements_catalog = self.define_achievements()
    
    def init_achievements_table(self):
        """Initialize achievements table in database"""
        import sqlite3
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                achievement_id TEXT NOT NULL,
                earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notified BOOLEAN DEFAULT FALSE
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def define_achievements(self):
        """Define all possible achievements"""
        return {
            # First Steps
            "first_transaction": {
                "name": "Getting Started",
                "description": "Add your first transaction",
                "emoji": "🌱",
                "category": "First Steps",
                "points": 10
            },
            "first_week": {
                "name": "Week Warrior",
                "description": "Track expenses for 7 days",
                "emoji": "📅",
                "category": "Consistency",
                "points": 25
            },
            "first_month": {
                "name": "Monthly Master",
                "description": "Track expenses for 30 days",
                "emoji": "📆",
                "category": "Consistency",
                "points": 100
            },
            
            # Savings Achievements
            "first_100": {
                "name": "Century Saver",
                "description": "Save your first $100",
                "emoji": "💯",
                "category": "Savings",
                "points": 50
            },
            "first_1000": {
                "name": "Thousand Club",
                "description": "Save $1,000",
                "emoji": "🥇",
                "category": "Savings",
                "points": 200
            },
            "emergency_fund": {
                "name": "Safety Net",
                "description": "Build 3-month emergency fund",
                "emoji": "🛡️",
                "category": "Savings",
                "points": 500
            },
            
            # Budgeting Achievements
            "budget_follower": {
                "name": "Budget Buddy",
                "description": "Stay under budget for 1 month",
                "emoji": "🎯",
                "category": "Budgeting",
                "points": 75
            },
            "fifty_thirty_twenty": {
                "name": "Rule Master",
                "description": "Follow 50/30/20 rule perfectly",
                "emoji": "⚖️",
                "category": "Budgeting",
                "points": 150
            },
            
            # Transaction Achievements
            "transaction_50": {
                "name": "Data Detective",
                "description": "Log 50 transactions",
                "emoji": "🕵️",
                "category": "Activity",
                "points": 75
            },
            "transaction_100": {
                "name": "Tracking Titan",
                "description": "Log 100 transactions",
                "emoji": "📊",
                "category": "Activity",
                "points": 150
            },
            
            # Special Achievements
            "coffee_conscious": {
                "name": "Coffee Conscious",
                "description": "Reduce coffee spending by 50%",
                "emoji": "☕",
                "category": "Mindful Spending",
                "points": 100
            },
            "goal_crusher": {
                "name": "Goal Crusher",
                "description": "Complete your first savings goal",
                "emoji": "🎯",
                "category": "Goals",
                "points": 200
            },
            "streak_7": {
                "name": "Weekly Warrior",
                "description": "7-day transaction streak",
                "emoji": "🔥",
                "category": "Consistency",
                "points": 50
            },
            "streak_30": {
                "name": "Monthly Legend",
                "description": "30-day transaction streak",
                "emoji": "🌟",
                "category": "Consistency",
                "points": 300
            }
        }
    
    def check_and_award_achievements(self, transactions_df):
        """Check for new achievements and award them"""
        new_achievements = []
        earned_achievements = self.get_earned_achievements()
        
        # First transaction
        if "first_transaction" not in earned_achievements and not transactions_df.empty:
            self.award_achievement("first_transaction")
            new_achievements.append("first_transaction")
        
        # Transaction count achievements
        total_transactions = len(transactions_df)
        if "transaction_50" not in earned_achievements and total_transactions >= 50:
            self.award_achievement("transaction_50")
            new_achievements.append("transaction_50")
        
        if "transaction_100" not in earned_achievements and total_transactions >= 100:
            self.award_achievement("transaction_100")
            new_achievements.append("transaction_100")
        
        # Consistency achievements
        if not transactions_df.empty:
            streak = self.calculate_streak(transactions_df)
            if "streak_7" not in earned_achievements and streak >= 7:
                self.award_achievement("streak_7")
                new_achievements.append("streak_7")
            
            if "streak_30" not in earned_achievements and streak >= 30:
                self.award_achievement("streak_30")
                new_achievements.append("streak_30")
        
        # Savings achievements
        self.check_savings_achievements(transactions_df, earned_achievements, new_achievements)
        
        return new_achievements
    
    def check_savings_achievements(self, transactions_df, earned_achievements, new_achievements):
        """Check savings-related achievements"""
        if transactions_df.empty:
            return
        
        # Calculate total savings
        total_income = transactions_df[transactions_df['type'] == 'income']['amount'].sum()
        total_expenses = transactions_df[transactions_df['type'] == 'expense']['amount'].sum()
        total_savings = total_income - total_expenses
        
        # Savings milestones
        if "first_100" not in earned_achievements and total_savings >= 100:
            self.award_achievement("first_100")
            new_achievements.append("first_100")
        
        if "first_1000" not in earned_achievements and total_savings >= 1000:
            self.award_achievement("first_1000")
            new_achievements.append("first_1000")
        
        # Emergency fund (3 months of expenses)
        monthly_expenses = self.calculate_monthly_expenses(transactions_df)
        if "emergency_fund" not in earned_achievements and total_savings >= (monthly_expenses * 3):
            self.award_achievement("emergency_fund")
            new_achievements.append("emergency_fund")
    
    def calculate_streak(self, transactions_df):
        """Calculate current transaction streak"""
        if transactions_df.empty:
            return 0
        
        # Convert dates and sort
        transactions_df['date'] = pd.to_datetime(transactions_df['date'])
        transactions_df = transactions_df.sort_values('date', ascending=False)
        
        # Get unique dates
        unique_dates = transactions_df['date'].dt.date.unique()
        
        # Calculate streak from today backwards
        today = datetime.now().date()
        streak = 0
        
        for i in range(len(unique_dates)):
            expected_date = today - timedelta(days=i)
            if expected_date in unique_dates:
                streak += 1
            else:
                break
        
        return streak
    
    def calculate_monthly_expenses(self, transactions_df):
        """Calculate average monthly expenses"""
        if transactions_df.empty:
            return 0
        
        expenses = transactions_df[transactions_df['type'] == 'expense']
        if expenses.empty:
            return 0
        
        # Group by month and calculate average
        expenses['date'] = pd.to_datetime(expenses['date'])
        monthly_expenses = expenses.groupby(expenses['date'].dt.to_period('M'))['amount'].sum()
        
        return monthly_expenses.mean() if not monthly_expenses.empty else 0
    
    def award_achievement(self, achievement_id):
        """Award an achievement to the user"""
        import sqlite3
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO user_achievements (achievement_id)
            VALUES (?)
        ''', (achievement_id,))
        
        conn.commit()
        conn.close()
    
    def get_earned_achievements(self):
        """Get list of earned achievement IDs"""
        import sqlite3
        conn = sqlite3.connect(self.db.db_path)
        
        try:
            df = pd.read_sql_query("SELECT achievement_id FROM user_achievements", conn)
            return df['achievement_id'].tolist()
        except:
            return []
        finally:
            conn.close()
    
    def display_achievements(self):
        """Display achievement dashboard"""
        st.subheader("🏆 Your Achievements")
        
        earned_achievements = self.get_earned_achievements()
        total_points = sum(self.achievements_catalog[aid]['points'] for aid in earned_achievements)
        
        # Stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🏆 Earned", len(earned_achievements))
        with col2:
            st.metric("🎯 Available", len(self.achievements_catalog))
        with col3:
            st.metric("⭐ Points", total_points)
        with col4:
            progress = (len(earned_achievements) / len(self.achievements_catalog)) * 100
            st.metric("📊 Progress", f"{progress:.1f}%")
        
        # Achievement cards
        categories = {}
        for aid, achievement in self.achievements_catalog.items():
            category = achievement['category']
            if category not in categories:
                categories[category] = []
            categories[category].append((aid, achievement))
        
        for category, achievements in categories.items():
            with st.expander(f"📋 {category}", expanded=True):
                cols = st.columns(3)
                for i, (aid, achievement) in enumerate(achievements):
                    with cols[i % 3]:
                        is_earned = aid in earned_achievements
                        
                        # Create achievement card
                        card_style = "achievement-badge" if is_earned else "locked-achievement"
                        opacity = "1.0" if is_earned else "0.5"
                        
                        st.markdown(f"""
                        <div style="
                            background: {'linear-gradient(45deg, #00C851, #2196F3)' if is_earned else '#CCCCCC'};
                            color: white;
                            padding: 1rem;
                            border-radius: 15px;
                            text-align: center;
                            margin: 0.5rem 0;
                            opacity: {opacity};
                            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                        ">
                            <div style="font-size: 2rem;">{achievement['emoji']}</div>
                            <div style="font-weight: bold; margin: 0.5rem 0;">{achievement['name']}</div>
                            <div style="font-size: 0.8rem; opacity: 0.9;">{achievement['description']}</div>
                            <div style="font-size: 0.7rem; margin-top: 0.5rem;">⭐ {achievement['points']} points</div>
                        </div>
                        """, unsafe_allow_html=True)
    
    def show_new_achievement_notification(self, achievement_id):
        """Show notification for new achievement"""
        if achievement_id in self.achievements_catalog:
            achievement = self.achievements_catalog[achievement_id]
            
            st.balloons()  # Celebration effect!
            
            st.success(f"""
            🎉 **NEW ACHIEVEMENT UNLOCKED!** 🎉
            
            {achievement['emoji']} **{achievement['name']}**
            
            {achievement['description']}
            
            +{achievement['points']} points earned!
            """)
    
    def get_user_level(self):
        """Calculate user level based on points"""
        earned_achievements = self.get_earned_achievements()
        total_points = sum(self.achievements_catalog[aid]['points'] for aid in earned_achievements)
        
        # Define levels
        levels = [
            (0, "🌱 Beginner", "Just getting started!"),
            (100, "🚀 Rising Star", "Making great progress!"),
            (300, "💪 Money Manager", "You know what you're doing!"),
            (600, "🧠 Financial Guru", "Impressive financial discipline!"),
            (1000, "👑 Budget Master", "You've mastered personal finance!"),
            (1500, "🏆 Legend", "Absolutely incredible achievement!")
        ]
        
        current_level = levels[0]
        for points_required, title, description in levels:
            if total_points >= points_required:
                current_level = (points_required, title, description)
        
        return current_level, total_points 