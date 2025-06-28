import streamlit as st
import re
import hashlib
import secrets
from database import BudgetDatabase

class AuthManager:
    def __init__(self):
        self.db = BudgetDatabase()
    
    def is_valid_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def is_strong_password(self, password):
        """Check if password meets security requirements"""
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        if not re.search(r'[A-Za-z]', password):
            return False, "Password must contain at least one letter"
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one number"
        return True, "Password is strong"
    
    def hash_password(self, password):
        """Hash password with salt for security"""
        salt = secrets.token_hex(16)
        hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return salt + hashed.hex()
    
    def verify_password(self, password, stored_hash):
        """Verify password against stored hash"""
        if not stored_hash or len(stored_hash) < 32:
            return False
        salt = stored_hash[:32]
        stored_password = stored_hash[32:]
        hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return hashed.hex() == stored_password
    
    def login_form(self):
        """Display enhanced login/register form"""
        st.markdown("""
        <div style="
            max-width: 450px;
            margin: 2rem auto;
            padding: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            text-align: center;
        ">
            <h1 style="color: white; margin-bottom: 1rem; font-size: 2.5rem;">
                💰 Budget Coach
            </h1>
            <p style="color: rgba(255,255,255,0.9); margin-bottom: 2rem; font-size: 1.2rem;">
                Your Personal Financial Assistant
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create tabs for Login and Register
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
        
        with tab1:
            self._login_tab()
        
        with tab2:
            self._register_tab()
    
    def _login_tab(self):
        """Login form tab"""
        with st.form("login_form"):
            st.markdown("### 🔑 Welcome Back!")
            st.markdown("Sign in to access your financial dashboard")
            
            email = st.text_input(
                "Email Address",
                placeholder="your.email@example.com",
                key="login_email"
            )
            
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_password"
            )
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit = st.form_submit_button(
                    "🚀 Sign In",
                    use_container_width=True
                )
            
            if submit:
                if not email or not password:
                    st.error("Please fill in all fields")
                elif not self.is_valid_email(email):
                    st.error("Please enter a valid email address")
                else:
                    user = self.db.get_user_by_email(email)
                    if user and self.verify_password(password, user.get('password_hash', '')):
                        # Successful login
                        self._authenticate_user(user)
                        st.success(f"Welcome back, {user['name']}! 🎉")
                        st.rerun()
                    else:
                        st.error("❌ Invalid email or password")
    
    def _register_tab(self):
        """Registration form tab"""
        with st.form("register_form"):
            st.markdown("### 📝 Create Account")
            st.markdown("Join thousands of users managing their finances!")
            
            name = st.text_input(
                "Full Name",
                placeholder="John Doe",
                key="register_name"
            )
            
            email = st.text_input(
                "Email Address",
                placeholder="your.email@example.com",
                key="register_email"
            )
            
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Create a strong password",
                help="At least 6 characters with letters and numbers",
                key="register_password"
            )
            
            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Re-enter your password",
                key="register_confirm_password"
            )
            
            # Terms checkbox
            agree_terms = st.checkbox(
                "I agree to the Terms of Service and Privacy Policy",
                key="agree_terms"
            )
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit = st.form_submit_button(
                    "✨ Create Account",
                    use_container_width=True
                )
            
            if submit:
                if not all([name, email, password, confirm_password]):
                    st.error("Please fill in all fields")
                elif not self.is_valid_email(email):
                    st.error("Please enter a valid email address")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                elif not agree_terms:
                    st.error("Please agree to the Terms of Service")
                else:
                    # Check password strength
                    is_strong, message = self.is_strong_password(password)
                    if not is_strong:
                        st.error(f"❌ {message}")
                    else:
                        # Check if user already exists
                        existing_user = self.db.get_user_by_email(email)
                        if existing_user:
                            st.error("❌ An account with this email already exists")
                        else:
                            # Create new user
                            password_hash = self.hash_password(password)
                            user_id = self.db.create_user_with_password(email, name, password_hash)
                            
                            if user_id:
                                # Auto-login the new user
                                user = self.db.get_user_by_email(email)
                                self._authenticate_user(user)
                                
                                st.success("🎉 Account created successfully!")
                                st.balloons()
                                st.info("Welcome to Budget Coach! Let's start your financial journey! 🚀")
                                st.rerun()
                            else:
                                st.error("❌ Failed to create account. Please try again.")
    
    def _authenticate_user(self, user):
        """Set session state for authenticated user"""
        st.session_state.authenticated = True
        st.session_state.user_id = user['id']
        st.session_state.user_email = user['email']
        st.session_state.user_name = user['name']
        st.session_state.is_new_user = user.get('login_count', 0) <= 1
        
        # Start session tracking
        session_id = self.db.start_user_session(user['id'])
        st.session_state.session_id = session_id
    
    def logout(self):
        """Handle user logout with notification"""
        user_name = st.session_state.get('user_name', 'User')
        
        # Clear session state
        keys_to_clear = [
            'authenticated', 'user_id', 'user_email', 'user_name', 
            'is_new_user', 'session_id'
        ]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        
        st.success(f"👋 Goodbye {user_name}! Your data has been saved securely.")
        st.info("💡 Come back anytime to continue managing your finances!")
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
        """Show enhanced welcome message for new users"""
        if st.session_state.get('is_new_user', False):
            st.balloons()
            st.success("""
            🎉 **Welcome to Budget Coach!** 
            
            Your account has been created successfully! Here's what you can do:
            """)
            
            # Show feature highlights
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info("📊 **Track Finances**\nAdd income & expenses")
            with col2:
                st.info("🎯 **Set Goals**\nCreate savings targets")
            with col3:
                st.info("🏆 **Earn Rewards**\nGet achievements!")
            
            st.markdown("---")
            st.markdown("💡 **Quick Start:** Navigate to 'Add Transaction' to log your first entry!")
            
            # Mark as no longer new user
            st.session_state.is_new_user = False
    
    def show_notifications(self):
        """Show user notifications"""
        if self.is_authenticated():
            user_id = st.session_state.get('user_id')
            
            # Example notifications - you can enhance this
            notifications = []
            
            # Check for achievements
            if hasattr(st.session_state, 'new_achievements'):
                for achievement in st.session_state.new_achievements:
                    notifications.append({
                        'type': 'success',
                        'message': f"🏆 New Achievement: {achievement}!",
                        'dismissible': True
                    })
            
            # Check for goal progress
            # Add more notification logic here
            
            return notifications
        return []
    
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