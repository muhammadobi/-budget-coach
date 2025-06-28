import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import sqlite3
import re
import os
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("⚠️ Plotly not available - using basic charts")

# Page configuration
st.set_page_config(
    page_title="💰 Budget Coach",
    page_icon="💰",
    layout="wide",
)

# Simple authentication
def login_form():
    st.markdown("### 🚀 Welcome to Budget Coach!")
    st.markdown("Enter your email to get started:")
    
    email = st.text_input("Email Address", placeholder="your.email@example.com")
    name = st.text_input("Your Name (Optional)", placeholder="John Doe")
    
    if st.button("Get Started"):
        if email and "@" in email:
            st.session_state.authenticated = True
            st.session_state.user_email = email
            st.session_state.user_name = name if name else email.split('@')[0]
            st.rerun()
        else:
            st.error("Please enter a valid email address")

# Check authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    login_form()
    st.stop()

# Database setup with better error handling for deployment
@st.cache_resource
def init_database():
    try:
        # Use a more deployment-friendly database path
        db_path = os.getenv('DATABASE_PATH', 'budget_coach.db')
        conn = sqlite3.connect(db_path, check_same_thread=False)
        cursor = conn.cursor()
        
        # Create transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                type TEXT NOT NULL
            )
        ''')
        
        # Create categories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                name TEXT PRIMARY KEY,
                type TEXT NOT NULL
            )
        ''')
        
        # Default categories
        categories = [
            ('Housing', 'expense'), ('Transportation', 'expense'), ('Food & Dining', 'expense'),
            ('Entertainment', 'expense'), ('Shopping', 'expense'), ('Healthcare', 'expense'),
            ('Utilities', 'expense'), ('Other', 'expense'), ('Salary', 'income'), 
            ('Freelance', 'income'), ('Investment', 'income'), ('Other Income', 'income')
        ]
        
        for name, cat_type in categories:
            cursor.execute('INSERT OR IGNORE INTO categories VALUES (?, ?)', (name, cat_type))
        
        conn.commit()
        return conn
    except Exception as e:
        st.error(f"Database initialization failed: {str(e)}")
        # Fallback to in-memory database
        conn = sqlite3.connect(':memory:', check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                type TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE categories (
                name TEXT PRIMARY KEY,
                type TEXT NOT NULL
            )
        ''')
        
        categories = [
            ('Housing', 'expense'), ('Transportation', 'expense'), ('Food & Dining', 'expense'),
            ('Entertainment', 'expense'), ('Shopping', 'expense'), ('Healthcare', 'expense'),
            ('Utilities', 'expense'), ('Other', 'expense'), ('Salary', 'income'), 
            ('Freelance', 'income'), ('Investment', 'income'), ('Other Income', 'income')
        ]
        
        for name, cat_type in categories:
            cursor.execute('INSERT INTO categories VALUES (?, ?)', (name, cat_type))
        
        conn.commit()
        st.warning("⚠️ Using temporary database - data will not persist between sessions")
        return conn

db = init_database()

# Header with your name
st.markdown("""
<div style="position: fixed; top: 60px; right: 20px; z-index: 999;
    background: rgba(255, 255, 255, 0.98); border-radius: 20px; padding: 8px 16px;
    border: 2px solid #6366F1; font-weight: bold; color: #6366F1;">
    👤 K.Muhammad Obi
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🧭 Budget Coach")
st.sidebar.markdown(f"**Welcome, {st.session_state.user_name}!** 👋")

if st.sidebar.button("🚪 Logout"):
    st.session_state.authenticated = False
    st.rerun()

st.sidebar.markdown("---")

# Contact info
st.sidebar.markdown("""
### 👨‍💻 **Created by K.Muhammad Obi**

📧 **Email**: [muhammadkarangwa07@gmail.com](mailto:muhammadkarangwa07@gmail.com)

📱 **Instagram**: [@obi_karangwa](https://instagram.com/obi_karangwa)

---

💡 **Love Budget Coach?** Share it with friends! 🚀
""")

# Main navigation
page = st.sidebar.selectbox("Choose a page:", ["📊 Dashboard", "➕ Add Transaction", "📈 Analytics"])

# Helper functions
def add_transaction(date, description, amount, category, transaction_type):
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO transactions (date, description, amount, category, type)
        VALUES (?, ?, ?, ?, ?)
    ''', (date, description, amount, category, transaction_type))
    db.commit()

def get_transactions():
    return pd.read_sql_query("SELECT * FROM transactions ORDER BY date DESC", db)

