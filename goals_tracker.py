import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date
from database import BudgetDatabase
import json

class SavingsGoalsTracker:
    def __init__(self, db):
        self.db = db
        self.init_goals_table()
    
    def init_goals_table(self):
        """Initialize the savings goals table in database"""
        conn = self.db.db_path
        import sqlite3
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS savings_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                target_amount REAL NOT NULL,
                current_amount REAL DEFAULT 0,
                target_date TEXT,
                category TEXT DEFAULT 'General',
                emoji TEXT DEFAULT '🎯',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_completed BOOLEAN DEFAULT FALSE
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_goal(self, name, target_amount, target_date, category="General", emoji="🎯"):
        """Add a new savings goal"""
        import sqlite3
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO savings_goals (name, target_amount, target_date, category, emoji)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, target_amount, target_date, category, emoji))
        
        conn.commit()
        conn.close()
    
    def update_goal_progress(self, goal_id, amount_to_add):
        """Add money to a savings goal"""
        import sqlite3
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE savings_goals 
            SET current_amount = current_amount + ?,
                is_completed = CASE 
                    WHEN current_amount + ? >= target_amount THEN TRUE 
                    ELSE FALSE 
                END
            WHERE id = ?
        ''', (amount_to_add, amount_to_add, goal_id))
        
        conn.commit()
        conn.close()
    
    def get_goals(self):
        """Get all savings goals"""
        import sqlite3
        conn = sqlite3.connect(self.db.db_path)
        df = pd.read_sql_query('''
            SELECT * FROM savings_goals 
            ORDER BY is_completed ASC, target_date ASC
        ''', conn)
        conn.close()
        return df
    
    def delete_goal(self, goal_id):
        """Delete a savings goal"""
        import sqlite3
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM savings_goals WHERE id = ?", (goal_id,))
        conn.commit()
        conn.close()
    
    def create_progress_chart(self, goals_df):
        """Create a beautiful progress chart for all goals"""
        if goals_df.empty:
            return None
        
        fig = go.Figure()
        
        for _, goal in goals_df.iterrows():
            progress = (goal['current_amount'] / goal['target_amount']) * 100
            color = '#00C851' if goal['is_completed'] else '#2196F3'
            
            fig.add_trace(go.Bar(
                name=f"{goal['emoji']} {goal['name']}",
                x=[goal['name']],
                y=[progress],
                text=f"${goal['current_amount']:,.0f} / ${goal['target_amount']:,.0f}",
                textposition='auto',
                marker_color=color,
                hovertemplate=f"<b>{goal['name']}</b><br>" +
                             f"Progress: {progress:.1f}%<br>" +
                             f"Current: ${goal['current_amount']:,.2f}<br>" +
                             f"Target: ${goal['target_amount']:,.2f}<br>" +
                             f"Remaining: ${goal['target_amount'] - goal['current_amount']:,.2f}<extra></extra>"
            ))
        
        fig.update_layout(
            title="🎯 Savings Goals Progress",
            xaxis_title="Goals",
            yaxis_title="Progress (%)",
            yaxis=dict(range=[0, 100]),
            showlegend=False,
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_goal_cards(self, goals_df):
        """Create beautiful cards for each goal"""
        if goals_df.empty:
            st.info("🎯 No savings goals yet! Create your first goal to start saving with purpose.")
            return
        
        for _, goal in goals_df.iterrows():
            progress = (goal['current_amount'] / goal['target_amount']) * 100
            days_left = self.calculate_days_left(goal['target_date'])
            
            # Create card container
            with st.container():
                col1, col2, col3, col4 = st.columns([1, 3, 2, 1])
                
                with col1:
                    st.markdown(f"<div style='font-size: 3rem; text-align: center;'>{goal['emoji']}</div>", 
                               unsafe_allow_html=True)
                
                with col2:
                    status = "🎉 COMPLETED!" if goal['is_completed'] else f"📅 {days_left}"
                    st.markdown(f"**{goal['name']}**")
                    st.markdown(f"*{goal['category']} • {status}*")
                    
                    # Progress bar
                    st.progress(min(progress / 100, 1.0))
                    st.markdown(f"${goal['current_amount']:,.0f} / ${goal['target_amount']:,.0f} ({progress:.1f}%)")
                
                with col3:
                    remaining = goal['target_amount'] - goal['current_amount']
                    if not goal['is_completed']:
                        st.markdown(f"**${remaining:,.0f}** to go!")
                        
                        # Quick add buttons
                        quick_amounts = [10, 25, 50, 100]
                        cols = st.columns(len(quick_amounts))
                        for i, amount in enumerate(quick_amounts):
                            if cols[i].button(f"+${amount}", key=f"add_{goal['id']}_{amount}"):
                                self.update_goal_progress(goal['id'], amount)
                                st.rerun()
                    else:
                        st.success("🎉 Goal Achieved!")
                
                with col4:
                    if st.button("🗑️", key=f"delete_goal_{goal['id']}", help="Delete goal"):
                        self.delete_goal(goal['id'])
                        st.rerun()
                
                st.markdown("---")
    
    def calculate_days_left(self, target_date_str):
        """Calculate days remaining until target date"""
        try:
            target_date = datetime.strptime(target_date_str, '%Y-%m-%d').date()
            today = date.today()
            days_left = (target_date - today).days
            
            if days_left < 0:
                return "⏰ Overdue"
            elif days_left == 0:
                return "🎯 Today!"
            elif days_left == 1:
                return "📅 Tomorrow"
            else:
                return f"📅 {days_left} days left"
        except:
            return "📅 No deadline"
    
    def create_goal_form(self):
        """Create form to add new savings goal"""
        st.subheader("🎯 Create New Savings Goal")
        
        col1, col2 = st.columns(2)
        
        with col1:
            goal_name = st.text_input("Goal Name", placeholder="e.g., Vacation to Hawaii")
            target_amount = st.number_input("Target Amount ($)", min_value=1.0, step=50.0, format="%.2f")
            
        with col2:
            target_date = st.date_input("Target Date", value=date.today())
            
            # Predefined categories with emojis
            goal_categories = {
                "🏖️ Vacation": "🏖️",
                "🏠 Emergency Fund": "🏠", 
                "🚗 Transportation": "🚗",
                "💍 Special Purchase": "💍",
                "🎓 Education": "🎓",
                "💰 Investment": "💰",
                "🎁 Gift": "🎁",
                "🏥 Healthcare": "🏥",
                "🎯 Other": "🎯"
            }
            
            selected_category = st.selectbox("Category", list(goal_categories.keys()))
            emoji = goal_categories[selected_category]
        
        if st.button("🚀 Create Goal", type="primary"):
            if goal_name and target_amount > 0:
                try:
                    self.add_goal(
                        name=goal_name,
                        target_amount=target_amount,
                        target_date=target_date.strftime('%Y-%m-%d'),
                        category=selected_category,
                        emoji=emoji
                    )
                    st.success(f"🎉 Created goal: {emoji} {goal_name}")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error creating goal: {str(e)}")
            else:
                st.error("Please fill in all required fields.")
    
    def show_goal_stats(self, goals_df):
        """Show statistics about goals"""
        if goals_df.empty:
            return
        
        total_goals = len(goals_df)
        completed_goals = len(goals_df[goals_df['is_completed'] == True])
        total_target = goals_df['target_amount'].sum()
        total_saved = goals_df['current_amount'].sum()
        overall_progress = (total_saved / total_target) * 100 if total_target > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🎯 Total Goals", total_goals)
        with col2:
            st.metric("✅ Completed", completed_goals, delta=f"{(completed_goals/total_goals)*100:.0f}%")
        with col3:
            st.metric("💰 Total Saved", f"${total_saved:,.0f}")
        with col4:
            st.metric("📊 Overall Progress", f"{overall_progress:.1f}%") 