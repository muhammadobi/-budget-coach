import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta

class BudgetVisualizer:
    def __init__(self):
        self.color_palette = {
            'income': '#2E8B57',
            'expense': '#DC143C',
            'savings': '#4169E1'
        }
    
    def create_spending_by_category_pie(self, transactions_df):
        """Create a pie chart showing spending by category"""
        if transactions_df.empty:
            return None
        
        expense_data = transactions_df[transactions_df['type'] == 'expense']
        if expense_data.empty:
            return None
        
        category_totals = expense_data.groupby('category')['amount'].sum().reset_index()
        category_totals = category_totals.sort_values('amount', ascending=False)
        
        fig = px.pie(
            category_totals, 
            values='amount', 
            names='category',
            title='Spending by Category',
            hole=0.3
        )
        
        fig.update_layout(
            showlegend=True,
            height=400,
            font=dict(size=12)
        )
        
        return fig
    
    def create_monthly_trend(self, transactions_df):
        """Create a line chart showing monthly income vs expenses"""
        if transactions_df.empty:
            return None
        
        # Extract year-month from date
        transactions_df['year_month'] = pd.to_datetime(transactions_df['date']).dt.to_period('M')
        
        # Group by month and type
        monthly_data = (transactions_df.groupby(['year_month', 'type'])['amount']
                       .sum().reset_index())
        
        # Pivot to get income and expense columns
        monthly_pivot = monthly_data.pivot(index='year_month', columns='type', values='amount').fillna(0)
        monthly_pivot = monthly_pivot.reset_index()
        monthly_pivot['year_month'] = monthly_pivot['year_month'].astype(str)
        
        fig = go.Figure()
        
        if 'income' in monthly_pivot.columns:
            fig.add_trace(go.Scatter(
                x=monthly_pivot['year_month'],
                y=monthly_pivot['income'],
                mode='lines+markers',
                name='Income',
                line=dict(color=self.color_palette['income'], width=3),
                marker=dict(size=8)
            ))
        
        if 'expense' in monthly_pivot.columns:
            fig.add_trace(go.Scatter(
                x=monthly_pivot['year_month'],
                y=monthly_pivot['expense'],
                mode='lines+markers',
                name='Expenses',
                line=dict(color=self.color_palette['expense'], width=3),
                marker=dict(size=8)
            ))
        
        # Add savings line (income - expenses)
        if 'income' in monthly_pivot.columns and 'expense' in monthly_pivot.columns:
            monthly_pivot['savings'] = monthly_pivot['income'] - monthly_pivot['expense']
            fig.add_trace(go.Scatter(
                x=monthly_pivot['year_month'],
                y=monthly_pivot['savings'],
                mode='lines+markers',
                name='Net Savings',
                line=dict(color=self.color_palette['savings'], width=3, dash='dash'),
                marker=dict(size=8)
            ))
        
        fig.update_layout(
            title='Monthly Income vs Expenses Trend',
            xaxis_title='Month',
            yaxis_title='Amount ($)',
            height=400,
            hovermode='x unified'
        )
        
        return fig
    
    def create_daily_spending_bar(self, transactions_df, days=30):
        """Create a bar chart showing daily spending for the last N days"""
        if transactions_df.empty:
            return None
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Filter for recent expenses
        recent_data = transactions_df[
            (pd.to_datetime(transactions_df['date']) >= start_date) &
            (transactions_df['type'] == 'expense')
        ].copy()
        
        if recent_data.empty:
            return None
        
        # Group by date
        daily_spending = (recent_data.groupby('date')['amount']
                         .sum().reset_index())
        daily_spending['date'] = pd.to_datetime(daily_spending['date'])
        daily_spending = daily_spending.sort_values('date')
        
        fig = px.bar(
            daily_spending,
            x='date',
            y='amount',
            title=f'Daily Spending (Last {days} Days)',
            labels={'amount': 'Amount ($)', 'date': 'Date'}
        )
        
        fig.update_layout(
            height=400,
            xaxis_title='Date',
            yaxis_title='Amount ($)'
        )
        
        return fig
    

    
    def create_income_breakdown(self, transactions_df):
        """Create a pie chart showing income sources"""
        if transactions_df.empty:
            return None
        
        income_data = transactions_df[transactions_df['type'] == 'income']
        if income_data.empty:
            return None
        
        income_by_category = income_data.groupby('category')['amount'].sum().reset_index()
        
        fig = px.pie(
            income_by_category,
            values='amount',
            names='category',
            title='Income Sources',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_layout(
            height=400,
            showlegend=True
        )
        
        return fig
    
    def create_50_30_20_gauge(self, total_income, needs_spending, wants_spending):
        """Create gauge charts for the 50/30/20 rule"""
        if total_income <= 0:
            return None
        
        try:
            needs_pct = (needs_spending / total_income) * 100
            wants_pct = (wants_spending / total_income) * 100
            savings_pct = 100 - needs_pct - wants_pct
            
            fig = make_subplots(
                rows=1, cols=3,
                specs=[[{'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}]],
                subplot_titles=("Needs (50%)", "Wants (30%)", "Savings (20%)")
            )
        
            fig.add_trace(go.Indicator(
                mode="gauge+number+delta", value=needs_pct,
                title={'text': "Needs"},
                delta={'reference': 50},
                gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "darkblue"}}
            ), row=1, col=1)
            
            fig.add_trace(go.Indicator(
                mode="gauge+number+delta", value=wants_pct,
                title={'text': "Wants"},
                delta={'reference': 30},
                gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "darkgreen"}}
            ), row=1, col=2)
            
            fig.add_trace(go.Indicator(
                mode="gauge+number+delta", value=savings_pct,
                title={'text': "Savings"},
                delta={'reference': 20},
                gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "purple"}}
            ), row=1, col=3)
            
            fig.update_layout(height=300, showlegend=False)
            return fig
            
        except Exception as e:
            # Return a simple bar chart if gauge charts fail
            needs_pct_safe = (needs_spending / total_income) * 100 if total_income > 0 else 0
            wants_pct_safe = (wants_spending / total_income) * 100 if total_income > 0 else 0
            savings_pct_safe = 100 - needs_pct_safe - wants_pct_safe
            
            fig = go.Figure(data=[
                go.Bar(name='Current', x=['Needs', 'Wants', 'Savings'], 
                       y=[needs_pct_safe, wants_pct_safe, savings_pct_safe]),
                go.Bar(name='Target', x=['Needs', 'Wants', 'Savings'], 
                       y=[50, 30, 20], opacity=0.6)
            ])
            fig.update_layout(
                title="50/30/20 Rule Analysis (Fallback View)",
                yaxis_title="Percentage (%)",
                height=300,
                barmode='group'
            )
            return fig
    
    def create_budget_vs_actual_chart(self, transactions_df, budget_targets_df):
        """Create a comparison chart of budget vs actual spending by category"""
        try:
            if transactions_df.empty or budget_targets_df.empty:
                return None
            
            current_month = datetime.now().strftime('%Y-%m')
            monthly_data = transactions_df[
                (transactions_df['date'].str.startswith(current_month)) &
                (transactions_df['type'] == 'expense')
            ]
            
            if monthly_data.empty:
                return None
            
            actual_spending = monthly_data.groupby('category')['amount'].sum()
            
            # Create budget targets dictionary
            budget_targets = dict(zip(budget_targets_df['category'], budget_targets_df['monthly_target']))
            
            # Get all categories that have either budget or actual spending
            all_categories = set(budget_targets.keys()) | set(actual_spending.index)
            
            categories = list(all_categories)
            budget_amounts = [budget_targets.get(cat, 0) for cat in categories]
            actual_amounts = [actual_spending.get(cat, 0) for cat in categories]
            
            fig = go.Figure(data=[
                go.Bar(name='Budget Target', x=categories, y=budget_amounts, 
                       marker_color='lightblue', opacity=0.7),
                go.Bar(name='Actual Spending', x=categories, y=actual_amounts, 
                       marker_color='darkred', opacity=0.8)
            ])
            
            fig.update_layout(
                barmode='group',
                title='Budget vs Actual Spending (Current Month)',
                xaxis_title='Category',
                yaxis_title='Amount ($)',
                height=400,
                showlegend=True
            )
            
            return fig
        except Exception as e:
            return None 