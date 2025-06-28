import streamlit as st
import re
from database import BudgetDatabase

class AuthManager:
    def __init__(self):
        self.db = BudgetDatabase()
    
    def is_valid_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def login_form(self):
        """Display login form and handle authentication"""
        st.markdown("""
        <div style="
            max-width: 400px;
            margin: 2rem auto;
            padding: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            text-align: center;
        ">
            <h2 style="color: white; margin-bottom: 1.5rem; font-size: 2rem;">
                🚀 Welcome to Budget Coach
            </h2>
            <p style="color: rgba(255,255,255,0.9); margin-bottom: 2rem; font-size: 1.1rem;">
                Your Personal Financial Assistant
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("### 📧 Sign In / Sign Up")
            st.markdown("Enter your email to get started with Budget Coach!")
            
            email = st.text_input(
                "Email Address",
                placeholder="your.email@example.com",
                help="We'll use this to track your progress and save your data"
            )
            
            name = st.text_input(
                "Your Name (Optional)",
                placeholder="John Doe",
                help="Help us personalize your experience"
            )
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit = st.form_submit_button(
                    "🚀 Get Started",
                    use_container_width=True
                )
            
            if submit:
                if not email:
                    st.error("Please enter your email address")
                elif not self.is_valid_email(email):
                    st.error("Please enter a valid email address")
                else:
                    # Create or get user
                    user_id = self.db.create_user(email, name if name else None)
                    user = self.db.get_user(email)
                    
                    # Store in session state
                    st.session_state.authenticated = True
                    st.session_state.user_id = user_id
                    st.session_state.user_email = email
                    st.session_state.user_name = name if name else email.split('@')[0]
                    st.session_state.is_new_user = user[4] == 1  # login_count == 1
                    
                    # Start session tracking
                    session_id = self.db.start_user_session(user_id)
                    st.session_state.session_id = session_id
                    
                    st.success(f"Welcome {'back' if not st.session_state.is_new_user else ''}, {st.session_state.user_name}! 🎉")
                    st.rerun()
    
    def logout(self):
        """Handle user logout"""
        # Clear session state
        keys_to_clear = [
            'authenticated', 'user_id', 'user_email', 'user_name', 
            'is_new_user', 'session_id'
        ]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        
        st.success("Logged out successfully! 👋")
        st.rerun()
    
    def is_authenticated(self):
        """Check if user is authenticated"""
        return st.session_state.get('authenticated', False)
    
    def get_current_user(self):
        """Get current user information"""
        if self.is_authenticated():
            return {
                'id': st.session_state.get('user_id'),
                'email': st.session_state.get('user_email'),
                'name': st.session_state.get('user_name'),
                'is_new_user': st.session_state.get('is_new_user', False)
            }
        return None
    
    def track_page_visit(self):
        """Track page visit for analytics"""
        if self.is_authenticated() and 'session_id' in st.session_state:
            self.db.update_session_activity(st.session_state.session_id)
    
    def show_user_welcome(self):
        """Show welcome message for new users"""
        if st.session_state.get('is_new_user', False):
            st.balloons()
            st.info("""
            🎉 **Welcome to Budget Coach!** 
            
            You're now part of our community! Here's what you can do:
            - 📊 Track your income and expenses
            - 🎯 Set savings goals and monitor progress  
            - 🏆 Earn achievements as you build good habits
            - 📈 Get personalized financial advice
            - 🧮 Use our financial calculators
            
            Start by adding your first transaction! 💪
            """)
            # Mark as no longer new user
            st.session_state.is_new_user = False
    
    def show_contact_info(self):
        """Display creator contact information in sidebar"""
        st.sidebar.markdown("---")
        st.sidebar.markdown("""
        ### 👨‍💻 **Created by K.Muhammad Obi**
        
        **Connect with me:**
        
        📧 **Email**: [muhammadkarangwa07@gmail.com](mailto:muhammadkarangwa07@gmail.com)
        
        📱 **Instagram**: [@obi_karangwa](https://instagram.com/obi_karangwa)
        
        ---
        
        💡 **Love Budget Coach?** 
        Share it with friends and help them achieve financial success too! 🚀
        
        ⭐ **Feedback?** 
        Send me a message - I'd love to hear from you!
        """) 