# preprocess.py
import sqlite3
import pandas as pd
import numpy as np
from car_database import DB_PATH, get_last_row

def process_new_car(is_electric):
    """Process the most recently added car data."""
    try:
        # Get data using the imported get_last_row function
        car_data = get_last_row(is_electric)
        if not car_data:
            print("No car data found to process")
            return False

        df = pd.DataFrame([car_data])
        df = preprocess_data(df)
        success = store_processed_data(df, is_electric)
        return success
    except Exception as e:
        print(f"Error processing car data: {e}")
        return False

def preprocess_data(df):
    """Apply preprocessing steps to the car data."""
    try:
        # Drop columns that aren't needed for modeling
        dropping_unneeded_col(df)
            
        # Convert numeric columns
        to_numeric(df)
        
        # Count features from options
        count_options(df)
        
        # Extract and encode options
        encode_options(df)
        
        # Apply feature engineering
        feture_engineering(df)
        
        return df
    except Exception as e:
        print(f"Error in preprocessing: {e}")
        raise

def dropping_unneeded_col(df):
    """Drop columns that aren't needed for modeling."""
    if 'id' in df.columns:
        df.drop(columns=['id'], inplace=True, errors='ignore')
    if 'city' in df.columns:
        df.drop(columns=['city'], inplace=True, errors='ignore')
    if 'neighborhood' in df.columns:
        df.drop(columns=['neighborhood'], inplace=True, errors='ignore')
    if 'cylinders' in df.columns:
        df.drop(columns=['cylinders'], inplace=True, errors='ignore')
    if 'submission_date' in df.columns:
        df.drop(columns=['submission_date'], inplace=True, errors='ignore')

def to_numeric(df):
    """Convert numeric columns to numeric types."""
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df['kilometers'] = pd.to_numeric(df['kilometers'], errors='coerce')
    df['seats'] = pd.to_numeric(df['seats'], errors='coerce')
    
    if 'engine_size' in df.columns:
        df['engine_size'] = pd.to_numeric(df['engine_size'], errors='coerce')
    if 'battery_range' in df.columns:
        df['battery_range'] = pd.to_numeric(df['battery_range'], errors='coerce')
    if 'battery_capacity' in df.columns:
        df['battery_capacity'] = pd.to_numeric(df['battery_capacity'], errors='coerce')

def extract_options(df, attr):
    """Extract options from a comma-separated string attribute."""
    return df[attr].fillna("").str.split(",").apply(lambda items: [item.strip() for item in items if item.strip() != ""]).tolist()

def count_options(df):
    """Count the number of options in each category."""
    # Using the actual implementation from the new code
    def count_non_empty(options_str):
        if pd.isna(options_str) or options_str == "":
            return 0
        return len([x for x in options_str.split(',') if x.strip()])
    
    df['Interior_Options_Count'] = df['interior_options'].apply(count_non_empty)
    df['Exterior_Options_Count'] = df['exterior_options'].apply(count_non_empty)
    df['Technology_Options_Count'] = df['tech_options'].apply(count_non_empty)
    df['Total_Options_Count'] = df['Interior_Options_Count'] + df['Exterior_Options_Count'] + df['Technology_Options_Count']

