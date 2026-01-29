"""
================================================================================
Title: Model Inference Script — Cyber Attack Detection (Docker-Aware Runtime)

Course: M. Grum – Advanced AI-based Application Systems
Track: Data Science and Business Analytics
Instructor: Prof. Dr. Marcus Grum
Chair: Junior Chair for Business Information Science, especially AI-based Application Systems
Institution: University of Potsdam, Germany
Author: Vaishnavi Vijaya, Gowtham Ramakrishna

Purpose:
- Apply trained ANN or OLS models to activation data for cyber attack detection
- Enforce professor-mandated Docker path usage for model and data access
- Produce structured, interpretable, and confidence-based inference outputs

Important:
- Active execution strictly follows Docker-exposed paths:
    /tmp/activationBase/activation_data.csv
    /tmp/knowledgeBase/currentAiSolution.h5
    /tmp/knowledgeBase/currentOlsSolution.pkl

Description:
This script implements a Docker-aware inference runtime that loads trained
ANN and OLS model artifacts and optional preprocessing components from
container-mounted paths, preprocesses activation data, executes deterministic
prediction logic, and reports labeled risk levels and confidence scores for
each sample.

Key Design Principles:
- Strict compliance with standardized /tmp container paths
- Reproducible preprocessing via optional scaler integration
- Transparent and deterministic prediction and reporting workflow

================================================================================
"""

# ==========================================================
# SILENCE TENSORFLOW & SYSTEM NOISE (COURSE SUBMISSION)
# ==========================================================
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import logging
logging.getLogger("tensorflow").setLevel(logging.ERROR)

# ==========================================================
# STANDARD IMPORTS
# ==========================================================
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
    print("Warning: TensorFlow not available.")
    tf = None


