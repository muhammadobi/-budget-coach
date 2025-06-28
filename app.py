import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import plotly.express as px
import plotly.graph_objects as go
from database import BudgetDatabase
from financial_advisor import FinancialAdvisor
from visualizations import BudgetVisualizer
from themes import ThemeManager
from goals_tracker import SavingsGoalsTracker
from achievements import AchievementSystem
from calculators import FinancialCalculators
from auth import AuthManager

# Page configuration
st.set_page_config(
    page_title="💰 Budget Coach",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize authentication
auth_manager = AuthManager()

# Check authentication first
if not auth_manager.is_authenticated():
    # Show login form if not authenticated
    auth_manager.login_form()
    st.stop()

# Track page visit for analytics
auth_manager.track_page_visit()

# Show welcome message for new users
auth_manager.show_user_welcome()

# Initialize classes
@st.cache_resource
def init_app():
    db = BudgetDatabase()
    advisor = FinancialAdvisor()
    visualizer = BudgetVisualizer()
    theme_manager = ThemeManager()
    return db, advisor, visualizer, theme_manager

db, advisor, visualizer, theme_manager = init_app()

# Initialize non-cached components
goals_tracker = SavingsGoalsTracker(db)
achievement_system = AchievementSystem(db)
calculators = FinancialCalculators()

# Apply theme and dynamic CSS
current_theme = theme_manager.create_theme_toggle()
st.markdown(theme_manager.get_theme_css(current_theme), unsafe_allow_html=True)

# Add name in upper right corner with CSS positioning
st.markdown("""
<div style="
    position: fixed;
    top: 60px;
    right: 20px;
    z-index: 999;
    background: rgba(255, 255, 255, 0.98);
    backdrop-filter: blur(15px);
    border-radius: 30px;
    padding: 10px 20px;
    border: 2px solid #6366F1;
    box-shadow: 0 8px 32px rgba(99, 102, 241, 0.2);
    font-size: 15px;
    font-weight: 600;
    color: #6366F1;
    animation: nameGlow 3s ease-in-out infinite alternate;
    font-family: 'Inter', sans-serif;
">
    👤 K.Muhammad Obi
</div>

<style>
@keyframes nameGlow {
    from { 
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.2);
        transform: scale(1);
    }
    to { 
        box-shadow: 0 12px 40px rgba(139, 92, 246, 0.3);
        transform: scale(1.02);
    }
}

/* Dark theme adjustments */
.stApp[data-theme="dark"] div[style*="K.Muhammad Obi"] {
    background: rgba(30, 30, 30, 0.95) !important;
    color: #8B5CF6 !important;
    border: 2px solid #7C3AED !important;
}
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🧭 Navigation")

# User info and logout
current_user = auth_manager.get_current_user()
st.sidebar.markdown(f"**Welcome, {current_user['name']}!** 👋")
st.sidebar.markdown(f"📧 {current_user['email']}")

if st.sidebar.button("🚪 Logout"):
    auth_manager.logout()

st.sidebar.markdown("---")

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = "📊 Dashboard"

pages = ["📊 Dashboard", "➕ Add Transaction", "📈 Analytics", "💰 Budget Targets", 
         "🎯 Savings Goals", "🏆 Achievements", "🧮 Calculators", "🎓 Financial Tips", "⚙️ Settings"]

page = st.sidebar.selectbox(
    "Choose a page:",
    pages,
    index=pages.index(st.session_state.page) if st.session_state.page in pages else 0
)

# Update session state when page is manually selected
st.session_state.page = page

# Check for new achievements and display user level
transactions_df_for_achievements = db.get_transactions()
new_achievements = achievement_system.check_and_award_achievements(transactions_df_for_achievements)

# Show new achievement notifications
for achievement_id in new_achievements:
    achievement_system.show_new_achievement_notification(achievement_id)

# Show notifications
notifications = auth_manager.show_notifications()
for notification in notifications:
    if notification['type'] == 'success':
        st.success(notification['message'])
    elif notification['type'] == 'info':
        st.info(notification['message'])
    elif notification['type'] == 'warning':
        st.warning(notification['message'])
    elif notification['type'] == 'error':
        st.error(notification['message'])

# Display user level in sidebar
level_info, total_points = achievement_system.get_user_level()
st.sidebar.markdown("---")
st.sidebar.markdown(f"**{level_info[1]}**")
st.sidebar.markdown(f"⭐ {total_points} points")
st.sidebar.progress(min(total_points / 1500, 1.0))  # Progress to max level

# Add month/year filter to sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("📅 Date Filter")
filter_type = st.sidebar.selectbox("Filter by:", ["Current Month", "Specific Month", "All Time"])

filter_start_date = None
filter_end_date = None

if filter_type == "Specific Month":
    selected_date = st.sidebar.date_input("Select Month", value=date.today())
    filter_start_date = selected_date.replace(day=1).strftime('%Y-%m-%d')
    # Last day of the month
    if selected_date.month == 12:
        next_month = selected_date.replace(year=selected_date.year + 1, month=1, day=1)
    else:
        next_month = selected_date.replace(month=selected_date.month + 1, day=1)
    filter_end_date = (next_month - timedelta(days=1)).strftime('%Y-%m-%d')
elif filter_type == "Current Month":
    current_month_start = datetime.now().replace(day=1)
    filter_start_date = current_month_start.strftime('%Y-%m-%d')
    filter_end_date = datetime.now().strftime('%Y-%m-%d')

# Sample data option in sidebar
st.sidebar.markdown("---")
if st.sidebar.button("🎯 Load Sample Data"):
    try:
        from sample_data import create_sample_data
        count = create_sample_data()
        st.sidebar.success(f"✅ Added {count} sample transactions!")
        st.rerun()
    except Exception as e:
        st.sidebar.error(f"❌ Error loading sample data: {str(e)}")

# Show contact information
auth_manager.show_contact_info()

# Main content based on selected page
if page == "📊 Dashboard":
    st.markdown('<h1 class="main-header">💰 Budget Coach Dashboard</h1>', unsafe_allow_html=True)
    
    # Get transactions with date filtering
    transactions_df = db.get_transactions(filter_start_date, filter_end_date)
    
    if not transactions_df.empty:
        # Current month analysis
        current_month = datetime.now().strftime('%Y-%m')
        monthly_data = transactions_df[transactions_df['date'].str.startswith(current_month)]
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        if not monthly_data.empty:
            total_income = monthly_data[monthly_data['type'] == 'income']['amount'].sum()
            total_expenses = monthly_data[monthly_data['type'] == 'expense']['amount'].sum()
            net_savings = total_income - total_expenses
            transactions_count = len(monthly_data)
        else:
            total_income = total_expenses = net_savings = transactions_count = 0
        
        with col1:
            st.metric("💵 Monthly Income", f"${total_income:,.2f}")
        with col2:
            st.metric("💸 Monthly Expenses", f"${total_expenses:,.2f}")
        with col3:
            st.metric("💰 Net Savings", f"${net_savings:,.2f}", delta=f"{net_savings:,.2f}")
        with col4:
            st.metric("📝 Transactions", transactions_count)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Spending by category pie chart
            pie_chart = visualizer.create_spending_by_category_pie(monthly_data)
            if pie_chart:
                st.plotly_chart(pie_chart, use_container_width=True)
        
        with col2:
            # Monthly trends
            trend_chart = visualizer.create_monthly_trend(transactions_df)
            if trend_chart:
                st.plotly_chart(trend_chart, use_container_width=True)
        
        # Recent transactions
        st.subheader("📋 Recent Transactions")
        recent_transactions = transactions_df.head(10)
        
        if not recent_transactions.empty:
            # Format the dataframe for display
            display_df = recent_transactions.copy()
            display_df['amount'] = display_df['amount'].apply(lambda x: f"${x:,.2f}")
            display_df = display_df[['date', 'description', 'category', 'type', 'amount']]
            
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No transactions yet. Add your first transaction to get started!")
    
    else:
        st.info("🚀 Welcome to Budget Coach! Start by adding your first transaction.")
        if st.button("➕ Add First Transaction"):
            st.session_state.page = "➕ Add Transaction"
            st.rerun()

elif page == "➕ Add Transaction":
    st.markdown('<h1 class="main-header">➕ Add New Transaction</h1>', unsafe_allow_html=True)
    
    # Transaction form
    col1, col2 = st.columns(2)
    
    with col1:
        transaction_type = st.selectbox("Transaction Type", ["expense", "income"])
        
        # Get categories based on type
        categories_df = db.get_categories(transaction_type)
        category_options = categories_df['name'].tolist() if not categories_df.empty else []
        
        category = st.selectbox("Category", category_options)
        amount = st.number_input("Amount ($)", min_value=0.01, step=0.01, format="%.2f")
    
    with col2:
        transaction_date = st.date_input("Date", value=date.today())
        description = st.text_input("Description", placeholder="Enter transaction description...")
        
        # Add transaction button
        if st.button("💾 Add Transaction", type="primary"):
            if description and amount > 0:
                try:
                    db.add_transaction(
                        date=transaction_date.strftime('%Y-%m-%d'),
                        description=description,
                        amount=amount,
                        category=category,
                        transaction_type=transaction_type
                    )
                    st.success(f"✅ Successfully added {transaction_type}: ${amount:.2f}")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error adding transaction: {str(e)}")
            else:
                st.error("Please fill in all required fields.")
    
    # Quick add buttons for common transactions
    st.subheader("🚀 Quick Add")
    col1, col2, col3, col4 = st.columns(4)
    
    quick_transactions = [
        ("☕ Coffee", "Food & Dining", 5.00),
        ("⛽ Gas", "Transportation", 40.00),
        ("🛒 Groceries", "Food & Dining", 75.00),
        ("💡 Utilities", "Utilities", 100.00)
    ]
    
    for i, (desc, cat, amt) in enumerate(quick_transactions):
        with [col1, col2, col3, col4][i]:
            if st.button(f"{desc}\n${amt:.2f}", key=f"quick_{i}"):
                try:
                    db.add_transaction(
                        date=date.today().strftime('%Y-%m-%d'),
                        description=desc.split(' ', 1)[1],
                        amount=amt,
                        category=cat,
                        transaction_type="expense"
                    )
                    st.success(f"✅ Added {desc}")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

elif page == "🎯 Savings Goals":
    st.markdown('<h1 class="main-header">🎯 Savings Goals Tracker</h1>', unsafe_allow_html=True)
    
    # Display goal statistics
    goals_df = goals_tracker.get_goals()
    goals_tracker.show_goal_stats(goals_df)
    
    # Progress chart
    if not goals_df.empty:
        progress_chart = goals_tracker.create_progress_chart(goals_df)
        if progress_chart:
            st.plotly_chart(progress_chart, use_container_width=True)
    
    # Create new goal form
    goals_tracker.create_goal_form()
    
    st.markdown("---")
    
    # Display goal cards
    st.subheader("📋 Your Goals")
    goals_tracker.create_goal_cards(goals_df)

elif page == "🏆 Achievements":
    st.markdown('<h1 class="main-header">🏆 Achievement Center</h1>', unsafe_allow_html=True)
    
    # Display user level prominently
    level_info, total_points = achievement_system.get_user_level()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style="
            background: linear-gradient(45deg, #00C851, #2196F3);
            color: white;
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            margin: 1rem 0;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem;">👑</div>
            <div style="font-size: 1.5rem; font-weight: bold;">{level_info[1]}</div>
            <div style="font-size: 1rem; margin-top: 0.5rem;">⭐ {total_points} points earned</div>
            <div style="font-size: 0.9rem; opacity: 0.9; margin-top: 0.5rem;">{level_info[2]}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display achievements
    achievement_system.display_achievements()

elif page == "🧮 Calculators":
    st.markdown('<h1 class="main-header">🧮 Financial Calculators</h1>', unsafe_allow_html=True)
    
    # Calculator selector
    calculator_type = st.selectbox(
        "Choose a Calculator:",
        ["🏠 Mortgage Calculator", "🏖️ Retirement Planner", "🚗 Loan Calculator", 
         "🛡️ Emergency Fund", "💳 Debt Payoff"]
    )
    
    st.markdown("---")
    
    if calculator_type == "🏠 Mortgage Calculator":
        calculators.mortgage_calculator()
    elif calculator_type == "🏖️ Retirement Planner":
        calculators.retirement_calculator()
    elif calculator_type == "🚗 Loan Calculator":
        calculators.loan_calculator()
    elif calculator_type == "🛡️ Emergency Fund":
        calculators.emergency_fund_calculator()
    elif calculator_type == "💳 Debt Payoff":
        calculators.debt_payoff_calculator()

elif page == "💰 Budget Targets":
    st.markdown('<h1 class="main-header">💰 Budget Targets</h1>', unsafe_allow_html=True)
    
    # Budget targets management
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Set Budget Targets")
        
        # Get expense categories for budget setting
        expense_categories = db.get_categories('expense')
        
        if not expense_categories.empty:
            category = st.selectbox("Category", expense_categories['name'].tolist())
            monthly_target = st.number_input("Monthly Target ($)", min_value=0.01, step=10.00, format="%.2f")
            
            if st.button("💾 Set Budget Target", type="primary"):
                try:
                    db.set_budget_target(category, monthly_target)
                    st.success(f"✅ Set budget target for {category}: ${monthly_target:.2f}")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error setting budget target: {str(e)}")
    
    with col2:
        st.subheader("📊 Current Budget Targets")
        
        budget_targets = db.get_budget_targets()
        
        if not budget_targets.empty:
            for _, target in budget_targets.iterrows():
                col_a, col_b, col_c = st.columns([3, 2, 1])
                
                with col_a:
                    st.write(f"**{target['category']}**")
                with col_b:
                    st.write(f"${target['monthly_target']:,.2f}")
                with col_c:
                    if st.button("🗑️", key=f"delete_target_{target['id']}", help="Delete budget target"):
                        db.delete_budget_target(target['category'])
                        st.rerun()
        else:
            st.info("No budget targets set yet. Create your first budget target!")
    
    # Budget vs Actual Chart
    if not budget_targets.empty:
        st.subheader("📈 Budget vs Actual Spending")
        transactions_df = db.get_transactions(filter_start_date, filter_end_date)
        
        budget_chart = visualizer.create_budget_vs_actual(transactions_df, budget_targets)
        if budget_chart:
            st.plotly_chart(budget_chart, use_container_width=True)
        else:
            st.info("Add some expense transactions to see budget comparison.")

elif page == "📈 Analytics":
    st.markdown('<h1 class="main-header">📈 Financial Analytics</h1>', unsafe_allow_html=True)
    
    transactions_df = db.get_transactions(filter_start_date, filter_end_date)
    
    # Show current filter info
    if filter_type != "All Time":
        st.info(f"📅 Showing data for: **{filter_type}**")
    
    if not transactions_df.empty:
        # Get financial advice
        budget_analysis = advisor.analyze_budget(transactions_df)
        
        if budget_analysis['status'] == 'success':
            # Display advice cards
            st.subheader("🎯 Your Financial Advice")
            
            for advice in budget_analysis['advice']:
                if advice['type'] == 'success':
                    st.success(f"**{advice['title']}**: {advice['message']}")
                elif advice['type'] == 'warning':
                    st.warning(f"**{advice['title']}**: {advice['message']}")
                elif advice['type'] == 'caution':
                    st.info(f"**{advice['title']}**: {advice['message']}")
                else:
                    st.info(f"**{advice['title']}**: {advice['message']}")
            
            # 50/30/20 Analysis
            st.subheader("📊 50/30/20 Rule Analysis")
            
            current_month = datetime.now().strftime('%Y-%m')
            monthly_data = transactions_df[transactions_df['date'].str.startswith(current_month)]
            
            if not monthly_data.empty:
                total_income = monthly_data[monthly_data['type'] == 'income']['amount'].sum()
                
                if total_income > 0:
                    expense_by_category = monthly_data[monthly_data['type'] == 'expense'].groupby('category')['amount'].sum()
                    
                    needs_categories = ['Housing', 'Utilities', 'Food & Dining', 'Healthcare', 'Transportation']
                    wants_categories = ['Entertainment', 'Shopping', 'Other']
                    
                    needs_spending = sum(expense_by_category.get(cat, 0) for cat in needs_categories)
                    wants_spending = sum(expense_by_category.get(cat, 0) for cat in wants_categories)
                    
                    # Create 50/30/20 gauge chart
                    gauge_chart = visualizer.create_50_30_20_gauge(total_income, needs_spending, wants_spending)
                    if gauge_chart:
                        st.plotly_chart(gauge_chart, use_container_width=True)
        
        # Additional charts
        col1, col2 = st.columns(2)
        
        with col1:
            daily_chart = visualizer.create_daily_spending_bar(transactions_df)
            if daily_chart:
                st.plotly_chart(daily_chart, use_container_width=True)
        
        with col2:
            income_chart = visualizer.create_income_breakdown(transactions_df)
            if income_chart:
                st.plotly_chart(income_chart, use_container_width=True)
    
    else:
        st.info("📊 Add some transactions to see your analytics!")

elif page == "🎓 Financial Tips":
    st.markdown('<h1 class="main-header">🎓 Financial Education</h1>', unsafe_allow_html=True)
    
    # Get a random tip
    tip = advisor.get_random_tip()
    
    st.markdown(f"""
    <div class="tip-card">
        <h2>💡 {tip['title']}</h2>
        {tip['content']}
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Get Another Tip"):
        st.rerun()
    
    # Educational sections
    st.subheader("📚 Quick Financial Concepts")
    
    with st.expander("💰 What is the 50/30/20 Rule?"):
        st.write("""
        The 50/30/20 rule is a simple budgeting framework:
        - **50% for Needs**: Essential expenses like housing, food, utilities
        - **30% for Wants**: Entertainment, dining out, hobbies
        - **20% for Savings & Debt**: Emergency fund, retirement, extra debt payments
        
        This rule helps ensure you're covering essentials while building wealth!
        """)
    
    with st.expander("🏦 Building an Emergency Fund"):
        st.write("""
        An emergency fund is crucial for financial security:
        - Aim for 3-6 months of living expenses
        - Keep it in a separate, easily accessible savings account
        - Only use for true emergencies (job loss, medical bills, major repairs)
        - Start small - even $500 can prevent debt from small emergencies
        """)
    
    with st.expander("📈 The Power of Compound Interest"):
        st.write("""
        Compound interest is earning interest on your interest:
        - Your money grows exponentially over time
        - Starting early is more important than investing large amounts
        - Even small amounts compound significantly over decades
        - Example: $100/month for 30 years at 7% return = $121,997!
        """)

elif page == "⚙️ Settings":
    st.markdown('<h1 class="main-header">⚙️ Settings & Data Management</h1>', unsafe_allow_html=True)
    
    # User Analytics (for creator)
    if current_user['email'] == "muhammadkarangwa07@gmail.com":
        st.subheader("📊 User Analytics Dashboard")
        
        user_stats = db.get_user_stats()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("👥 Total Users", user_stats['total_users'])
        with col2:
            st.metric("🔥 Active Users (30 days)", user_stats['active_users'])
        with col3:
            st.metric("📱 Total Sessions", user_stats['total_sessions'])
        
        st.info("💡 This analytics dashboard is only visible to the app creator.")
        st.markdown("---")
    
    # Data Export/Import
    st.subheader("📂 Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Export Data**")
        if st.button("📥 Export to CSV"):
            try:
                export_path = f"budget_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                count = db.export_to_csv(export_path)
                st.success(f"✅ Exported {count} transactions to {export_path}")
            except Exception as e:
                st.error(f"❌ Export failed: {str(e)}")
    
    with col2:
        st.write("**Import Data**")
        uploaded_file = st.file_uploader("Choose CSV file", type="csv")
        if uploaded_file is not None:
            try:
                # Save uploaded file temporarily
                import_path = f"temp_import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                with open(import_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                
                count = db.import_from_csv(import_path)
                st.success(f"✅ Imported {count} transactions")
                
                # Clean up temp file
                import os
                os.remove(import_path)
                
            except Exception as e:
                st.error(f"❌ Import failed: {str(e)}")
    
    # Transaction Management
    st.subheader("📋 Transaction Management")
    
    transactions_df = db.get_transactions(filter_start_date, filter_end_date)
    if not transactions_df.empty:
        st.write("**Recent Transactions**")
        
        # Display transactions with delete option
        for idx, row in transactions_df.head(20).iterrows():
            col1, col2, col3, col4, col5, col6 = st.columns([2, 3, 2, 2, 2, 1])
            
            with col1:
                st.write(row['date'])
            with col2:
                st.write(row['description'])
            with col3:
                st.write(row['category'])
            with col4:
                st.write(row['type'].title())
            with col5:
                st.write(f"${row['amount']:,.2f}")
            with col6:
                if st.button("🗑️", key=f"delete_{row['id']}", help="Delete transaction"):
                    db.delete_transaction(row['id'])
                    st.success("Transaction deleted!")
                    st.rerun()
    
    # App Info
    st.subheader("ℹ️ About Budget Coach")
    st.info("""
    **Budget Coach v1.0**
    
    A simple, educational budgeting app designed to help you:
    - Track income and expenses
    - Understand the 50/30/20 budgeting rule
    - Learn fundamental financial concepts
    - Build healthy money habits
    
    Built with ❤️ using Streamlit, SQLite, and Plotly.
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>💰 Budget Coach - Your Personal Financial Literacy Assistant</div>",
    unsafe_allow_html=True
) 