def encode_options(df):
    """Create binary features for specific options."""
    # Using the implementation from the new code
    df["interior_steering_wheel_controls"] = df['interior_options'].apply(lambda x: 1 if 'Steering Wheel Controls' in x else 0)
    df["interior_airbags"] = df['interior_options'].apply(lambda x: 1 if 'Airbags' in x else 0)
    df["interior_electric_seat_control"] = df['interior_options'].apply(lambda x: 1 if 'Electric Seat Control' in x else 0)
    
    df["exterior_rear_sensors"] = df['exterior_options'].apply(lambda x: 1 if 'Rear Sensors' in x else 0)
    df["exterior_keyless_entry"] = df['exterior_options'].apply(lambda x: 1 if 'Keyless Entry' in x else 0)
    df["exterior_front_sensors"] = df['exterior_options'].apply(lambda x: 1 if 'Front Sensors' in x else 0)
    
    df["technology_cruise_control"] = df['tech_options'].apply(lambda x: 1 if 'Cruise Control' in x else 0)
    df["technology_tyre_pressure_monitoring"] = df['tech_options'].apply(lambda x: 1 if 'Tyre Pressure Monitoring' in x else 0)
    df["technology_traction_control"] = df['tech_options'].apply(lambda x: 1 if 'Traction Control' in x else 0)
    df["technology_voice_control"] = df['tech_options'].apply(lambda x: 1 if 'Voice Control' in x else 0)
    df["technology_blind_spot_alert"] = df['tech_options'].apply(lambda x: 1 if 'Blind Spot Alert' in x else 0)
    df["technology_forward_collision_alert"] = df['tech_options'].apply(lambda x: 1 if 'Forward Collision Alert' in x else 0)
    df["technology_lane_departure_alert"] = df['tech_options'].apply(lambda x: 1 if 'Lane Departure Alert' in x else 0)
    df["technology_navigation_system_/_maps"] = df['tech_options'].apply(lambda x: 1 if 'Navigation system/maps' in x else 0)

def feture_engineering(df):
    """Apply feature engineering to create derived features."""
    # Using the implementation from the new code with original naming
    # 1. Luxury brand flag
    premium_brands = ['Mercedes Benz', 'BMW', 'Lexus', 'Audi', 'Porsche', 'Land Rover', 'Cadillac']
    df['is_luxury'] = df['make'].apply(lambda x: 1 if x in premium_brands else 0)

    # 2. Age-based features
    df['car_age'] = 2025 - df['year']
    df['car_age_sqrt'] = np.sqrt(df['car_age'])
    df['age_km_interaction'] = df['car_age'] * df['kilometers']

    # 3. Cube-root transformations for option counts
    for col in ['Interior_Options_Count', 'Exterior_Options_Count', 'Technology_Options_Count', 'Total_Options_Count']:
        df[f'{col}_cuberoot'] = np.cbrt(df[col])

    # 4. Condition encodings using raw "Body Condition" and "Paint"
    body_mapping = {
        'Excellent with no defects': 4,
        'Good (body only has minor blemishes)': 3,
        'Fair (body needs work)': 2,
        'Poor (severe body damages)': 1,
        'Other': 0
    }
    paint_mapping = {
        'Original Paint': 3,
        'Partially repainted': 2,
        'Total repaint': 1,
        'Other': 0
    }
    df['body_condition_encoded'] = df['body_condition'].map(body_mapping).fillna(0).astype(int)
    df['paint_condition_encoded'] = df['paint'].map(paint_mapping).fillna(0).astype(int)

    # 5. Maintenance score
    df['maintenance_score'] = df['body_condition_encoded'] + df['paint_condition_encoded']

    # 6. Advanced technology flag
    tech_features = [
        'technology_cruise_control', 'technology_tyre_pressure_monitoring',
        'technology_traction_control', 'technology_voice_control',
        'technology_blind_spot_alert', 'technology_forward_collision_alert',
        'technology_lane_departure_alert', 'technology_navigation_system_/_maps'
    ]
    df['has_advanced_tech'] = (df[tech_features].sum(axis=1) > 3).astype(int)

    # 7. Weighted options calculation
    df['weighted_options'] = (0.4 * df['Technology_Options_Count'] + 
                             0.3 * df['Exterior_Options_Count'] + 
                             0.3 * df['Interior_Options_Count'])

    # 8. Size classification
    def determine_size(row):
        if row['body_type'] in ['SUV', 'PickUp', 'Bus_-_Van']:
            return 'large'
        elif row['seats'] > 5:
            return 'large'
        elif row['body_type'] in ['Sedan', 'HatchBack']:
            return 'medium'
        return 'small'

    df['size_class'] = df.apply(determine_size, axis=1)

    # Clean up temporary columns
    df.drop(columns=['car_age'], inplace=True, errors='ignore')