class CyberAttackInference:
    """
    Inference engine for cyber attack detection.
    """

    def __init__(self, model_type="ann"):
        self.model_type = model_type
        self.model = None # Loaded model
        self.scaler = None # For preprocessing

        self.temperature = 1.3   # recommended range: 1.2–1.5
        self.eps = 1e-6          # numerical stability

        # ---- Risk thresholds ----
        self.risk_levels = [
            (0.20, "Very Low"),
            (0.40, "Low"),
            (0.60, "Medium"),
            (0.80, "High"),
            (1.01, "Critical"),
        ]
        


        # ==========================================================
        # PATH STRATEGY
        # ==========================================================

        # -------- LOCAL / RESEARCH MODE (COMMENTED - DO NOT DELETE) --------
        # self.base_dir = Path(__file__).resolve().parents[2]
        #
        # self.models_dir = Path(
        #     os.getenv("MODELS_DIR", self.base_dir / "models")
        # )
        #
        # self.activation_dir = Path(
        #     os.getenv("ACTIVATION_DIR", self.base_dir / "data" / "processed")
        # )

        # -------- COURSE SUBMISSION MODE (ACTIVE) --------
        # As required by assignment: Docker images expose /tmp paths
        self.models_dir = Path("/tmp/knowledgeBase")
        self.activation_dir = Path("/tmp/activationBase")

        print(f"📁 MODELS_DIR: {self.models_dir}") 
        print(f"📁 ACTIVATION_DIR: {self.activation_dir}")

        # ==========================================================
        # RUN REGISTRY
        # ==========================================================

        # -------- ADVANCED RUN HISTORY MODE (COMMENTED - FUTURE USE) --------
        # self.run_id = self.get_latest_run_id()
        # self.run_dir = self.models_dir / self.run_id
        # self.ann_dir = self.run_dir / "ann"
        # self.ols_dir = self.run_dir / "ols"

        # -------- COURSE SUBMISSION MODE (ACTIVE) --------
        # self.run_id = "course_submission" # Future use
        self.ann_dir = self.models_dir
        self.ols_dir = self.models_dir

        # ==========================================================
        # LABEL MAPPING
        # ==========================================================
        self.attack_labels = {
            0: "Normal", 
            1: "Attack"
        } 

    # ==========================================================
    # RUN REGISTRY (FUTURE USE - COMMENTED)
    # ==========================================================
    def get_latest_run_id(self):
        latest_file = self.models_dir / "LATEST_RUN.txt"
        if not latest_file.exists():
            raise FileNotFoundError("LATEST_RUN.txt not found.")
        return latest_file.read_text().strip()

    # ==========================================================
    # STEP 1: MODEL LOADING
    # ==========================================================
    def load_model(self):
        print("\n" + "=" * 60)
        print("STEP 1: LOADING MODEL")
        print("=" * 60)
        # print(f"🧪 Active Run-ID: {self.run_id}")

        if self.model_type == "ann":
            if tf is None:
                print("❌ TensorFlow not available.")
                return False

            # Local mode (commented)
            # model_path = self.ann_dir / "best_model.h5"

            # Course mode (active)
            model_path = self.ann_dir / "currentAiSolution.h5"

            print(f"📦 Loading ANN model from: {model_path}")

            try:
                self.model = tf.keras.models.load_model(model_path)
                print("✅ ANN model loaded successfully")
            except Exception as e:
                print(f"❌ ANN load failed: {e}")
                return False

        elif self.model_type == "ols":
            model_path = self.ols_dir / "currentOlsSolution.pkl"
            print(f"📦 Loading OLS model from: {model_path}")

            try:
                with open(model_path, "rb") as f:
                    self.model = pickle.load(f)
                print("✅ OLS model loaded successfully")
            except Exception as e:
                print(f"❌ OLS load failed: {e}")
                return False

        return True

    # ==========================================================
    # STEP 2: PREPROCESSING ARTIFACTS
    # ==========================================================
    def load_preprocessing_artifacts(self):
        print("\n" + "=" * 60)
        print("STEP 2: LOADING PREPROCESSING ARTIFACTS")
        print("=" * 60)

        # Local mode (commented)
        # scaler_path = self.ann_dir / "scaler.pkl"

        # Course mode (optional)
        scaler_path = self.models_dir / "scaler.pkl"
        print(f"📦 Looking for scaler at: {scaler_path}")

        if not scaler_path.exists():
            print("⚠️  No scaler found. Skipping scaling.")
            self.scaler = None
            return True

        self.scaler = joblib.load(scaler_path)
        print("✅ Scaler loaded successfully")
        return True

    # ==========================================================
    # STEP 3: INPUT DATA
    # ==========================================================
    def load_activation_data(self):
        print("\n" + "=" * 60)
        print("STEP 3: LOADING ACTIVATION DATA")
        print("=" * 60)

        data_file = self.activation_dir / "activation_data.csv"
        print(f"📂 Loading activation data from: {data_file}")

        df = pd.read_csv(data_file)
        print(f"✅ Loaded {len(df)} sample(s)")
        return df

    # ==========================================================
    # STEP 4: PREPROCESSING (VISIBLE & STRUCTURED)
    # ==========================================================
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
        X_raw = df[feature_cols].values

        print(f"Input samples : {X_raw.shape[0]}")
        print(f"Feature count : {X_raw.shape[1]}")
        print("\n🔎 Raw features (sample 1, first 10):")
        print(X_raw[0][:10])

        if self.scaler is not None:
            X_scaled = self.scaler.transform(X_raw)
            # --- SAFETY FOR OLS (critical) ---
            X_scaled = np.nan_to_num(
                X_scaled,
                nan=0.0,
                posinf=0.0,
                neginf=0.0
            )
            print("\n🔧 Scaling applied (StandardScaler)")
            print("🔎 Scaled features (sample 1, first 10):")
            print(X_scaled[0][:10])
            return X_scaled, True
        else:
            print("\n⚠️  No scaling applied")
            return X_raw, False

    # ==========================================================
    # STEP 5: PREDICTION
    # ==========================================================
    def predict(self, X):
        print("\n" + "=" * 60)
        print("STEP 5: MAKING PREDICTIONS")
        print("=" * 60)

        start = datetime.now()

        if self.model_type == "ann":
            # probs = self.model.predict(X, verbose=0).flatten()
            # preds = (probs > 0.5).astype(int)

            raw_probs = self.model.predict(X, verbose=0).flatten()

            # Convert probability → logits
            logits = np.log((raw_probs + self.eps) / (1 - raw_probs + self.eps))

            # Temperature scaling
            scaled_logits = logits / self.temperature
            probs = 1 / (1 + np.exp(-scaled_logits))

            # Clip only for numerical safety
            probs = np.clip(probs, self.eps, 1 - self.eps)

            preds = (probs > 0.5).astype(int)


        else:
            preds = self.model.predict(X)
            probs = self.model.predict_proba(X)[:, 1]

        elapsed = (datetime.now() - start).total_seconds() * 1000
        print(f"Inference time: {elapsed:.2f} ms")

        return preds, probs
    
    # ==========================================================
    # RISK LEVEL MAPPING
    # =========================================================
    def get_risk_level(self, prob):
        for threshold, level in self.risk_levels:
            if prob < threshold:
                return level
        return "Unknown"


    # ==========================================================
    # STEP 6: STRUCTURED OUTPUT
    # ==========================================================
    def display_results(self, preds, probs, scaling_used):
        print("\n" + "=" * 70)
        print("FINAL INFERENCE RESULTS")
        print("=" * 70)
    
        header = f"{'Sample':<8}{'Prediction':<12}{'Confidence':<12}{'Risk Level'}"
        print(header)
        print("-" * len(header))
    
        for i, (p, pr) in enumerate(zip(preds, probs)):
            label = self.attack_labels[int(p)]
            risk = self.get_risk_level(pr)
            print(f"{i+1:<8}{label:<12}{pr*100:>7.2f}%     {risk}")
    
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"Total samples : {len(preds)}")
        print(f"Scaling used  : {'Yes' if scaling_used else 'No'}")
    
        print("\nMODEL INTERPRETATION")
        print("-" * 70)
        if self.model_type == "ann":
            print("ANN: Non-linear classifier with high-confidence decision boundaries")
            print("Note: Confidence saturation is expected for strongly separable samples")
        else:
            print("OLS: Linear baseline model with smoother probability estimates")
    
    # ==========================================================
    # PIPELINE
    # ==========================================================
    def run(self):
        print("\n" + "=" * 60)
        print("CYBER ATTACK DETECTION - INFERENCE")
        print("Course: M. Grum – Advanced AI-based Application Systems")
        print("=" * 60)

        if not self.load_model():
            return False

        self.load_preprocessing_artifacts()
        df = self.load_activation_data()

        X, scaling_used = self.preprocess_input(df)
        preds, probs = self.predict(X)
        self.display_results(preds, probs, scaling_used)

        print("\n✅ INFERENCE COMPLETE")
        return True


# ==========================================================
# MAIN
# ==========================================================
def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=["ann", "ols"], default="ann")
    args = parser.parse_args()

    engine = CyberAttackInference(model_type=args.model)
    success = engine.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
