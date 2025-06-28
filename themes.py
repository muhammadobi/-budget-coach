import streamlit as st

class ThemeManager:
    def __init__(self):
        self.themes = {
            "modern_light": {
                "name": "🌟 Modern Light",
                "primary_color": "#6366F1",
                "secondary_color": "#8B5CF6", 
                "accent_color": "#06B6D4",
                "success_color": "#10B981",
                "warning_color": "#F59E0B",
                "error_color": "#EF4444",
                "background_color": "#FFFFFF",
                "secondary_background": "#F8FAFC",
                "card_background": "#FFFFFF",
                "text_color": "#1F2937",
                "text_secondary": "#6B7280",
                "border_color": "#E5E7EB"
            },
            "dark_pro": {
                "name": "🌙 Dark Pro",
                "primary_color": "#7C3AED",
                "secondary_color": "#EC4899",
                "accent_color": "#14B8A6",
                "success_color": "#059669",
                "warning_color": "#D97706",
                "error_color": "#DC2626",
                "background_color": "#0F172A",
                "secondary_background": "#1E293B",
                "card_background": "#334155",
                "text_color": "#F8FAFC",
                "text_secondary": "#CBD5E1",
                "border_color": "#475569"
            },
            "ocean_breeze": {
                "name": "🌊 Ocean Breeze",
                "primary_color": "#0EA5E9",
                "secondary_color": "#3B82F6",
                "accent_color": "#06B6D4",
                "success_color": "#059669",
                "warning_color": "#D97706",
                "error_color": "#DC2626",
                "background_color": "#F0F9FF",
                "secondary_background": "#E0F2FE",
                "card_background": "#FFFFFF",
                "text_color": "#0C4A6E",
                "text_secondary": "#0369A1",
                "border_color": "#7DD3FC"
            },
            "forest_green": {
                "name": "🌲 Forest Green",
                "primary_color": "#059669",
                "secondary_color": "#065F46",
                "accent_color": "#10B981",
                "success_color": "#047857",
                "warning_color": "#D97706",
                "error_color": "#DC2626",
                "background_color": "#ECFDF5",
                "secondary_background": "#D1FAE5",
                "card_background": "#FFFFFF",
                "text_color": "#064E3B",
                "text_secondary": "#065F46",
                "border_color": "#A7F3D0"
            },
            "sunset_orange": {
                "name": "🌅 Sunset Orange",
                "primary_color": "#EA580C",
                "secondary_color": "#DC2626",
                "accent_color": "#F59E0B",
                "success_color": "#059669",
                "warning_color": "#D97706",
                "error_color": "#DC2626",
                "background_color": "#FFF7ED",
                "secondary_background": "#FFEDD5",
                "card_background": "#FFFFFF",
                "text_color": "#9A3412",
                "text_secondary": "#C2410C",
                "border_color": "#FED7AA"
            }
        }
    
    def get_theme_css(self, theme_name="modern_light"):
        """Generate comprehensive CSS for the selected theme"""
        theme = self.themes.get(theme_name, self.themes["modern_light"])
        
        return f"""
        <style>
            /* Import Google Fonts */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            /* Global Styles */
            .stApp {{
                font-family: 'Inter', sans-serif;
                background: {theme['background_color']};
                color: {theme['text_color']};
            }}
            
            /* Main Headers with Gradient */
            .main-header {{
                font-size: 2.5rem;
                font-weight: 700;
                text-align: center;
                margin: 1rem 0 2rem 0;
                background: linear-gradient(135deg, {theme['primary_color']}, {theme['secondary_color']});
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                animation: headerGlow 3s ease-in-out infinite alternate;
                letter-spacing: -0.02em;
            }}
            
            @keyframes headerGlow {{
                0% {{ 
                    filter: drop-shadow(0 0 10px {theme['primary_color']}40);
                    transform: scale(1);
                }}
                100% {{ 
                    filter: drop-shadow(0 0 20px {theme['secondary_color']}60);
                    transform: scale(1.02);
                }}
            }}
            
            /* Page Headers */
            .page-header {{
                font-size: 2rem;
                font-weight: 600;
                color: {theme['primary_color']};
                margin-bottom: 1.5rem;
                padding-bottom: 0.5rem;
                border-bottom: 3px solid {theme['accent_color']};
                position: relative;
            }}
            
            .page-header::after {{
                content: '';
                position: absolute;
                bottom: -3px;
                left: 0;
                width: 50px;
                height: 3px;
                background: {theme['secondary_color']};
                border-radius: 2px;
            }}
            
            /* Enhanced Metric Cards */
            .metric-card {{
                background: {theme['card_background']};
                padding: 2rem;
                border-radius: 20px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                margin: 1rem 0;
                border: 1px solid {theme['border_color']};
                position: relative;
                overflow: hidden;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }}
            
            .metric-card::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 4px;
                background: linear-gradient(90deg, {theme['primary_color']}, {theme['accent_color']});
            }}
            
            .metric-card:hover {{
                transform: translateY(-8px) scale(1.02);
                box-shadow: 0 20px 40px rgba(0,0,0,0.15);
                border-color: {theme['primary_color']};
            }}
            
            /* Tip Cards */
            .tip-card {{
                background: linear-gradient(135deg, {theme['card_background']}, {theme['secondary_background']});
                padding: 2.5rem;
                border-radius: 20px;
                border: 1px solid {theme['border_color']};
                margin: 1.5rem 0;
                box-shadow: 0 8px 32px rgba(0,0,0,0.08);
                position: relative;
                overflow: hidden;
                transition: all 0.3s ease;
            }}
            
            .tip-card::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 6px;
                height: 100%;
                background: linear-gradient(180deg, {theme['accent_color']}, {theme['secondary_color']});
            }}
            
            .tip-card:hover {{
                transform: translateX(10px);
                box-shadow: 0 12px 40px rgba(0,0,0,0.12);
            }}
            
            /* Achievement Badges */
            .achievement-badge {{
                background: linear-gradient(135deg, {theme['primary_color']}, {theme['secondary_color']});
                color: white;
                padding: 0.75rem 1.5rem;
                border-radius: 50px;
                font-weight: 600;
                margin: 0.5rem;
                display: inline-block;
                box-shadow: 0 4px 20px rgba(0,0,0,0.2);
                animation: achievementPulse 2s ease-in-out infinite;
                font-size: 0.9rem;
                letter-spacing: 0.02em;
            }}
            
            @keyframes achievementPulse {{
                0%, 100% {{ 
                    transform: scale(1);
                    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
                }}
                50% {{ 
                    transform: scale(1.05);
                    box-shadow: 0 8px 30px rgba(0,0,0,0.3);
                }}
            }}
            
            /* Goal Progress Cards */
            .goal-progress {{
                background: {theme['card_background']};
                border-radius: 16px;
                padding: 1.5rem;
                margin: 1rem 0;
                border: 2px solid {theme['border_color']};
                box-shadow: 0 4px 20px rgba(0,0,0,0.08);
                transition: all 0.3s ease;
                position: relative;
            }}
            
            .goal-progress:hover {{
                border-color: {theme['accent_color']};
                transform: translateY(-4px);
                box-shadow: 0 8px 30px rgba(0,0,0,0.12);
            }}
            
            /* Sidebar Styling */
            .css-1d391kg {{
                background-color: {theme['secondary_background']};
            }}
            
            /* Button Styling */
            .stButton > button {{
                background: linear-gradient(135deg, {theme['primary_color']}, {theme['secondary_color']});
                color: white;
                border: none;
                border-radius: 12px;
                padding: 0.75rem 2rem;
                font-weight: 600;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }}
            
            .stButton > button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.2);
                filter: brightness(1.1);
            }}
            
            /* Select Box Styling */
            .stSelectbox > div > div {{
                background-color: {theme['card_background']};
                color: {theme['text_color']};
                border: 2px solid {theme['border_color']};
                border-radius: 12px;
                transition: all 0.3s ease;
            }}
            
            .stSelectbox > div > div:focus-within {{
                border-color: {theme['primary_color']};
                box-shadow: 0 0 0 3px {theme['primary_color']}20;
            }}
            
            /* Metric Value Styling */
            .metric-value {{
                font-size: 2.5rem;
                font-weight: 700;
                background: linear-gradient(135deg, {theme['primary_color']}, {theme['accent_color']});
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}
            
            /* Success/Warning/Error Colors */
            .success-text {{ color: {theme['success_color']}; }}
            .warning-text {{ color: {theme['warning_color']}; }}
            .error-text {{ color: {theme['error_color']}; }}
            
            /* Scrollbar Styling */
            ::-webkit-scrollbar {{
                width: 8px;
                height: 8px;
            }}
            
            ::-webkit-scrollbar-track {{
                background: {theme['secondary_background']};
                border-radius: 4px;
            }}
            
            ::-webkit-scrollbar-thumb {{
                background: {theme['primary_color']};
                border-radius: 4px;
            }}
            
            ::-webkit-scrollbar-thumb:hover {{
                background: {theme['secondary_color']};
            }}
            
            /* Loading Animation */
            @keyframes shimmer {{
                0% {{ background-position: -200px 0; }}
                100% {{ background-position: calc(200px + 100%) 0; }}
            }}
            
            .loading-shimmer {{
                background: linear-gradient(90deg, transparent, {theme['border_color']}, transparent);
                background-size: 200px 100%;
                animation: shimmer 1.5s infinite;
            }}
        </style>
        """
    
    def create_theme_toggle(self):
        """Create enhanced theme selection interface"""
        if 'theme' not in st.session_state:
            st.session_state.theme = "modern_light"
        
        # Create theme selector with better styling
        theme_names = [self.themes[key]["name"] for key in self.themes.keys()]
        theme_keys = list(self.themes.keys())
        
        current_index = theme_keys.index(st.session_state.theme) if st.session_state.theme in theme_keys else 0
        
        theme_choice = st.selectbox(
            "🎨 Choose Theme",
            theme_names,
            index=current_index,
            key="theme_selector",
            help="Select your preferred theme for the best experience"
        )
        
        # Convert display name back to key
        selected_key = theme_keys[theme_names.index(theme_choice)]
        
        if selected_key != st.session_state.theme:
            st.session_state.theme = selected_key
            st.rerun()
        
        return st.session_state.theme 