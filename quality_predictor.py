import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
import joblib
import os

class MoldingQualityPredictor:
    """
    Predicts warpage and sinkage for injection molding products
    based on process parameters and part geometry
    """
    
    def __init__(self):
        self.warpage_model = None
        self.sinkage_model = None
        self.scaler = StandardScaler()
        self.model_path = "models/"
        self.create_model_dir()
        
    def create_model_dir(self):
        """Create models directory if it doesn't exist"""
        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)
    
    def generate_training_data(self, samples=500):
        """
        Generate synthetic training data based on injection molding parameters
        In real scenario, this would be actual measurement data
        """
        np.random.seed(42)
        
        # Process Parameters (from the research paper)
        melt_temp = np.random.uniform(200, 260, samples)  # 200-260°C
        mold_temp = np.random.uniform(30, 80, samples)    # 30-80°C
        injection_pressure = np.random.uniform(30, 120, samples)  # 30-120 MPa
        holding_pressure = np.random.uniform(20, 80, samples)     # 20-80 MPa
        holding_time = np.random.uniform(5, 30, samples)         # 5-30 seconds
        cooling_time = np.random.uniform(10, 60, samples)        # 10-60 seconds
        
        # Part Geometry Parameters
        wall_thickness = np.random.uniform(1.5, 4.0, samples)  # 1.5-4.0 mm
        part_volume = np.random.uniform(20, 200, samples)      # 20-200 cm³
        aspect_ratio = np.random.uniform(0.5, 3.0, samples)    # Length/Width ratio
        
        # Create feature matrix
        X = np.column_stack([
            melt_temp, mold_temp, injection_pressure, holding_pressure,
            holding_time, cooling_time, wall_thickness, part_volume, aspect_ratio
        ])
        
        # Generate target variables (warpage % and sinkage %)
        # Based on formula from research: these are influenced by process parameters
        warpage = (
            0.15 * (melt_temp - 230) ** 2 / 1000 +
            0.10 * (mold_temp - 50) ** 2 / 100 +
            0.05 * (cooling_time - 30) / 20 +
            0.12 * wall_thickness +
            0.08 * aspect_ratio +
            np.random.normal(0, 0.5, samples)
        )
        warpage = np.clip(warpage, 0.5, 15)
        
        sinkage = (
            0.20 * (holding_pressure - 50) ** 2 / 1000 +
            0.18 * (holding_time - 15) / 10 +
            0.15 * wall_thickness ** 2 / 5 +
            0.12 * (mold_temp - 50) / 30 +
            np.random.normal(0, 0.4, samples)
        )
        sinkage = np.clip(sinkage, 0.3, 12)
        
        return X, warpage, sinkage
    
    def train_models(self):
        """Train neural network models for warpage and sinkage prediction"""
        print("Generating training data...")
        X, y_warpage, y_sinkage = self.generate_training_data(samples=500)
        
        print("Scaling features...")
        X_scaled = self.scaler.fit_transform(X)
        
        print("Training Warpage Prediction Model...")
        self.warpage_model = MLPRegressor(
            hidden_layer_sizes=(64, 32),
            activation='relu',
            max_iter=500,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1
        )
        self.warpage_model.fit(X_scaled, y_warpage)
        
        print("Training Sinkage Prediction Model...")
        self.sinkage_model = MLPRegressor(
            hidden_layer_sizes=(64, 32),
            activation='relu',
            max_iter=500,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1
        )
        self.sinkage_model.fit(X_scaled, y_sinkage)
        
        # Save models
        self.save_models()
        print("Models trained and saved!")
    
    def save_models(self):
        """Save trained models to disk"""
        joblib.dump(self.warpage_model, f"{self.model_path}warpage_model.pkl")
        joblib.dump(self.sinkage_model, f"{self.model_path}sinkage_model.pkl")
        joblib.dump(self.scaler, f"{self.model_path}scaler.pkl")
    
    def load_models(self):
        """Load pre-trained models"""
        try:
            self.warpage_model = joblib.load(f"{self.model_path}warpage_model.pkl")
            self.sinkage_model = joblib.load(f"{self.model_path}sinkage_model.pkl")
            self.scaler = joblib.load(f"{self.model_path}scaler.pkl")
            return True
        except:
            return False
    
    def predict(self, process_params, geometry_params):
        """
        Predict warpage and sinkage
        
        Args:
            process_params (dict): Melt temp, mold temp, pressures, times
            geometry_params (dict): Wall thickness, volume, aspect ratio
            
        Returns:
            dict: Predicted warpage and sinkage percentages
        """
        # Create feature vector
        features = np.array([[
            process_params['melt_temp'],
            process_params['mold_temp'],
            process_params['injection_pressure'],
            process_params['holding_pressure'],
            process_params['holding_time'],
            process_params['cooling_time'],
            geometry_params['wall_thickness'],
            geometry_params['part_volume'],
            geometry_params['aspect_ratio']
        ]])
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Predict
        warpage = self.warpage_model.predict(features_scaled)[0]
        sinkage = self.sinkage_model.predict(features_scaled)[0]
        
        return {
            'warpage_percent': max(0, warpage),
            'sinkage_percent': max(0, sinkage)
        }

if __name__ == "__main__":
    predictor = MoldingQualityPredictor()
    predictor.train_models()
    print("Quality predictor ready!")