# Page content
if page == "📊 Dashboard":
    st.title("💰 Budget Coach Dashboard")
    
    transactions_df = get_transactions()
    
    if not transactions_df.empty:
        # Current month analysis
        current_month = datetime.now().strftime('%Y-%m')
        monthly_data = transactions_df[transactions_df['date'].str.startswith(current_month)]
        
        if not monthly_data.empty:
            total_income = monthly_data[monthly_data['type'] == 'income']['amount'].sum()
            total_expenses = monthly_data[monthly_data['type'] == 'expense']['amount'].sum()
            net_savings = total_income - total_expenses
        else:
            total_income = total_expenses = net_savings = 0
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💵 Monthly Income", f"${total_income:,.2f}")
        with col2:
            st.metric("💸 Monthly Expenses", f"${total_expenses:,.2f}")
        with col3:
            st.metric("💰 Net Savings", f"${net_savings:,.2f}")
        
        # Recent transactions
        st.subheader("📋 Recent Transactions")
        display_df = transactions_df.head(10).copy()
        display_df['amount'] = display_df['amount'].apply(lambda x: f"${x:,.2f}")
        st.dataframe(display_df[['date', 'description', 'category', 'type', 'amount']], use_container_width=True)
        
        # Simple chart
        if not monthly_data.empty:
            expense_data = monthly_data[monthly_data['type'] == 'expense']
            if not expense_data.empty:
                spending_by_category = expense_data.groupby('category')['amount'].sum()
                st.subheader("💸 Spending by Category")
                st.bar_chart(spending_by_category)
    
    else:
        st.info("🚀 Welcome to Budget Coach! Start by adding your first transaction.")

elif page == "➕ Add Transaction":
    st.title("➕ Add New Transaction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        transaction_type = st.selectbox("Transaction Type", ["expense", "income"])
        
        # Get categories
        categories_df = pd.read_sql_query(f"SELECT name FROM categories WHERE type = '{transaction_type}'", db)
        category_options = categories_df['name'].tolist()
        
        category = st.selectbox("Category", category_options)
        amount = st.number_input("Amount ($)", min_value=0.01, step=0.01)
    
    with col2:
        transaction_date = st.date_input("Date", value=date.today())
        description = st.text_input("Description", placeholder="Enter description...")
        
        if st.button("💾 Add Transaction", type="primary"):
            if description and amount > 0:
                add_transaction(
                    transaction_date.strftime('%Y-%m-%d'),
                    description,
                    amount,
                    category,
                    transaction_type
                )
                st.success(f"✅ Added {transaction_type}: ${amount:.2f}")
                st.rerun()

elif page == "📈 Analytics":
    st.title("📈 Financial Analytics")
    
    transactions_df = get_transactions()
    
    if not transactions_df.empty:
        # Spending vs Income over time
        transactions_df['date'] = pd.to_datetime(transactions_df['date'])
        transactions_df['month'] = transactions_df['date'].dt.to_period('M')
        
        monthly_summary = transactions_df.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0)
        
        if not monthly_summary.empty:
            st.subheader("📊 Monthly Income vs Expenses")
            if PLOTLY_AVAILABLE:
                # Create a better line chart with Plotly
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=monthly_summary.index.astype(str),
                    y=monthly_summary.get('income', [0]*len(monthly_summary)),
                    mode='lines+markers',
                    name='Income',
                    line=dict(color='#22c55e', width=3)
                ))
                fig.add_trace(go.Scatter(
                    x=monthly_summary.index.astype(str),
                    y=monthly_summary.get('expense', [0]*len(monthly_summary)),
                    mode='lines+markers',
                    name='Expenses',
                    line=dict(color='#ef4444', width=3)
                ))
                fig.update_layout(
                    title="Monthly Income vs Expenses",
                    xaxis_title="Month",
                    yaxis_title="Amount ($)",
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.line_chart(monthly_summary)
        
        # Category breakdown
        expense_data = transactions_df[transactions_df['type'] == 'expense']
        income_data = transactions_df[transactions_df['type'] == 'income']
        
        col1, col2 = st.columns(2)
        
        with col1:
            if not expense_data.empty:
                st.subheader("💸 Expenses by Category")
                expense_by_cat = expense_data.groupby('category')['amount'].sum()
                if PLOTLY_AVAILABLE:
                    fig = px.pie(
                        values=expense_by_cat.values,
                        names=expense_by_cat.index,
                        title="Expenses by Category"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.bar_chart(expense_by_cat)
        
        with col2:
            if not income_data.empty:
                st.subheader("💰 Income Sources")
                income_by_cat = income_data.groupby('category')['amount'].sum()
                if PLOTLY_AVAILABLE:
                    fig = px.bar(
                        x=income_by_cat.index,
                        y=income_by_cat.values,
                        title="Income by Source",
                        color=income_by_cat.values,
                        color_continuous_scale='Greens'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.bar_chart(income_by_cat)
    
    else:
        st.info("📊 Add some transactions to see your analytics!")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>💰 Budget Coach - Your Personal Financial Assistant</div>", unsafe_allow_html=True) 