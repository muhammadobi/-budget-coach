import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
import math

class FinancialCalculators:
    def __init__(self):
        pass
    
    def mortgage_calculator(self):
        """Interactive mortgage calculator with visualization"""
        st.subheader("🏠 Mortgage Calculator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            home_price = st.number_input("Home Price ($)", min_value=50000, max_value=5000000, 
                                       value=350000, step=10000, format="%d")
            down_payment_pct = st.slider("Down Payment (%)", min_value=0, max_value=50, value=20, step=1)
            interest_rate = st.slider("Interest Rate (%)", min_value=1.0, max_value=15.0, value=6.5, step=0.1)
            loan_term = st.selectbox("Loan Term", [15, 20, 25, 30], index=3)
        
        # Calculations
        down_payment = home_price * (down_payment_pct / 100)
        loan_amount = home_price - down_payment
        monthly_rate = interest_rate / 100 / 12
        num_payments = loan_term * 12
        
        if monthly_rate > 0:
            monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / \
                            ((1 + monthly_rate)**num_payments - 1)
        else:
            monthly_payment = loan_amount / num_payments
        
        total_paid = monthly_payment * num_payments
        total_interest = total_paid - loan_amount
        
        with col2:
            st.metric("💰 Monthly Payment", f"${monthly_payment:,.2f}")
            st.metric("🏦 Loan Amount", f"${loan_amount:,.2f}")
            st.metric("💸 Total Interest", f"${total_interest:,.2f}")
            st.metric("📊 Total Paid", f"${total_paid:,.2f}")
        
        # Amortization chart
        if st.checkbox("📈 Show Amortization Schedule"):
            schedule = self.calculate_amortization(loan_amount, monthly_rate, num_payments)
            fig = self.create_amortization_chart(schedule)
            st.plotly_chart(fig, use_container_width=True)
    
    def calculate_amortization(self, loan_amount, monthly_rate, num_payments):
        """Calculate amortization schedule"""
        balance = loan_amount
        schedule = []
        
        for payment_num in range(1, int(num_payments) + 1):
            interest_payment = balance * monthly_rate
            
            if monthly_rate > 0:
                principal_payment = (loan_amount * monthly_rate * (1 + monthly_rate)**num_payments / 
                                   ((1 + monthly_rate)**num_payments - 1)) - interest_payment
            else:
                principal_payment = loan_amount / num_payments
            
            balance -= principal_payment
            
            schedule.append({
                'Payment': payment_num,
                'Principal': principal_payment,
                'Interest': interest_payment,
                'Balance': max(0, balance)
            })
        
        return pd.DataFrame(schedule)
    
    def create_amortization_chart(self, schedule):
        """Create amortization visualization"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=schedule['Payment'],
            y=schedule['Principal'],
            fill='tonexty',
            mode='none',
            name='Principal',
            fillcolor='rgba(76, 175, 80, 0.7)'
        ))
        
        fig.add_trace(go.Scatter(
            x=schedule['Payment'],
            y=schedule['Interest'],
            fill='tozeroy',
            mode='none',
            name='Interest',
            fillcolor='rgba(244, 67, 54, 0.7)'
        ))
        
        fig.update_layout(
            title='Monthly Payment Breakdown Over Time',
            xaxis_title='Payment Number',
            yaxis_title='Amount ($)',
            hovermode='x',
            height=400
        )
        
        return fig
    
    def retirement_calculator(self):
        """Retirement planning calculator"""
        st.subheader("🏖️ Retirement Calculator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            current_age = st.number_input("Current Age", min_value=18, max_value=80, value=30, step=1)
            retirement_age = st.number_input("Retirement Age", min_value=current_age + 1, max_value=85, value=65, step=1)
            current_savings = st.number_input("Current Savings ($)", min_value=0, value=10000, step=1000)
            monthly_contribution = st.number_input("Monthly Contribution ($)", min_value=0, value=500, step=50)
            
        with col2:
            annual_return = st.slider("Expected Annual Return (%)", min_value=1.0, max_value=15.0, value=7.0, step=0.5)
            inflation_rate = st.slider("Inflation Rate (%)", min_value=0.0, max_value=10.0, value=3.0, step=0.5)
            desired_income = st.number_input("Desired Monthly Income ($)", min_value=1000, value=5000, step=500)
        
        # Calculations
        years_to_retirement = retirement_age - current_age
        months_to_retirement = years_to_retirement * 12
        monthly_return = annual_return / 100 / 12
        
        # Future value calculation
        if monthly_return > 0:
            future_value = current_savings * (1 + monthly_return)**months_to_retirement + \
                          monthly_contribution * (((1 + monthly_return)**months_to_retirement - 1) / monthly_return)
        else:
            future_value = current_savings + (monthly_contribution * months_to_retirement)
        
        # Purchasing power adjustment
        inflation_adjusted_value = future_value / ((1 + inflation_rate/100)**years_to_retirement)
        
        # Required nest egg for desired income
        required_nest_egg = desired_income * 12 / (annual_return / 100) * 1.2  # 4% rule adjusted
        
        # Display results
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💰 Projected Savings", f"${future_value:,.0f}")
        with col2:
            st.metric("🛒 Purchasing Power", f"${inflation_adjusted_value:,.0f}")
        with col3:
            st.metric("🎯 Required Nest Egg", f"${required_nest_egg:,.0f}")
        
        # Progress visualization
        progress = (future_value / required_nest_egg) * 100 if required_nest_egg > 0 else 100
        st.metric("📊 Goal Progress", f"{progress:.1f}%")
        
        if progress >= 100:
            st.success("🎉 Congratulations! You're on track for retirement!")
        elif progress >= 75:
            st.warning("⚠️ You're close! Consider increasing contributions.")
        else:
            st.error("🚨 You may need to adjust your retirement plan.")
        
        # Projection chart
        if st.checkbox("📈 Show Growth Projection"):
            projection = self.calculate_retirement_projection(
                current_savings, monthly_contribution, monthly_return, months_to_retirement
            )
            fig = self.create_retirement_chart(projection, required_nest_egg)
            st.plotly_chart(fig, use_container_width=True)
    
    def calculate_retirement_projection(self, initial, monthly, rate, months):
        """Calculate year-by-year retirement savings projection"""
        projection = []
        balance = initial
        
        for month in range(0, months + 1, 12):  # Yearly data points
            year = month // 12
            projection.append({
                'Year': year,
                'Balance': balance,
                'Age': 30 + year  # Assuming starting age 30
            })
            
            # Add 12 months of growth
            for _ in range(12):
                if month + _ * 12 < months:
                    balance = balance * (1 + rate) + monthly
        
        return pd.DataFrame(projection)
    
    def create_retirement_chart(self, projection, target):
        """Create retirement savings projection chart"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=projection['Year'],
            y=projection['Balance'],
            mode='lines+markers',
            name='Projected Savings',
            line=dict(color='#2196F3', width=3),
            fill='tozeroy',
            fillcolor='rgba(33, 150, 243, 0.2)'
        ))
        
        fig.add_hline(
            y=target,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Target: ${target:,.0f}"
        )
        
        fig.update_layout(
            title='Retirement Savings Projection',
            xaxis_title='Years from Now',
            yaxis_title='Savings ($)',
            height=400,
            hovermode='x'
        )
        
        return fig
    
    def loan_calculator(self):
        """General loan calculator"""
        st.subheader("🚗 Loan Calculator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            loan_amount = st.number_input("Loan Amount ($)", min_value=1000, max_value=1000000, 
                                        value=25000, step=1000)
            interest_rate = st.slider("Interest Rate (%)", min_value=0.1, max_value=30.0, value=5.5, step=0.1)
            loan_term_years = st.slider("Loan Term (years)", min_value=1, max_value=10, value=5, step=1)
        
        monthly_rate = interest_rate / 100 / 12
        num_payments = loan_term_years * 12
        
        if monthly_rate > 0:
            monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / \
                            ((1 + monthly_rate)**num_payments - 1)
        else:
            monthly_payment = loan_amount / num_payments
        
        total_paid = monthly_payment * num_payments
        total_interest = total_paid - loan_amount
        
        with col2:
            st.metric("💳 Monthly Payment", f"${monthly_payment:,.2f}")
            st.metric("💸 Total Interest", f"${total_interest:,.2f}")
            st.metric("📊 Total Paid", f"${total_paid:,.2f}")
            
            # Interest vs Principal
            interest_percentage = (total_interest / total_paid) * 100
            st.metric("📈 Interest %", f"{interest_percentage:.1f}%")
    
    def emergency_fund_calculator(self):
        """Emergency fund calculator"""
        st.subheader("🛡️ Emergency Fund Calculator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            monthly_expenses = st.number_input("Monthly Expenses ($)", min_value=500, max_value=20000, 
                                             value=3500, step=100)
            current_emergency_fund = st.number_input("Current Emergency Fund ($)", min_value=0, 
                                                   value=2000, step=100)
            monthly_savings = st.number_input("Monthly Savings Capacity ($)", min_value=0, 
                                            value=300, step=50)
        
        # Calculate recommendations
        emergency_fund_targets = {
            "Basic (3 months)": monthly_expenses * 3,
            "Recommended (6 months)": monthly_expenses * 6,
            "Conservative (12 months)": monthly_expenses * 12
        }
        
        with col2:
            st.write("**Emergency Fund Targets:**")
            for level, target in emergency_fund_targets.items():
                progress = (current_emergency_fund / target) * 100
                months_needed = max(0, (target - current_emergency_fund) / monthly_savings) if monthly_savings > 0 else float('inf')
                
                st.metric(
                    level, 
                    f"${target:,.0f}",
                    delta=f"{progress:.1f}% complete"
                )
                
                if months_needed != float('inf'):
                    st.write(f"⏰ {months_needed:.1f} months to reach")
                st.write("---")
        
        # Visualization
        if st.checkbox("📊 Show Progress Chart"):
            fig = self.create_emergency_fund_chart(emergency_fund_targets, current_emergency_fund)
            st.plotly_chart(fig, use_container_width=True)
    
    def create_emergency_fund_chart(self, targets, current):
        """Create emergency fund progress chart"""
        categories = list(targets.keys())
        target_amounts = list(targets.values())
        current_amounts = [min(current, target) for target in target_amounts]
        
        fig = go.Figure(data=[
            go.Bar(name='Target', x=categories, y=target_amounts, marker_color='lightblue'),
            go.Bar(name='Current', x=categories, y=current_amounts, marker_color='darkblue')
        ])
        
        fig.update_layout(
            barmode='overlay',
            title='Emergency Fund Progress',
            xaxis_title='Target Level',
            yaxis_title='Amount ($)',
            height=400
        )
        
        return fig
    
    def debt_payoff_calculator(self):
        """Debt payoff calculator with snowball vs avalanche"""
        st.subheader("💳 Debt Payoff Calculator")
        
        st.write("Enter your debts:")
        
        # Initialize session state for debts
        if 'debts' not in st.session_state:
            st.session_state.debts = [
                {'name': 'Credit Card 1', 'balance': 5000, 'rate': 18.0, 'minimum': 150},
                {'name': 'Credit Card 2', 'balance': 3000, 'rate': 22.0, 'minimum': 100}
            ]
        
        # Display current debts
        for i, debt in enumerate(st.session_state.debts):
            col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
            
            with col1:
                debt['name'] = st.text_input(f"Debt {i+1}", value=debt['name'], key=f"name_{i}")
            with col2:
                debt['balance'] = st.number_input(f"Balance", value=debt['balance'], key=f"balance_{i}")
            with col3:
                debt['rate'] = st.number_input(f"Interest %", value=debt['rate'], key=f"rate_{i}")
            with col4:
                debt['minimum'] = st.number_input(f"Minimum $", value=debt['minimum'], key=f"minimum_{i}")
            with col5:
                if st.button("🗑️", key=f"delete_{i}"):
                    st.session_state.debts.pop(i)
                    st.rerun()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Add Debt"):
                st.session_state.debts.append({'name': f'Debt {len(st.session_state.debts)+1}', 
                                             'balance': 1000, 'rate': 15.0, 'minimum': 50})
                st.rerun()
        
        with col2:
            extra_payment = st.number_input("Extra Payment ($)", min_value=0, value=200, step=50)
        
        if st.session_state.debts:
            # Calculate payoff strategies
            snowball_result = self.calculate_debt_snowball(st.session_state.debts, extra_payment)
            avalanche_result = self.calculate_debt_avalanche(st.session_state.debts, extra_payment)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("❄️ Debt Snowball")
                st.write("*Pay minimums + extra to smallest balance*")
                st.metric("Time to payoff", f"{snowball_result['months']} months")
                st.metric("Total interest", f"${snowball_result['total_interest']:,.2f}")
            
            with col2:
                st.subheader("🗻 Debt Avalanche")
                st.write("*Pay minimums + extra to highest rate*")
                st.metric("Time to payoff", f"{avalanche_result['months']} months")
                st.metric("Total interest", f"${avalanche_result['total_interest']:,.2f}")
            
            # Show savings
            if avalanche_result['total_interest'] < snowball_result['total_interest']:
                savings = snowball_result['total_interest'] - avalanche_result['total_interest']
                st.success(f"💰 Avalanche method saves ${savings:,.2f} in interest!")
            else:
                st.info("🎯 Both methods are very similar in cost!")
    
    def calculate_debt_snowball(self, debts, extra_payment):
        """Calculate debt snowball payoff strategy"""
        debts_copy = [debt.copy() for debt in debts]
        debts_copy.sort(key=lambda x: x['balance'])  # Sort by balance (smallest first)
        
        return self.simulate_debt_payoff(debts_copy, extra_payment)
    
    def calculate_debt_avalanche(self, debts, extra_payment):
        """Calculate debt avalanche payoff strategy"""
        debts_copy = [debt.copy() for debt in debts]
        debts_copy.sort(key=lambda x: x['rate'], reverse=True)  # Sort by rate (highest first)
        
        return self.simulate_debt_payoff(debts_copy, extra_payment)
    
    def simulate_debt_payoff(self, debts, extra_payment):
        """Simulate debt payoff with given strategy"""
        total_interest = 0
        months = 0
        remaining_debts = [debt for debt in debts if debt['balance'] > 0]
        
        while remaining_debts and months < 600:  # 50 year max
            months += 1
            extra_available = extra_payment
            
            # Pay minimums on all debts
            for debt in remaining_debts:
                monthly_interest = debt['balance'] * (debt['rate'] / 100 / 12)
                principal_payment = debt['minimum'] - monthly_interest
                
                debt['balance'] -= principal_payment
                total_interest += monthly_interest
                debt['balance'] = max(0, debt['balance'])
            
            # Apply extra payment to first debt (strategy determines order)
            if remaining_debts and extra_available > 0:
                target_debt = remaining_debts[0]
                extra_applied = min(extra_available, target_debt['balance'])
                target_debt['balance'] -= extra_applied
            
            # Remove paid off debts
            remaining_debts = [debt for debt in remaining_debts if debt['balance'] > 0.01]
        
        return {
            'months': months,
            'total_interest': total_interest
        } 