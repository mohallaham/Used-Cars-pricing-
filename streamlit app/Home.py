import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import json
import os
st.set_page_config(
    page_title="𝓢𝓪𝔂𝓪𝓻𝓲𝓬𝓮",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None  # Hides the automatic "About" section
    }
)
# Create pages directory if it doesn't exist
# This is needed for hiding the default Streamlit pages
os.makedirs("pages", exist_ok=True)

# Hide Streamlit's default sidebar navigation
hide_streamlit_nav = """
<style>
[data-testid="stSidebarNav"] {display: none !important;}
</style>
"""
st.markdown(hide_streamlit_nav, unsafe_allow_html=True)

# Disable Streamlit's automatic sidebar for pages


# Load Lottie Animation
def load_lottiefile(filename: str):
    """Load Lottie file from assets/animations/ folder"""
    try:
        path = os.path.join(os.path.dirname(__file__), "assets", "animations", filename)
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Animation not found: {e}")
        return None


# Custom Sidebar with option_menu
with st.sidebar:
    lottie = load_lottiefile("sayarice_animation.json")  # Update path
    if lottie:
        st_lottie(
            lottie,
            speed=1,
            reverse=False,
            loop=False,
            quality="high",
            height=150,
            width=250,
            key="sidebar_lottie"
        )

    st.markdown("---")
    
    # Your custom navigation menu
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Car Pricing", "Dashboard"],
        icons=["house", "tag", "bar-chart"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"background-color": "#F0F2F6", "padding": "10px", "border-radius": "10px"},
            "nav-link": {"font-size": "14px"}
        }
    )

    st.markdown("---")
    st.markdown("### Contact Information")
    st.markdown("✉️ Email: mhmmdallahham@gmail.com")
    st.markdown("📱 Phone: 0770067932")

# Page content based on selection
if selected == "Home":
    st.title("Welcome to SayaRice")
    st.markdown("### AI-Driven Car Pricing System")
    st.divider()
    st.markdown("### About SayaRice")
    st.markdown("""
        This project, Sayarice, will be a data-driven car pricing system for the Jordanian second-hand market. It aims to solve the problem of inaccurate pricing by individual sellers on online platforms who lack market insights, leading to potential profit loss or prolonged selling times. The proposed solution involves using Machine Learning (ML) models trained on historical data from the Jordanian used car market to predict optimal prices.
        
        The project will follow the CRISP-DM methodology, involving stages like data collection (web scraping), data understanding and preparation, modeling (regression algorithms), evaluation, and deployment as a user-friendly website. This website will allow users to input car details and receive price recommendations, along with data-driven insights.
        
        Sayarice will primarily benefit individual car owners, but also used car buyers and online car listing platforms. The goal is to bring transparency and efficiency to the Jordanian second-hand car market."""
    )

elif selected == "Car Pricing":
    st.switch_page("pages/1_Car_Pricing.py")  # Redirect to Car Pricing page

elif selected == "Dashboard":
    st.switch_page("pages/2_Dashboard.py")  # Redirect to Dashboard main page
