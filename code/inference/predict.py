"""
================================================================================
Title: Model Inference Script – Run-ID & Docker-Aware Implementation

Course: M. Grum – Advanced AI-based Application Systems
Track: Data Science and Business Analytics Instructor: Prof. Dr. Marcus Grum
Chair: Junior Chair for Business Information Science, especially AI-based Application Systems
Institution: University of Potsdam, Germany
Authors: Gowtham Ramakrishna, Vaishnavi Vijaya

Description:
This script performs inference using trained machine learning models on new
network traffic data. It supports both Artificial Neural Network (ANN) and
Ordinary Least Squares (OLS) models.

Key Design Principles:
- Run-ID aware execution using LATEST_RUN.txt for model version resolution
- Docker-compatible path handling via environment-based configuration
- Reproducible and research-grade workflow design
- Modular and extensible architecture for future model integration
================================================================================
"""

import os
import sys
import json
import pickle
from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np
import joblib

try:
    import tensorflow as tf
except ImportError:
    print("Warning: TensorFlow not available. ANN inference will not work.")
    tf = None


class CyberAttackInference:
    """
    Inference engine for cyber attack detection.
    """

    def __init__(self, model_type="ann"):
        """
        Initialize inference engine.

        Args:
            model_type: 'ann' or 'ols'
        """
        self.model_type = model_type
        self.model = None
        self.scaler = None
        self.temperature = 1.0  # For temperature scaling (ANN)

        # -----------------------------
        # PATH STRATEGY (Docker + Local)
        # -----------------------------
        self.base_dir = Path(__file__).resolve().parents[2]

        self.models_dir = Path(
            os.getenv("MODELS_DIR", self.base_dir / "models")
        )

        self.activation_dir = Path(
            os.getenv("ACTIVATION_DIR", self.base_dir / "data" / "processed")
        )

        # Resolve run context
        self.run_id = self.get_latest_run_id()
        self.run_dir = self.models_dir / self.run_id

        self.ann_dir = self.run_dir / "ann"
        self.ols_dir = self.run_dir / "ols"

        # -----------------------------
        # Label mappings
        # -----------------------------
        self.attack_labels = {
            0: "Normal",
            1: "Attack (DoS/Probe/R2L/U2R)"
        }

    # -----------------------------
    # RUN REGISTRY
    # -----------------------------
    def get_latest_run_id(self):
        latest_file = self.models_dir / "LATEST_RUN.txt"

        if not latest_file.exists():
            raise FileNotFoundError(
                f"LATEST_RUN.txt not found in {self.models_dir}. Train a model first."
            )

        return latest_file.read_text().strip()

    # -----------------------------
    # MODEL LOADING
    # -----------------------------
    def load_model(self):
        print("=" * 60)
        print("STEP 1: LOADING MODEL")
        print("=" * 60)

        print(f"\n🧪 Active Run-ID: {self.run_id}")

        if self.model_type == "ann":
            if tf is None:
                print("❌ TensorFlow not available. Cannot load ANN model.")
                return False

            model_path = self.ann_dir / "best_model.h5"
            print(f"\n📦 Loading ANN model from: {model_path}")

            try:
                self.model = tf.keras.models.load_model(model_path)
                print("✅ ANN model loaded successfully")
                print(f"   Parameters: {self.model.count_params():,}")
                print(f"   Architecture: {len(self.model.layers)} layers")
            except Exception as e:
                print(f"❌ Error loading ANN model: {str(e)}")
                return False

        elif self.model_type == "ols":
            model_path = self.ols_dir / "currentOlsSolution.pkl"
            print(f"\n📦 Loading OLS model from: {model_path}")

            try:
                with open(model_path, "rb") as f:
                    self.model = pickle.load(f)
                print("✅ OLS model loaded successfully")
                print("   Algorithm: Logistic Regression")
                print(f"   Classes: {self.model.classes_}")
            except Exception as e:
                print(f"❌ Error loading OLS model: {str(e)}")
                return False
        else:
            print(f"❌ Unknown model type: {self.model_type}")
            return False

        return True

    # -----------------------------
    # PREPROCESSING ARTIFACTS
    # -----------------------------
    def load_preprocessing_artifacts(self):
        print("\n" + "=" * 60)
        print("STEP 2: LOADING PREPROCESSING ARTIFACTS")
        print("=" * 60)

        scaler_path = self.ann_dir / "scaler.pkl"
        print(f"\n📦 Loading scaler from: {scaler_path}")


        try:
            self.scaler = joblib.load(scaler_path)
            print("✅ Scaler loaded successfully")
        except Exception as e:
            print(f"❌ Failed to load scaler: {str(e)}")
            return False
        
        return True

    # -----------------------------
    # INPUT DATA
    # -----------------------------
    def load_activation_data(self):
        print("\n" + "=" * 60)
        print("STEP 3: LOADING ACTIVATION DATA")
        print("=" * 60)

        data_file = self.activation_dir / "activation_data.csv"
        print(f"\n📂 Loading activation data from: {data_file}")

        try:
            df = pd.read_csv(data_file)
            print(f"✅ Loaded {len(df)} records for inference")
            print(f"   Features: {len(df.columns)}")
            return df
        except Exception as e:
            print(f"❌ Error loading activation data: {str(e)}")
            return None

    # -----------------------------
    # PREPROCESSING
    # -----------------------------
    def preprocess_input(self, df):
        print("\n" + "=" * 60)
        print("STEP 4: PREPROCESSING INPUT")
        print("=" * 60)

        label_cols = [
            "label",
            "label_binary",
            "label_multiclass",
            "label_multiclass_encoded"
        ]

        feature_cols = [c for c in df.columns if c not in label_cols]
        X = df[feature_cols].values

        print("\n✅ Input prepared:")
        print(f"   Shape: {X.shape}")
        print(f"   Features: {len(feature_cols)}")

        print("\n🔧 Applying StandardScaler...")
        X = self.scaler.transform(X)

        return X

    # -----------------------------
    # PREDICTION
    # -----------------------------
    def predict(self, X):
        print("\n" + "=" * 60)
        print("STEP 5: MAKING PREDICTIONS")
        print("=" * 60)

        print(f"\n🔮 Running {self.model_type.upper()} inference on {len(X)} samples...")

        start_time = datetime.now()

        try:
            if self.model_type == "ann":
                # y_pred_proba = self.model.predict(X, verbose=0).flatten()
                # y_pred = (y_pred_proba > 0.5).astype(int)

                # Temperature-scaled ANN inference (NEW) Added by Gowtham
                logits_model = tf.keras.Model(
                    inputs=self.model.input,
                    outputs=self.model.layers[-1].input
                )

                logits = logits_model.predict(X, verbose=0).flatten()
                scaled_logits = logits / self.temperature
                y_pred_proba = tf.sigmoid(scaled_logits).numpy()

                y_pred = (y_pred_proba > 0.5).astype(int)

            elif self.model_type == "ols":
                y_pred = self.model.predict(X)
                y_pred_proba = self.model.predict_proba(X)[:, 1]

            end_time = datetime.now()
            inference_time = (end_time - start_time).total_seconds() * 1000

            print("✅ Predictions complete")
            print(f"   Inference time: {inference_time:.2f} ms")
            print(f"   Time per sample: {inference_time / len(X):.2f} ms")

            return {
                "predictions": y_pred,
                "probabilities": y_pred_proba,
                "inference_time_ms": inference_time
            }

        except Exception as e:
            print(f"❌ Error during prediction: {str(e)}")
            return None

    # -----------------------------
    # INTERPRETATION
    # -----------------------------
    def interpret_predictions(self, results):
        print("\n" + "=" * 60)
        print("STEP 6: INTERPRETING PREDICTIONS")
        print("=" * 60)

        predictions = results["predictions"]
        probabilities = results["probabilities"]

        interpretations = []

        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            interpretation = {
                "sample_id": i + 1,
                "prediction": int(pred),
                "label": self.attack_labels[int(pred)],
                "confidence": float(prob),
                "confidence_percent": f"{prob * 100:.2f}%",
                "verdict": "ATTACK DETECTED" if pred == 1 else "Normal Traffic",
                "severity": self._get_severity(prob, pred),
                "recommended_action": self._get_recommended_action(pred, prob)
            }

            interpretations.append(interpretation)

        return interpretations

    def _get_severity(self, confidence, prediction):
        if prediction == 0:
            return "None"
        if confidence > 0.95:
            return "Critical"
        elif confidence > 0.85:
            return "High"
        elif confidence > 0.70:
            return "Medium"
        else:
            return "Low"

    def _get_recommended_action(self, prediction, confidence):
        if prediction == 0:
            return "Continue monitoring"
        if confidence > 0.95:
            return "IMMEDIATE: Block source IP, isolate affected systems"
        elif confidence > 0.85:
            return "URGENT: Investigate and prepare countermeasures"
        elif confidence > 0.70:
            return "WARNING: Enhanced monitoring, collect evidence"
        else:
            return "ALERT: Review logs, verify with secondary systems"

    # -----------------------------
    # OUTPUT
    # -----------------------------
    def display_results(self, interpretations):
        print("\n" + "=" * 60)
        print("PREDICTION RESULTS")
        print("=" * 60)

        for interp in interpretations:
            print("\n" + "=" * 60)
            print(f"Sample #{interp['sample_id']}")
            print("=" * 60)
            print(f"Verdict:     {interp['verdict']}")
            print(f"Prediction:  {interp['label']}")
            print(f"Confidence:  {interp['confidence_percent']}")
            print(f"Severity:    {interp['severity']}")
            print(f"Action:      {interp['recommended_action']}")

        total = len(interpretations)
        attacks = sum(1 for i in interpretations if i["prediction"] == 1)
        normal = total - attacks

        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Run-ID:               {self.run_id}")
        print(f"Total samples:       {total}")
        print(f"Normal traffic:      {normal} ({normal / total * 100:.1f}%)")
        print(f"Attacks detected:   {attacks} ({attacks / total * 100:.1f}%)")

    def save_results(self, interpretations, output_file="predictions.json"):
        print(f"\n💾 Saving results to: {output_file}")

        output_data = {
            "run_id": self.run_id,
            "model_type": self.model_type,
            "model_path": str(
                self.ann_dir if self.model_type == "ann" else self.ols_dir
            ),
            "timestamp": datetime.now().isoformat(),
            "total_samples": len(interpretations),
            "predictions": interpretations
        }

        try:
            with open(output_file, "w") as f:
                json.dump(output_data, f, indent=2)
            print("✅ Results saved successfully")
        except Exception as e:
            print(f"⚠️  Could not save results: {str(e)}")

    # -----------------------------
    # PIPELINE
    # -----------------------------
    def run(self):
        print("=" * 60)
        print(f"CYBER ATTACK DETECTION - {self.model_type.upper()} INFERENCE")
        print("Course: M. Grum: Advanced AI-based Application Systems")
        print("University of Potsdam")
        print("=" * 60)

        if not self.load_model():
            return False

        if not self.load_preprocessing_artifacts():
            return False
        
        # Load temperature ONLY for ANN
        if self.model_type == "ann":
            self.load_temperature()

        df = self.load_activation_data()
        if df is None:
            return False

        X = self.preprocess_input(df)

        results = self.predict(X)
        if results is None:
            return False

        interpretations = self.interpret_predictions(results)

        self.display_results(interpretations)
        self.save_results(interpretations)

        print("\n" + "=" * 60)
        print("✅ INFERENCE COMPLETE!")
        print("=" * 60)

        return True
    
    def load_temperature(self):
        temp_path = self.ann_dir / "temperature.json"

        if temp_path.exists():
            try:
                with open(temp_path, "r") as f:
                    self.temperature = json.load(f)["temperature"]
                print(f"🌡️  Loaded temperature: {self.temperature:.4f}")
            except Exception:
                print("⚠️  Failed to load temperature. Using T=1.0")
        else:
            print("⚠️  No temperature file found. Using T=1.0")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Cyber Attack Detection Inference"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="ann",
        choices=["ann", "ols"],
        help="Model type to use for inference (default: ann)"
    )

    args = parser.parse_args()

    engine = CyberAttackInference(model_type=args.model)
    success = engine.run()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
