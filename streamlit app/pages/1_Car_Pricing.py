import streamlit as st
import pandas as pd
from car_database import initialize_db, save_car_data, check_database_stats, get_database_path
from preprocess import process_new_car
from predict import CarPricePredictor
from streamlit_lottie import st_lottie
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import json
import os
from os import path
# Hide Streamlit's default sidebar navigation
hide_streamlit_nav = """
<style>
[data-testid="stSidebarNav"] {display: none !important;}
</style>
"""
st.markdown(hide_streamlit_nav, unsafe_allow_html=True)

# Page configuration
# st.set_page_config(
#     page_title="𝓢𝓪𝔂𝓪𝓻𝓲𝓬𝓮",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# Function to determine if a car is electric based on fuel type
def is_electric_fun():
    # This gets the current fuel_type value from session state (if it exists)
    # or defaults to empty string if not set yet
    fuel_type = st.session_state.get('fuel_type', '')
    return fuel_type == 'Electric'

# Initialize database and get table existence status
tables_existed = initialize_db()

# importing dataset
# df = pd.read_csv(os.path.join(os.path.dirname(__file__), "..", "data", "enriched_cars_data_4.csv"))
try:
    df = pd.read_csv("data/enriched_cars_data_4.csv")
except FileNotFoundError:
    # Option 2: More robust path handling
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "..", "data", "enriched_cars_data_4.csv")
    df = pd.read_csv(csv_path)
car_make_model = df.groupby('Make')['Model'].unique().apply(list).to_dict()
city_neighborhood = df.groupby('City')['Neighborhood'].unique().apply(list).to_dict()
car_model_trim = df.groupby('Model')['Trim'].unique().apply(list).to_dict()
body_type_list = df['Body Type'].unique().tolist()
fuel_type_list = df['Fuel'].unique().tolist()
transmission_list = df['Transmission'].unique().tolist()
regional_specs_list = df['Regional Specs'].unique().tolist()
insurance_list = df['Insurance'].unique().tolist()
body_condition_list = df['Body Condition'].unique().tolist()
paint_list = df['Paint'].unique().tolist()

exterior_options = df["Exterior Options"].fillna("").str.split(",").apply(lambda items: [item.strip() for item in items if item.strip() != ""]).tolist()
interior_options = df["Interior Options"].fillna("").str.split(",").apply(lambda items: [item.strip() for item in items if item.strip() != ""]).tolist()
tech_options = df["Technology Options"].fillna("").str.split(",").apply(lambda items: [item.strip() for item in items if item.strip() != ""]).tolist()

# Using list comprehensions to flatten the lists and get unique items
exterior_options = set(item for sublist in exterior_options for item in sublist)
interior_options = set(item for sublist in interior_options for item in sublist)
tech_options = set(item for sublist in tech_options for item in sublist)


# Create sidebar with navigation
try:    
    with st.sidebar:
       
        # Navigation menu - Modified to include Home
        selected = option_menu(
            menu_title='Navigation',
            options=["Home", "Car Pricing", "Dashboard"],
            icons=["house", "tag", "bar-chart"],
            menu_icon="cast",
            default_index=1,  # Default to Car Pricing since we're on that page
            styles={"container": {"background-color": "#F0F2F6", "padding": "10px", "border-radius": "10px"}}
        )
        
        # Handle navigation
        if selected == "Home":
            st.switch_page("Home.py")
        elif selected == "Dashboard":
            st.switch_page("pages/2_Dashboard.py")
        
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

# Main page content - Only show if we're on the Car Pricing page
st.title("SayaRice: Car Pricing System")
st.divider()
st.markdown("### About SayaRice")
st.markdown("""
    This project, Sayarice, will be a data-driven car pricing system for the Jordanian second-hand market. It aims to solve the problem of inaccurate pricing by individual sellers on online platforms who lack market insights, leading to potential profit loss or prolonged selling times. The proposed solution involves using Machine Learning (ML) models trained on historical data from the Jordanian used car market to predict optimal prices.
    The project will follow the CRISP-DM methodology, involving stages like data collection (web scraping), data understanding and preparation, modeling (regression algorithms), evaluation, and deployment as a user-friendly website. This website will allow users to input car details and receive price recommendations, along with data-driven insights.
    Sayarice will primarily benefit individual car owners, but also used car buyers and online car listing platforms. The goal is to bring transparency and efficiency to the Jordanian second-hand car market."""
)
st.divider()
st.title("Input Form")

