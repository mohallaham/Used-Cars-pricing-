import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import json

# Hide Streamlit's default sidebar navigation and adjust padding
# st.set_page_config(
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

hide_streamlit_nav = """
<style>
[data-testid="stSidebarNav"] {display: none !important;}
/* Remove padding around the main content area */
[data-testid="stAppViewContainer"] > .main {
    padding-top: 0rem;
    padding-right: 0rem;
    padding-left: 0rem;
    padding-bottom: 0rem;
}
/* Remove padding around the iframe container */
[data-testid="stHorizontalBlock"] {
    padding: 0rem;
}
/* Make the iframe take full width and height */
iframe {
    width: 100%;
    height: 100vh;
}
</style>
"""
st.markdown(hide_streamlit_nav, unsafe_allow_html=True)


# Create sidebar with navigation
try:    
    with st.sidebar:
       
        # Main navigation menu
        main_menu = option_menu(
            menu_title='Navigation',
            options=["Home", "Car Pricing", "Dashboard"],
            icons=["house", "tag", "bar-chart"],
            menu_icon="cast",
            default_index=2,  # Default to Dashboard since we're on that page
            styles={"container": {"background-color": "#F0F2F6", "padding": "10px", "border-radius": "10px"}}
        )
        
        # Handle main navigation
        if main_menu == "Home":
            st.switch_page("Home.py")
        elif main_menu == "Car Pricing":
            st.switch_page("pages/1_Car_Pricing.py")
        
        # Dashboard sub-menu
        st.markdown("### Dashboard Type")
        dashboard_type = option_menu(
            menu_title=None,
            options=["Non-Electric Cars", "Electric Cars"],
            icons=["fuel-pump", "lightning-charge"],
            menu_icon="cast",
            default_index=0,
            styles={"container": {"background-color": "#F0F2F6", "padding": "10px", "border-radius": "10px"}}
        )
        
        # Add a separator
        st.markdown("---")
        # Contact information section
        st.markdown("### Contact Information")
        st.markdown("✉️ Email: mhmmdallahham@gmail.com")
        st.markdown("📱 Phone: 0770067932")
        
except Exception as e:
    st.sidebar.error(f"Error in sidebar: {e}")
    st.sidebar.markdown("### Contact Information")
    st.sidebar.markdown("📧 Email: mhmmdallahham@gmail.com")
    st.sidebar.markdown("📱 Phone: 0770067932")

# Display dashboard based on selection
if dashboard_type == "Non-Electric Cars":
    # Set the title for the Streamlit page
    st.title("Non-Electric Cars Dashboard")

    # Add description to the page
    st.write(
        "This page contains an embedded Power BI Dashboard for non-electric cars. Below is the Power BI report displayed on the site."
    )

    # Embed the Power BI report using iframe
    powerbi_url = "https://app.fabric.microsoft.com/reportEmbed?reportId=655d1050-4864-42b5-b464-b8dc5b6e1dad&autoAuth=true&ctid=acf629da-951b-4fd2-81dc-9d427b929d96"

    # Use CSS to make iframe full screen
    components.html(
        f"""
        <div style="width:100%; height:100vh;">
            <iframe 
                src="{powerbi_url}" 
                width="100%" 
                height="100%" 
                frameborder="0" 
                style="border:0; overflow:hidden;"
                allowfullscreen="true">
            </iframe>
        </div>
        """,
        height=1000,  # Fallback height
        scrolling=True
    )
else:  # Electric Cars
    # Set the title for the Streamlit page
    st.title("Electric Cars Dashboard")

    # Add description to the page
    st.write(
        "This page contains an embedded Power BI Dashboard for electric cars. Below is the Power BI report displayed on the site."
    )

    # Embed the Power BI report using iframe
    powerbi_url = "https://app.fabric.microsoft.com/reportEmbed?reportId=b7278538-dcfe-42cc-b630-762fbe385eec&autoAuth=true&ctid=acf629da-951b-4fd2-81dc-9d427b929d96"

    # Use CSS to make iframe full screen
    components.html(
        f"""
        <div style="width:100%; height:100vh;">
            <iframe 
                src="{powerbi_url}" 
                width="100%" 
                height="100%" 
                frameborder="0" 
                style="border:0; overflow:hidden;"
                allowfullscreen="true">
            </iframe>
        </div>
        """,
        height=1000,  # Fallback height
        scrolling=True
    )
