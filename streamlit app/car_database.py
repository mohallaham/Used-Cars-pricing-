# car_database.py
import sqlite3
import pandas as pd
import os

# Define the database path
DB_PATH = os.path.join(os.path.dirname(__file__), "Cars_DB.db")

def initialize_db():
    """
    Initialize the database by creating tables if they don't exist.
    Returns whether the tables existed before initialization.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if Electric_Cars table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Electric_Cars'")
    electric_table_exists = cursor.fetchone() is not None
    
    # Check if Non_Electric_Cars table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Non_Electric_Cars'")
    non_electric_table_exists = cursor.fetchone() is not None
    
    # Check if electric_cars_modeling exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='electric_cars_modeling'")
    electric_modeling_exists = cursor.fetchone() is not None
    
    # Check if non_electric_cars_modeling exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='non_electric_cars_modeling'")
    non_electric_modeling_exists = cursor.fetchone() is not None
    
    # Create tables only if they don't exist
    if not electric_table_exists:
        # Create Electric_Cars table
        cursor.execute('''
        CREATE TABLE Electric_Cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            make TEXT,
            model TEXT,
            trim TEXT,
            condition TEXT,
            year INTEGER,
            body_type TEXT,
            seats INTEGER,
            transmission TEXT,
            kilometers INTEGER,
            body_condition TEXT,
            paint TEXT,
            regional_specs TEXT,
            insurance TEXT,
            license TEXT,
            car_customs TEXT,
            city TEXT,
            neighborhood TEXT,
            interior_options TEXT,
            exterior_options TEXT,
            tech_options TEXT,
            fuel_type TEXT,
            battery_range INTEGER,
            battery_capacity INTEGER,
            submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
    
    if not non_electric_table_exists:
        # Create Non_Electric_Cars table
        cursor.execute('''
        CREATE TABLE Non_Electric_Cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            make TEXT,
            model TEXT,
            trim TEXT,
            condition TEXT,
            year INTEGER,
            body_type TEXT,
            seats INTEGER,
            transmission TEXT,
            kilometers INTEGER,
            body_condition TEXT,
            paint TEXT,
            regional_specs TEXT,
            insurance TEXT,
            license TEXT,
            car_customs TEXT,
            city TEXT,
            neighborhood TEXT,
            interior_options TEXT,
            exterior_options TEXT,
            tech_options TEXT,
            fuel_type TEXT,
            engine_size REAL,
            cylinders INTEGER,
            submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
    
    if not non_electric_modeling_exists:
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
                "Engine Size (cc)" REAL,
                "Regional Specs" TEXT,
                "Car License" TEXT,
                "Insurance" TEXT,
                "Car Customs" TEXT,
                "Body Condition" TEXT,
                body_condition_encoded INTEGER,
                "Paint" TEXT,
                paint_condition_encoded INTEGER,
                interior_steering_wheel_controls INTEGER,
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
                "technology_navigation_system_/_maps" INTEGER,
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
    
    if not electric_modeling_exists:
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
            interior_steering_wheel_controls INTEGER,
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
            "technology_navigation_system_/_maps" INTEGER,
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
    
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Cars_Data'")
        if not cursor.fetchone():
            csv_path = os.path.join(os.path.dirname(__file__), "data", "enriched_cars_data_4.csv")
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)
                df.to_sql('Cars_Data', conn, if_exists='replace', index=False)
    except Exception as e:
        print(f"Error creating Cars_Data table: {e}")

    # Check if predicted_non_electric table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='predicted_non_electric'")
    pred_non_electric_exists = cursor.fetchone() is not None

    # Check if predicted_electric table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='predicted_electric'")
    pred_electric_exists = cursor.fetchone() is not None

    # Create prediction tables if they don't exist
    if not pred_non_electric_exists:
        cursor.execute('''
        CREATE TABLE predicted_non_electric (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_id INTEGER,
            predicted_price REAL,
            prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (car_id) REFERENCES non_electric_cars_modeling(rowid)
        )
        ''')

    if not pred_electric_exists:
        cursor.execute('''
        CREATE TABLE predicted_electric (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_id INTEGER,
            predicted_price REAL,
            prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (car_id) REFERENCES electric_cars_modeling(rowid)
        )
        ''')
    conn.commit()
    conn.close()

    return electric_table_exists, non_electric_table_exists

def save_car_data(data, is_electric):
    """
    Save car data to the appropriate table based on whether it's electric.
    
    Args:
        data (dict): Dictionary containing car data.
        is_electric (bool): Whether the car is electric.
        
    Returns:
        tuple: (table_name, success) where table_name is the name of the table 
               where data was saved and success is a boolean indicating if the 
               operation was successful.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Choose the appropriate table based on fuel type
    table_name = 'Electric_Cars' if is_electric else 'Non_Electric_Cars'
    
    # Remove fields that don't belong in the chosen table
    if is_electric:
        data.pop('engine_size', None)
        data.pop('cylinders', None)
    else:
        data.pop('battery_range', None)
        data.pop('battery_capacity', None)
    
    # Remove None values
    clean_data = {k: v for k, v in data.items() if v is not None}
    
    try:
        # Prepare SQL query
        columns = ', '.join(clean_data.keys())
        placeholders = ', '.join(['?' for _ in clean_data])
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        # Execute query with data values
        cursor.execute(sql, list(clean_data.values()))
        conn.commit()
        success = True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        success = False
    finally:
        conn.close()
    
    return table_name, success

def check_database_stats():
    """
    Check database statistics including record counts and sample data.
    
    Returns:
        dict: Dictionary containing database statistics or error information.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check Electric_Cars table
        cursor.execute("SELECT COUNT(*) FROM Electric_Cars")
        electric_count = cursor.fetchone()[0]
        
        # Check Non_Electric_Cars table
        cursor.execute("SELECT COUNT(*) FROM Non_Electric_Cars")
        non_electric_count = cursor.fetchone()[0]
        
        # Get some sample data
        cursor.execute("SELECT id, make, model, year FROM Electric_Cars LIMIT 3")
        electric_samples = cursor.fetchall()
        
        cursor.execute("SELECT id, make, model, year FROM Non_Electric_Cars LIMIT 3")
        non_electric_samples = cursor.fetchall()
        
        return {
            "electric_count": electric_count,
            "non_electric_count": non_electric_count,
            "electric_samples": electric_samples,
            "non_electric_samples": non_electric_samples
        }
    except sqlite3.Error as e:
        return {"error": str(e)}
    finally:
        conn.close()

def get_database_path():
    """
    Get the absolute path to the database file.
    
    Returns:
        str: Absolute path to the database file.
    """
    return os.path.abspath(DB_PATH)

def get_last_row(is_electric):
    """Get the most recently added car entry from the database."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        table_name = 'Electric_Cars' if is_electric else 'Non_Electric_Cars'
        cursor.execute(f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        
        if row:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))
        return None
    
    except sqlite3.Error as e:
        print(f"Database error while getting last row: {str(e)}")
        return None
    finally:
        if conn:
            conn.close()

# def store_prediction(car_id, is_electric, predicted_price):
#     """Store the predicted price in the database"""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
    
#     try:
#         table_name = 'electric_cars_modeling' if is_electric else 'non_electric_cars_modeling'
#         cursor.execute(f"""
#             UPDATE {table_name} 
#             SET predicted_price = ?
#             WHERE id = ?
#         """, (predicted_price, car_id))
        
#         conn.commit()
#         return True
#     except sqlite3.Error as e:
#         print(f"Database error storing prediction: {e}")
#         return False
#     finally:
#         conn.close()
