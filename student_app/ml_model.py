import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

class CoursePredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.label_encoders = {
            'gender': LabelEncoder(),
            'interest': LabelEncoder(),
            'course': LabelEncoder()
        }
        self.model_path = os.path.join(os.path.dirname(__file__), 'course_predictor_model.joblib')
        self.is_trained = False
        self.model_metrics = {}

    def preprocess_data(self, ages, genders, interests):
        try:
            # Validate input data
            if len(ages) != len(genders) or len(ages) != len(interests):
                raise ValueError("Input arrays must have the same length")
            
            if not all(isinstance(age, (int, float)) for age in ages):
                raise ValueError("Ages must be numeric values")

            genders_encoded = self.label_encoders['gender'].fit_transform(genders)
            interests_encoded = self.label_encoders['interest'].fit_transform(interests)
            return np.array(list(zip(ages, genders_encoded, interests_encoded)))
        except Exception as e:
            raise ValueError(f"Error preprocessing data: {str(e)}")

    def train(self, ages, genders, interests, courses):
        """Train the model with student data and perform validation"""
        try:
            X = self.preprocess_data(ages, genders, interests)
            y = self.label_encoders['course'].fit_transform(courses)
            
            # Count minimum samples per class
            from collections import Counter
            class_counts = Counter(y)
            min_samples = min(class_counts.values())
            
            # Adjust number of CV splits based on minimum samples
            n_splits = min(3, min_samples)  # Use maximum 3 splits, or less if we have few samples
            
            if n_splits < 2:
                # If we have too few samples, skip cross-validation
                self.model.fit(X, y)
                y_pred = self.model.predict(X)
                self.model_metrics['training_accuracy'] = accuracy_score(y, y_pred)
                self.model_metrics['classification_report'] = classification_report(y, y_pred)
                self.model_metrics['cv_mean'] = self.model_metrics['training_accuracy']
                self.model_metrics['cv_std'] = 0.0
            else:
                # Perform cross-validation with adjusted n_splits
                cv_scores = cross_val_score(self.model, X, y, cv=n_splits)
                self.model_metrics['cv_scores'] = cv_scores
                self.model_metrics['cv_mean'] = cv_scores.mean()
                self.model_metrics['cv_std'] = cv_scores.std()
                
                # Train the final model
                self.model.fit(X, y)
                y_pred = self.model.predict(X)
                self.model_metrics['training_accuracy'] = accuracy_score(y, y_pred)
                self.model_metrics['classification_report'] = classification_report(y, y_pred)
            
            self.is_trained = True
            self.save_model()
            
            return {
                'success': True,
                'metrics': self.model_metrics
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def predict(self, age, gender, interest):
        """Predict course for a single student with input validation"""
        if not self.is_trained:
            raise ValueError("Model needs to be trained or loaded first")
            
        try:
            # Validate inputs
            if not isinstance(age, (int, float)):
                raise ValueError("Age must be a numeric value")
            
            if gender not in self.label_encoders['gender'].classes_:
                raise ValueError(f"Invalid gender. Must be one of {self.label_encoders['gender'].classes_}")
            
            # Fit transform for new interest if it's not in the existing classes
            if interest not in self.label_encoders['interest'].classes_:
                # Update the label encoder with the new interest
                new_classes = list(self.label_encoders['interest'].classes_) + [interest]
                self.label_encoders['interest'].classes_ = np.array(new_classes)
            
            gender_encoded = self.label_encoders['gender'].transform([gender])[0]
            interest_encoded = self.label_encoders['interest'].transform([interest])[0]
            X = np.array([[age, gender_encoded, interest_encoded]])
            prediction = self.model.predict(X)
            
            # Get prediction probabilities
            probabilities = self.model.predict_proba(X)[0]
            max_prob = max(probabilities)
            
            return {
                'predicted_course': self.label_encoders['course'].inverse_transform(prediction)[0],
                'confidence': float(max_prob),
                'success': True
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def save_model(self):
        """Save the trained model, encoders, and metrics"""
        model_data = {
            'model': self.model,
            'label_encoders': self.label_encoders,
            'is_trained': self.is_trained,
            'model_metrics': self.model_metrics
        }
        joblib.dump(model_data, self.model_path)

    def load_model(self):
        """Load a trained model with validation"""
        try:
            if os.path.exists(self.model_path):
                model_data = joblib.load(self.model_path)
                self.model = model_data['model']
                self.label_encoders = model_data['label_encoders']
                self.is_trained = model_data.get('is_trained', False)
                self.model_metrics = model_data.get('model_metrics', {})
                return True
            return False
        except Exception as e:
            self.is_trained = False
            raise ValueError(f"Error loading model: {str(e)}")

    def get_model_info(self):
        """Get information about the trained model"""
        if not self.is_trained:
            return {
                'status': 'Not trained',
                'metrics': None
            }
        return {
            'status': 'Trained',
            'metrics': self.model_metrics,
            'features': {
                'genders': list(self.label_encoders['gender'].classes_),
                'interests': list(self.label_encoders['interest'].classes_),
                'courses': list(self.label_encoders['course'].classes_)
            }
        }