def initialize_db():
    """
    Initialize the database by creating tables if they don't exist.
    Returns whether the tables existed before initialization.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if Electric_Cars table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='electric_cars_modeling'")
    electric_table_exists = cursor.fetchone() is not None
    
    # Check if Non_Electric_Cars table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='non_electric_cars_modeling'")
    non_electric_table_exists = cursor.fetchone() is not None
    
    # Create tables only if they don't exist
    if not electric_table_exists:
        # Create Electric_Cars table
        cursor.execute('''CREATE TABLE non_electric_cars_modeling (
                "Condition" TEXT,
                "Car Make" TEXT,
                is_luxury INTEGER,
                "Model" TEXT,
                "Trim" TEXT,
                "Year" INTEGER,
                car_age_sqrt REAL,
                "Kilometers Numerical" INTEGER,
                age_km_interaction REAL,
                "Body Type" TEXT,
                "Number of Seats" INTEGER,
                "Fuel" TEXT,
                "Transmission" TEXT,
                "Engine Size (cc)" INTEGER,
                "Regional Specs" TEXT,
                "Car License" TEXT,
                "Insurance" TEXT,
                "Car Customs" TEXT,
                "Body Condition" TEXT,
                body_condition_encoded INTEGER,
                "Paint" TEXT,
                paint_condition_encoded INTEGER,
                interior_steering_wheel_controls TEXT,
                interior_airbags INTEGER,
                technology_cruise_control INTEGER,
                exterior_rear_sensors INTEGER,
                exterior_keyless_entry INTEGER,
                technology_tyre_pressure_monitoring INTEGER,
                exterior_front_sensors INTEGER,
                interior_electric_seat_control INTEGER,
                technology_traction_control INTEGER,
                technology_voice_control INTEGER,
                technology_blind_spot_alert INTEGER,
                technology_forward_collision_alert INTEGER,
                technology_lane_departure_alert INTEGER,
                "technology_navigation_system_/_maps" TEXT,
                "Interior_Options_Count" INTEGER,
                "Interior_Options_Count_cuberoot" REAL,
                "Exterior_Options_Count" INTEGER,
                "Exterior_Options_Count_cuberoot" REAL,
                "Technology_Options_Count" INTEGER,
                "Technology_Options_Count_cuberoot" REAL,
                has_advanced_tech INTEGER,
                "Total_Options_Count" INTEGER,
                "Total_Options_Count_cuberoot" REAL,
                weighted_options REAL,
                maintenance_score REAL,
                size_class TEXT
                        );''')
     
    if not non_electric_table_exists:
        # Create Non_Electric_Cars table
        cursor.execute("""CREATE TABLE electric_cars_modeling (
            "Condition" TEXT,
            "Car Make" TEXT,
            is_luxury INTEGER,
            "Model" TEXT,
            "Trim" TEXT,
            "Year" INTEGER,
            car_age_sqrt REAL,
            "Kilometers Numerical" INTEGER,
            age_km_interaction REAL,
            "Body Type" TEXT,
            "Number of Seats" INTEGER,
            "Fuel" TEXT,
            "Transmission" TEXT,
            "Regional Specs" TEXT,
            "Car License" TEXT,
            "Insurance" TEXT,
            "Car Customs" TEXT,
            "Body Condition" TEXT,
            body_condition_encoded INTEGER,
            "Paint" TEXT,
            paint_condition_encoded INTEGER,
            interior_steering_wheel_controls TEXT,
            interior_airbags INTEGER,
            technology_cruise_control INTEGER,
            exterior_rear_sensors INTEGER,
            exterior_keyless_entry INTEGER,
            technology_tyre_pressure_monitoring INTEGER,
            exterior_front_sensors INTEGER,
            interior_electric_seat_control INTEGER,
            technology_traction_control INTEGER,
            technology_voice_control INTEGER,
            technology_blind_spot_alert INTEGER,
            technology_forward_collision_alert INTEGER,
            technology_lane_departure_alert INTEGER,
            "technology_navigation_system_/_maps" TEXT,
            "Interior_Options_Count" INTEGER,
            "Interior_Options_Count_cuberoot" REAL,
            "Exterior_Options_Count" INTEGER,
            "Exterior_Options_Count_cuberoot" REAL,
            "Technology_Options_Count" INTEGER,
            "Technology_Options_Count_cuberoot" REAL,
            has_advanced_tech INTEGER,
            "Total_Options_Count" INTEGER,
            "Total_Options_Count_cuberoot" REAL,
            weighted_options REAL,
            "Battery Capacity" INTEGER,
            "Battery Range" INTEGER,
            maintenance_score REAL,
            size_class TEXT
        );
        """)
    
    conn.commit()
    conn.close()
    
    return electric_table_exists, non_electric_table_exists

def store_processed_data(df, is_electric):
    """
    Store the processed DataFrame to the appropriate table based on the is_electric flag.
    Maps the DataFrame columns to the appropriate table columns with exact spelling and order.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        
        # Create a copy of the DataFrame to avoid modifying the original
        df_to_store = df.copy()
        
        # Choose the correct table and map columns based on the is_electric flag
        if is_electric:
            table_name = 'electric_cars_modeling'
            # Complete mapping for electric cars table
            column_mapping = {
                'condition': 'Condition',
                'make': 'Car Make',
                'is_luxury': 'is_luxury',
                'model': 'Model',
                'trim': 'Trim',
                'year': 'Year',
                'car_age_sqrt': 'car_age_sqrt',
                'kilometers': 'Kilometers Numerical',
                'age_km_interaction': 'age_km_interaction',
                'body_type': 'Body Type',
                'seats': 'Number of Seats',
                'fuel_type': 'Fuel',
                'transmission': 'Transmission',
                'regional_specs': 'Regional Specs',
                'license': 'Car License',
                'insurance': 'Insurance',
                'car_customs': 'Car Customs',
                'body_condition': 'Body Condition',
                'body_condition_encoded': 'body_condition_encoded',
                'paint': 'Paint',
                'paint_condition_encoded': 'paint_condition_encoded',
                'interior_steering_wheel_controls': 'interior_steering_wheel_controls',
                'interior_airbags': 'interior_airbags',
                'technology_cruise_control': 'technology_cruise_control',
                'exterior_rear_sensors': 'exterior_rear_sensors',
                'exterior_keyless_entry': 'exterior_keyless_entry',
                'technology_tyre_pressure_monitoring': 'technology_tyre_pressure_monitoring',
                'exterior_front_sensors': 'exterior_front_sensors',
                'interior_electric_seat_control': 'interior_electric_seat_control',
                'technology_traction_control': 'technology_traction_control',
                'technology_voice_control': 'technology_voice_control',
                'technology_blind_spot_alert': 'technology_blind_spot_alert',
                'technology_forward_collision_alert': 'technology_forward_collision_alert',
                'technology_lane_departure_alert': 'technology_lane_departure_alert',
                'technology_navigation_system_/_maps': 'technology_navigation_system_/_maps',
                'Interior_Options_Count': 'Interior_Options_Count',
                'Interior_Options_Count_cuberoot': 'Interior_Options_Count_cuberoot',
                'Exterior_Options_Count': 'Exterior_Options_Count',
                'Exterior_Options_Count_cuberoot': 'Exterior_Options_Count_cuberoot',
                'Technology_Options_Count': 'Technology_Options_Count',
                'Technology_Options_Count_cuberoot': 'Technology_Options_Count_cuberoot',
                'has_advanced_tech': 'has_advanced_tech',
                'Total_Options_Count': 'Total_Options_Count',
                'Total_Options_Count_cuberoot': 'Total_Options_Count_cuberoot',
                'weighted_options': 'weighted_options',
                'battery_capacity': 'Battery Capacity',
                'battery_range': 'Battery Range',
                'maintenance_score': 'maintenance_score',
                'size_class': 'size_class'
            }
        else:
            table_name = 'non_electric_cars_modeling'
            # Complete mapping for non-electric cars table
            column_mapping = {
                'condition': 'Condition',
                'make': 'Car Make',
                'is_luxury': 'is_luxury',
                'model': 'Model',
                'trim': 'Trim',
                'year': 'Year',
                'car_age_sqrt': 'car_age_sqrt',
                'kilometers': 'Kilometers Numerical',
                'age_km_interaction': 'age_km_interaction',
                'body_type': 'Body Type',
                'seats': 'Number of Seats',
                'fuel_type': 'Fuel',
                'transmission': 'Transmission',
                'engine_size': 'Engine Size (cc)',
                'regional_specs': 'Regional Specs',
                'license': 'Car License',
                'insurance': 'Insurance',
                'car_customs': 'Car Customs',
                'body_condition': 'Body Condition',
                'body_condition_encoded': 'body_condition_encoded',
                'paint': 'Paint',
                'paint_condition_encoded': 'paint_condition_encoded',
                'interior_steering_wheel_controls': 'interior_steering_wheel_controls',
                'interior_airbags': 'interior_airbags',
                'technology_cruise_control': 'technology_cruise_control',
                'exterior_rear_sensors': 'exterior_rear_sensors',
                'exterior_keyless_entry': 'exterior_keyless_entry',
                'technology_tyre_pressure_monitoring': 'technology_tyre_pressure_monitoring',
                'exterior_front_sensors': 'exterior_front_sensors',
                'interior_electric_seat_control': 'interior_electric_seat_control',
                'technology_traction_control': 'technology_traction_control',
                'technology_voice_control': 'technology_voice_control',
                'technology_blind_spot_alert': 'technology_blind_spot_alert',
                'technology_forward_collision_alert': 'technology_forward_collision_alert',
                'technology_lane_departure_alert': 'technology_lane_departure_alert',
                'technology_navigation_system_/_maps': 'technology_navigation_system_/_maps',
                'Interior_Options_Count': 'Interior_Options_Count',
                'Interior_Options_Count_cuberoot': 'Interior_Options_Count_cuberoot',
                'Exterior_Options_Count': 'Exterior_Options_Count',
                'Exterior_Options_Count_cuberoot': 'Exterior_Options_Count_cuberoot',
                'Technology_Options_Count': 'Technology_Options_Count',
                'Technology_Options_Count_cuberoot': 'Technology_Options_Count_cuberoot',
                'has_advanced_tech': 'has_advanced_tech',
                'Total_Options_Count': 'Total_Options_Count',
                'Total_Options_Count_cuberoot': 'Total_Options_Count_cuberoot',
                'weighted_options': 'weighted_options',
                'maintenance_score': 'maintenance_score',
                'size_class': 'size_class'
            }
        
        # Rename columns according to mapping
        rename_dict = {}
        for df_col, db_col in column_mapping.items():
            if df_col in df_to_store.columns:
                rename_dict[df_col] = db_col
        
        df_to_store.rename(columns=rename_dict, inplace=True)
        
        # Filter to include only columns that exist in the target table
        cursor = conn.cursor()
        if is_electric:
            cursor.execute("PRAGMA table_info(electric_cars_modeling)")
        else:
            cursor.execute("PRAGMA table_info(non_electric_cars_modeling)")
        
        table_columns = [col[1] for col in cursor.fetchall()]
        df_columns = df_to_store.columns
        
        # Keep only columns that exist in the target table
        columns_to_keep = [col for col in df_columns if col in table_columns]
        df_to_store = df_to_store[columns_to_keep]
        
        # Add missing columns with NULL values
        for col in table_columns:
            if col not in df_to_store.columns:
                df_to_store[col] = None
        
        # Reorder columns to match the table schema
        df_to_store = df_to_store[table_columns]
        
        # Store the processed DataFrame to the selected table
        df_to_store.to_sql(table_name, conn, if_exists='append', index=False)
        
        conn.commit()
        conn.close()
        print(f"Data successfully stored in {table_name} table")
        return True
        
    except sqlite3.Error as e:
        print(f"Database error while storing data: {str(e)}")
        return False
    except Exception as e:
        print(f"Error while storing data: {str(e)}")
        return False



if __name__ == "__main__":
    # Get electric car flag from the imported function
    is_electric = is_electric_fun()
    
    # Initialize database
    initialize_db()
    
    # Process the car
    success = process_new_car(is_electric)
    
    print(f"Car processing {'successful' if success else 'failed'}")