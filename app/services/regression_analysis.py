import statsmodels.api as sm
import numpy as np
import json
from typing import Dict, List, Optional
from datetime import datetime

class RegressionAnalysis:
    def __init__(self):
        self.models = {}

    def train_model(self, 
                   data: List[Dict],
                   target_variable: str,
                   feature_variables: List[str]) -> Dict:
        """
        Train a linear regression model
        
        Args:
            data: List of dictionaries containing the training data
            target_variable: Name of the target variable
            feature_variables: List of feature variable names
        
        Returns:
            Dictionary containing model parameters and metrics
        """
        # Convert data to numpy arrays
        X = []
        y = []
        
        for item in data:
            features = []
            for feature in feature_variables:
                features.append(item.get(feature, 0))
            X.append(features)
            y.append(item[target_variable])
        
        X = np.array(X)
        y = np.array(y)
        
        # Add constant term
        X = sm.add_constant(X)
        
        # Fit the model
        model = sm.OLS(y, X).fit()
        
        # Extract coefficients
        coefficients = dict(zip(['intercept'] + feature_variables, model.params))
        
        # Create model metadata
        model_metadata = {
            'name': f"{target_variable}_model_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'target_variable': target_variable,
            'feature_variables': feature_variables,
            'coefficients': coefficients,
            'r_squared': model.rsquared,
            'p_values': dict(zip(['intercept'] + feature_variables, model.pvalues)),
            'last_trained_at': datetime.now().isoformat()
        }
        
        return model_metadata

    def predict(self, model_params: Dict, features: Dict) -> float:
        """
        Make predictions using a trained model
        
        Args:
            model_params: Dictionary containing model parameters
            features: Dictionary of feature values
        
        Returns:
            Predicted value for the target variable
        """
        # Extract coefficients
        intercept = model_params['coefficients']['intercept']
        feature_coefs = {k: v for k, v in model_params['coefficients'].items() 
                        if k != 'intercept'}
        
        # Calculate prediction
        prediction = intercept
        for feature, coef in feature_coefs.items():
            prediction += coef * features.get(feature, 0)
        
        return prediction

    def evaluate_model(self, model_params: Dict, test_data: List[Dict]) -> Dict:
        """
        Evaluate model performance on test data
        
        Args:
            model_params: Dictionary containing model parameters
            test_data: List of test data points
        
        Returns:
            Dictionary containing evaluation metrics
        """
        predictions = []
        actuals = []
        
        for item in test_data:
            features = {k: item[k] for k in model_params['feature_variables']}
            prediction = self.predict(model_params, features)
            predictions.append(prediction)
            actuals.append(item[model_params['target_variable']])
        
        # Calculate metrics
        mse = np.mean((np.array(predictions) - np.array(actuals)) ** 2)
        mae = np.mean(np.abs(np.array(predictions) - np.array(actuals)))
        
        return {
            'mse': mse,
            'mae': mae,
            'r_squared': model_params['r_squared']
        }