# Form fields
make = st.selectbox("Car Make", list(car_make_model.keys()))
model = st.selectbox("Car Model", car_make_model[make])
trim = st.selectbox("Car Trim", car_model_trim[model])
condition = st.radio("Condition", ["New", "Used"], index=None)
year = st.number_input("Year", min_value=1970, max_value=2025)
body_type = st.selectbox("Body Type", body_type_list)
seats = st.number_input("Number of Seats", min_value=1, max_value=9)
transmission = st.selectbox("Transmission Type", transmission_list)
kilometers = st.number_input("Kilometers", min_value=0)
body_condition = st.selectbox("Body Condition", body_condition_list)
paint = st.selectbox("Paint", paint_list)
regional_specs = st.selectbox("Regional Specifications", regional_specs_list)
insurance = st.selectbox("Type of Insurance", insurance_list)
license = st.radio("Does Your Car Licensed?", ["Licensed", "Not Licensed"], index=None)
car_customs = st.radio("Does Your Car Customed?", ["With Customs", "Without Customs"], index=None)
city = st.selectbox("City", list(city_neighborhood.keys()))
neighborhood = st.selectbox("Neighborhood", city_neighborhood[city])

interior = st.pills("Interior Options", interior_options, selection_mode="multi")
interior_str = ",".join(interior) if interior else ""

exterior = st.pills("Exterior Options", exterior_options, selection_mode="multi")
exterior_str = ",".join(exterior) if exterior else ""

tech = st.pills("Technology Options", tech_options, selection_mode="multi")
tech_str = ",".join(tech) if tech else ""

fuel_type = st.selectbox("Fuel Type", fuel_type_list)
# Store fuel type in session state to make it accessible to is_electric_fun()
st.session_state['fuel_type'] = fuel_type

# Initialize variables
battery_range = None
battery_capacity = None
engine_size = None
cylinders = None

if fuel_type == 'Electric':
    battery_range = st.number_input("Battery Range", min_value=100)
    battery_capacity = st.number_input("Battery Capacity", min_value=50)
else:
    engine_size = st.number_input("Engine Size in Liters", min_value=0.0, step=0.1, format="%.1f")
    cylinders = st.number_input("Cylinders", min_value=1, max_value=12)

# Button to submit form
if st.button("Submit"):
    # Prepare data dictionary with all form values
    form_data = {
        'make': make,
        'model': model,
        'trim': trim,
        'condition': condition,
        'year': year,
        'body_type': body_type,
        'seats': seats,
        'transmission': transmission,
        'kilometers': kilometers,
        'body_condition': body_condition,
        'paint': paint,
        'regional_specs': regional_specs,
        'insurance': insurance,
        'license': license,
        'car_customs': car_customs,
        'city': city,
        'neighborhood': neighborhood,
        'interior_options': interior_str,
        'exterior_options': exterior_str,
        'tech_options': tech_str,
        'fuel_type': fuel_type,
        'battery_range': battery_range,
        'battery_capacity': battery_capacity,
        'engine_size': engine_size,
        'cylinders': cylinders
    }
    
    is_electric = (fuel_type == 'Electric')
    table_name, save_success = save_car_data(form_data, is_electric)
    
    if save_success:
        process_success = process_new_car(is_electric)
        
        if process_success:
            try:
                # Initialize predictor with both models
                predictor = CarPricePredictor(
                    non_electric_model_path="models/non_electric.cbm",
                    electric_model_path="models/electric.cbm"
                )
                
                # Get prediction
                predicted_price, car_id, error = predictor.predict_from_processed_data(is_electric)
                
                if error:
                    st.error(f"Prediction error: {error}")
                else:
                    # Display results
                    st.success("### Prediction Results")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Predicted Price", f"{predicted_price:,.0f}JOD")
                    
            except Exception as e:
                st.error(f"Prediction system error: {str(e)}")
    else:
        st.error("Failed to save car data")
