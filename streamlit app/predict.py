# predict.py - UPDATED WITH SEPARATE FEATURE HANDLING
import pandas as pd
import numpy as np
from catboost import CatBoostRegressor
from car_database import DB_PATH
import sqlite3
import os
from typing import Optional, Tuple, Dict, List


class CarPricePredictor:
    """Car price predictor with separate models and feature sets for electric/non-electric"""
    
class CarPricePredictor:

    def __init__(self,
                 non_electric_model_path: str = os.path.join(os.path.dirname(__file__), "models", "non_electric.cbm"),
                 electric_model_path: str = os.path.join(os.path.dirname(__file__), "models", "electric.cbm")):
        """
        Initialize predictor with default model paths
        
        Args:
            non_electric_model_path: Path to non-electric model (default: models/non_electric.cbm)
            electric_model_path: Path to electric model (default: models/electric.cbm)
        """
        try:
            # Verify model paths exist
            if not os.path.exists(non_electric_model_path):
                raise FileNotFoundError(f"Non-electric model not found at {non_electric_model_path}")
            if not os.path.exists(electric_model_path):
                raise FileNotFoundError(f"Electric model not found at {electric_model_path}")
            
            # Load models
            self.non_electric_model = CatBoostRegressor().load_model(non_electric_model_path)
            self.electric_model = CatBoostRegressor().load_model(electric_model_path)
            
            

            # Define feature sets for each model type
            self.feature_sets = {
                'non_electric':['Condition',
                                'Car Make',
                                'is_luxury',
                                'Model',
                                'Trim',
                                'Year',
                                'car_age',
                                'car_age_sqrt',
                                'Kilometers Numerical',
                                'age_km_interaction',
                                'Body Type',
                                'Number of Seats',
                                'Fuel',
                                'Transmission',
                                'Engine Size (cc)',
                                'Engine Size (cc)_cuberoot',
                                'Regional Specs',
                                'Car License',
                                'Insurance',
                                'Car Customs',
                                'Body Condition',
                                'body_condition_encoded',
                                'Paint',
                                'paint_condition_encoded',
                                'interior_steering_wheel_controls',
                                'interior_airbags',
                                'technology_cruise_control',
                                'exterior_rear_sensors',
                                'exterior_keyless_entry',
                                'technology_tyre_pressure_monitoring',
                                'exterior_front_sensors',
                                'interior_electric_seat_control',
                                'technology_traction_control',
                                'technology_voice_control',
                                'technology_blind_spot_alert',
                                'technology_forward_collision_alert',
                                'technology_lane_departure_alert',
                                'technology_navigation_system_/_maps',
                                'Interior_Options_Count',
                                'Interior_Options_Count_cuberoot',
                                'Exterior_Options_Count',
                                'Exterior_Options_Count_cuberoot',
                                'Technology_Options_Count',
                                'Technology_Options_Count_cuberoot',
                                'has_advanced_tech',
                                'Total_Options_Count',
                                'Total_Options_Count_cuberoot',
                                'weighted_options',
                                'maintenance_score',
                                'excellent_maintenance',
                                'size_class'],
                'electric': ['Condition',
                            'Car Make',
                            'is_luxury',
                            'Model',
                            'Trim',
                            'Year',
                            'car_age',
                            'car_age_sqrt',
                            'Kilometers Numerical',
                            'age_km_interaction',
                            'Body Type',
                            'Number of Seats',
                            'Regional Specs',
                            'Car License',
                            'Insurance',
                            'Car Customs',
                            'Body Condition',
                            'body_condition_encoded',
                            'Paint',
                            'paint_condition_encoded',
                            'interior_steering_wheel_controls',
                            'interior_airbags',
                            'technology_cruise_control',
                            'exterior_rear_sensors',
                            'exterior_keyless_entry',
                            'technology_tyre_pressure_monitoring',
                            'exterior_front_sensors',
                            'interior_electric_seat_control',
                            'technology_traction_control',
                            'technology_voice_control',
                            'technology_blind_spot_alert',
                            'technology_forward_collision_alert',
                            'technology_lane_departure_alert',
                            'technology_navigation_system_/_maps',
                            'Interior_Options_Count',
                            'Interior_Options_Count_cuberoot',
                            'Exterior_Options_Count',
                            'Exterior_Options_Count_cuberoot',
                            'Technology_Options_Count',
                            'Technology_Options_Count_cuberoot',
                            'has_advanced_tech',
                            'Total_Options_Count',
                            'Total_Options_Count_cuberoot',
                            'weighted_options',
                            'Battery Capacity',
                            'Battery Range',
                            'maintenance_score',
                            'excellent_maintenance',
                            'size_class']
            }
            
            # Categorical features for each model type
            self.categorical_features = {
                'non_electric': ['Condition',
                                'Car Make',
                                'Model',
                                'Trim',
                                'Body Type',
                                'Fuel',
                                'Transmission',
                                'Regional Specs',
                                'Car License',
                                'Insurance',
                                'Car Customs',
                                'Body Condition',
                                'Paint',
                                'size_class'],
                'electric': ['Condition',
                            'Car Make',
                            'Model',
                            'Trim',
                            'Body Type',
                            'Regional Specs',
                            'Car License',
                            'Insurance',
                            'Car Customs',
                            'Body Condition',
                            'Paint',
                            'size_class']

            }
            
        except Exception as e:
            raise ValueError(f"Initialization failed: {str(e)}")

    def _get_features_from_db(self, is_electric: bool) -> Optional[Tuple[pd.DataFrame, int]]:
        """Retrieve features and rowid from database"""
        conn = sqlite3.connect(DB_PATH)
        try:
            table = 'electric_cars_modeling' if is_electric else 'non_electric_cars_modeling'
            query = f"SELECT rowid, * FROM {table} ORDER BY rowid DESC LIMIT 1"
            df = pd.read_sql(query, conn)
            if df.empty:
                return None
            return df, df['rowid'].iloc[0]
        finally:
            conn.close()

    def _prepare_features(self, df: pd.DataFrame, is_electric: bool) -> pd.DataFrame:
        """Prepare features with robust handling of missing columns"""
        model_type = 'electric' if is_electric else 'non_electric'
        required_features = self.feature_sets[model_type]
        
        # Create a copy of the dataframe to avoid SettingWithCopyWarning
        features = df.copy()
        
        # Ensure all required features exist
        for feat in required_features:
            if feat not in features.columns:
                if feat == 'car_age':
                    features['car_age'] = 2025 - features['Year']
                elif feat == 'excellent_maintenance':
                    if 'maintenance_score' in features.columns:
                        features['excellent_maintenance'] = (features['maintenance_score'] >= 6).astype(int)
                    else:
                        features['excellent_maintenance'] = 0  # Default value
                elif feat == 'Engine Size (cc)_cuberoot' and 'Engine Size (cc)' in features.columns:
                    features['Engine Size (cc)_cuberoot'] = np.cbrt(features['Engine Size (cc)'])
                else:
                    features[feat] = 0  # Default value for other missing features
        
        # Select only the required features
        features = features[required_features]
        
        # Convert categorical features
        for feat in self.categorical_features[model_type]:
            if feat in features.columns:
                features[feat] = features[feat].astype(str).fillna("NaN")
        
        return features
    def predict_from_processed_data(self, is_electric: bool) -> Tuple[Optional[float], Optional[int], Optional[str]]:
        """Make price prediction and store result"""
        try:
            # Get data from database
            result = self._get_features_from_db(is_electric)
            if result is None:
                return None, None, "No processed data found"
                
            df, car_id = result
            
            # Prepare features
            features = self._prepare_features(df, is_electric)
            
            # Make prediction
            model = self.electric_model if is_electric else self.non_electric_model
            log_prediction = model.predict(features)
            prediction = np.exp(log_prediction[0])  # Convert from log price
            
            # Store prediction
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            table = 'predicted_electric' if is_electric else 'predicted_non_electric'
            cursor.execute(f"""
                INSERT INTO {table} (car_id, predicted_price)
                VALUES (?, ?)
            """, (car_id, prediction))
            conn.commit()
            conn.close()
            
            return prediction, car_id, None
            
        except Exception as e:
            return None, None, f"Prediction failed: {str(e)}"
