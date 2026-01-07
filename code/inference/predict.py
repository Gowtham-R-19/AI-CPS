"""
Model Inference Script - FULL IMPLEMENTATION
Course: M. Grum: Advanced AI-based Application Systems
University of Potsdam

This script performs inference using trained models on new network traffic data.
Supports both ANN and OLS models.

Author: V (ML Engineer)
Week: 5 (Subgoal 6: Docker Model Provision)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import pickle
import json
import sys
from datetime import datetime

try:
    import tensorflow as tf
except ImportError:
    print("Warning: TensorFlow not available. ANN inference will not work.")
    tf = None


class CyberAttackInference:
    """
    Inference engine for cyber attack detection.
    """
    
    def __init__(self, model_type='ann'):
        """
        Initialize inference engine.
        
        Args:
            model_type: 'ann' or 'ols'
        """
        self.model_type = model_type
        self.model = None
        self.scaler = None
        self.label_encoders = None
        
        # Paths (Docker volume paths)
        self.knowledge_base = Path('/tmp/knowledgeBase')
        self.activation_base = Path('/tmp/activationBase')
        self.learning_base = Path('/tmp/learningBase')
        
        # Attack type mapping
        self.attack_labels = {
            0: 'Normal',
            1: 'Attack (DoS/Probe/R2L/U2R)'
        }
        
        self.multiclass_labels = {
            0: 'Normal',
            1: 'DoS (Denial of Service)',
            2: 'Probe (Port Scanning)',
            3: 'R2L (Remote to Local)',
            4: 'U2R (User to Root)'
        }
        
    def load_model(self):
        """
        Load trained model from knowledge base.
        """
        print("="*60)
        print("STEP 1: LOADING MODEL")
        print("="*60)
        
        if self.model_type == 'ann':
            if tf is None:
                print("❌ TensorFlow not available. Cannot load ANN model.")
                return False
            
            model_path = self.knowledge_base / 'currentAiSolution.h5'
            print(f"\n📦 Loading ANN model from: {model_path}")
            
            try:
                self.model = tf.keras.models.load_model(model_path)
                print(f"✅ ANN model loaded successfully")
                print(f"   Parameters: {self.model.count_params():,}")
                print(f"   Architecture: {len(self.model.layers)} layers")
            except Exception as e:
                print(f"❌ Error loading ANN model: {str(e)}")
                return False
                
        elif self.model_type == 'ols':
            model_path = self.knowledge_base / 'currentOlsSolution.pkl'
            print(f"\n📦 Loading OLS model from: {model_path}")
            
            try:
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                print(f"✅ OLS model loaded successfully")
                print(f"   Algorithm: Logistic Regression")
                print(f"   Classes: {self.model.classes_}")
            except Exception as e:
                print(f"❌ Error loading OLS model: {str(e)}")
                return False
        else:
            print(f"❌ Unknown model type: {self.model_type}")
            return False
        
        return True
    
    def load_preprocessing_artifacts(self):
        """
        Load scaler and label encoders used during training.
        """
        print("\n" + "="*60)
        print("STEP 2: LOADING PREPROCESSING ARTIFACTS")
        print("="*60)
        
        # Try to load from learning base (where preprocessing artifacts should be)
        scaler_path = self.learning_base / 'train' / '../scaler.pkl'
        encoders_path = self.learning_base / 'train' / '../label_encoders.pkl'
        
        # Alternative: they might be in the activation base
        if not scaler_path.exists():
            scaler_path = Path('/tmp/processed/scaler.pkl')
        if not encoders_path.exists():
            encoders_path = Path('/tmp/processed/label_encoders.pkl')
        
        print(f"\n📦 Loading preprocessing artifacts...")
        
        # Load scaler
        try:
            with open(scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            print(f"✅ Scaler loaded")
        except Exception as e:
            print(f"⚠️  Could not load scaler: {str(e)}")
            print(f"   Will skip normalization (data should already be normalized)")
        
        # Load label encoders
        try:
            with open(encoders_path, 'rb') as f:
                self.label_encoders = pickle.load(f)
            print(f"✅ Label encoders loaded")
        except Exception as e:
            print(f"⚠️  Could not load label encoders: {str(e)}")
            print(f"   Will skip categorical encoding (data should already be encoded)")
        
        return True
    
    def load_activation_data(self):
        """
        Load data for inference from activation base.
        """
        print("\n" + "="*60)
        print("STEP 3: LOADING ACTIVATION DATA")
        print("="*60)
        
        data_file = self.activation_base / 'activation_data.csv'
        
        print(f"\n📂 Loading activation data from: {data_file}")
        
        try:
            df = pd.read_csv(data_file)
            print(f"✅ Loaded {len(df)} records for inference")
            
            # Show preview
            print(f"\n📊 Data preview:")
            print(f"   Records: {len(df)}")
            print(f"   Features: {len(df.columns)}")
            
            return df
        except Exception as e:
            print(f"❌ Error loading activation data: {str(e)}")
            return None
    
    def preprocess_input(self, df):
        """
        Preprocess input data to match training format.
        """
        print("\n" + "="*60)
        print("STEP 4: PREPROCESSING INPUT")
        print("="*60)
        
        # Remove label columns if present
        label_cols = ['label', 'label_binary', 'label_multiclass', 'label_multiclass_encoded']
        feature_cols = [col for col in df.columns if col not in label_cols]
        
        X = df[feature_cols].values
        
        print(f"\n✅ Input prepared:")
        print(f"   Shape: {X.shape}")
        print(f"   Features: {len(feature_cols)}")
        
        # Check if data needs normalization
        if self.scaler and (X.max() > 1.1 or X.min() < -0.1):
            print(f"\n🔧 Applying normalization...")
            X = self.scaler.transform(X)
            print(f"   ✅ Data normalized to [0, 1] range")
        else:
            print(f"\n✓ Data already normalized or scaler unavailable")
        
        return X
    
    def predict(self, X):
        """
        Make predictions using loaded model.
        """
        print("\n" + "="*60)
        print("STEP 5: MAKING PREDICTIONS")
        print("="*60)
        
        print(f"\n🔮 Running {self.model_type.upper()} inference on {len(X)} samples...")
        
        start_time = datetime.now()
        
        try:
            if self.model_type == 'ann':
                # ANN prediction
                y_pred_proba = self.model.predict(X, verbose=0).flatten()
                y_pred = (y_pred_proba > 0.5).astype(int)
                
            elif self.model_type == 'ols':
                # OLS prediction
                y_pred = self.model.predict(X)
                y_pred_proba = self.model.predict_proba(X)[:, 1]  # Probability of attack
            
            end_time = datetime.now()
            inference_time = (end_time - start_time).total_seconds() * 1000  # Convert to ms
            
            print(f"✅ Predictions complete")
            print(f"   Inference time: {inference_time:.2f}ms")
            print(f"   Time per sample: {inference_time/len(X):.2f}ms")
            
            return {
                'predictions': y_pred,
                'probabilities': y_pred_proba,
                'inference_time_ms': inference_time
            }
            
        except Exception as e:
            print(f"❌ Error during prediction: {str(e)}")
            return None
    
    def interpret_predictions(self, results):
        """
        Interpret and explain predictions.
        """
        print("\n" + "="*60)
        print("STEP 6: INTERPRETING PREDICTIONS")
        print("="*60)
        
        predictions = results['predictions']
        probabilities = results['probabilities']
        
        interpretations = []
        
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            interpretation = {
                'sample_id': i + 1,
                'prediction': int(pred),
                'label': self.attack_labels[pred],
                'confidence': float(prob),
                'confidence_percent': f"{prob*100:.2f}%",
                'verdict': 'ATTACK DETECTED' if pred == 1 else 'Normal Traffic',
                'severity': self._get_severity(prob, pred)
            }
            
            # Add recommended action
            interpretation['recommended_action'] = self._get_recommended_action(pred, prob)
            
            interpretations.append(interpretation)
        
        return interpretations
    
    def _get_severity(self, confidence, prediction):
        """
        Determine severity level based on confidence.
        """
        if prediction == 0:  # Normal
            return 'None'
        
        if confidence > 0.95:
            return 'Critical'
        elif confidence > 0.85:
            return 'High'
        elif confidence > 0.70:
            return 'Medium'
        else:
            return 'Low'
    
    def _get_recommended_action(self, prediction, confidence):
        """
        Recommend action based on prediction and confidence.
        """
        if prediction == 0:  # Normal
            return 'Continue monitoring'
        
        # Attack detected
        if confidence > 0.95:
            return 'IMMEDIATE: Block source IP, isolate affected systems'
        elif confidence > 0.85:
            return 'URGENT: Investigate and prepare countermeasures'
        elif confidence > 0.70:
            return 'WARNING: Enhanced monitoring, collect evidence'
        else:
            return 'ALERT: Review logs, verify with secondary systems'
    
    def display_results(self, interpretations):
        """
        Display prediction results in a clear format.
        """
        print("\n" + "="*60)
        print("PREDICTION RESULTS")
        print("="*60)
        
        for interp in interpretations:
            print(f"\n{'='*60}")
            print(f"Sample #{interp['sample_id']}")
            print(f"{'='*60}")
            print(f"Verdict:     {interp['verdict']}")
            print(f"Prediction:  {interp['label']}")
            print(f"Confidence:  {interp['confidence_percent']}")
            print(f"Severity:    {interp['severity']}")
            print(f"Action:      {interp['recommended_action']}")
        
        # Summary statistics
        print(f"\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        
        total = len(interpretations)
        attacks = sum(1 for i in interpretations if i['prediction'] == 1)
        normal = total - attacks
        
        print(f"Total samples analyzed: {total}")
        print(f"Normal traffic:         {normal} ({normal/total*100:.1f}%)")
        print(f"Attacks detected:       {attacks} ({attacks/total*100:.1f}%)")
        
        if attacks > 0:
            avg_confidence = np.mean([i['confidence'] for i in interpretations if i['prediction'] == 1])
            print(f"Average attack confidence: {avg_confidence*100:.2f}%")
    
    def save_results(self, interpretations, output_file='predictions.json'):
        """
        Save predictions to file.
        """
        print(f"\n💾 Saving results to: {output_file}")
        
        output_data = {
            'model_type': self.model_type,
            'timestamp': datetime.now().isoformat(),
            'total_samples': len(interpretations),
            'predictions': interpretations
        }
        
        try:
            with open(output_file, 'w') as f:
                json.dump(output_data, f, indent=2)
            print(f"✅ Results saved successfully")
        except Exception as e:
            print(f"⚠️  Could not save results: {str(e)}")
    
    def run(self):
        """
        Execute complete inference pipeline.
        """
        print("="*60)
        print(f"CYBER ATTACK DETECTION - {self.model_type.upper()} INFERENCE")
        print("Course: M. Grum: Advanced AI-based Application Systems")
        print("University of Potsdam")
        print("="*60)
        
        # Step 1: Load model
        if not self.load_model():
            print("\n❌ Failed to load model. Exiting.")
            return False
        
        # Step 2: Load preprocessing artifacts
        self.load_preprocessing_artifacts()
        
        # Step 3: Load activation data
        df = self.load_activation_data()
        if df is None:
            print("\n❌ Failed to load activation data. Exiting.")
            return False
        
        # Step 4: Preprocess input
        X = self.preprocess_input(df)
        
        # Step 5: Make predictions
        results = self.predict(X)
        if results is None:
            print("\n❌ Prediction failed. Exiting.")
            return False
        
        # Step 6: Interpret predictions
        interpretations = self.interpret_predictions(results)
        
        # Display results
        self.display_results(interpretations)
        
        # Save results
        self.save_results(interpretations)
        
        print("\n" + "="*60)
        print("✅ INFERENCE COMPLETE!")
        print("="*60)
        
        return True


def main():
    """
    Main entry point.
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Cyber Attack Detection Inference'
    )
    parser.add_argument(
        '--model',
        type=str,
        default='ann',
        choices=['ann', 'ols'],
        help='Model type to use for inference (default: ann)'
    )
    
    args = parser.parse_args()
    
    # Create and run inference engine
    engine = CyberAttackInference(model_type=args.model)
    success = engine.run()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()