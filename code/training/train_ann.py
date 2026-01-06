"""
ANN Model Training Script
Course: M. Grum: Advanced AI-based Application Systems
University of Potsdam

This script trains a neural network for network intrusion detection.

NOTE: This is a TEMPLATE for Subgoal 1.
Full implementation will be done in Subgoal 4 (Week 4).
"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_training_data():
    """
    Load preprocessed training data.
    """
    print("📂 Loading training data...")
    
    data_file = Path("../../data/processed/training_data.csv")
    
    if not data_file.exists():
        print(f"❌ Training data not found: {data_file}")
        print("   Run preprocessing first: python code/preprocessing/preprocess_data.py")
        return None
    
    df = pd.read_csv(data_file)
    print(f"✅ Loaded {len(df)} training records")
    
    return df


def build_ann_model():
    """
    Build ANN architecture.
    
    Architecture (planned):
    - Input Layer: 41 features
    - Hidden Layer 1: 64 neurons, ReLU, Dropout(0.3)
    - Hidden Layer 2: 32 neurons, ReLU, Dropout(0.2)
    - Output Layer: 1 neuron (binary) or 5 neurons (multi-class), Sigmoid/Softmax
    
    TODO: Implement in Week 4 (Subgoal 4)
    """
    print("\n🧠 Building ANN model...")
    print("   [TEMPLATE] Full implementation in Subgoal 4")
    
    # Placeholder for model architecture
    model_config = {
        'input_features': 41,
        'hidden_layer_1': 64,
        'hidden_layer_2': 32,
        'output_neurons': 1,  # or 5 for multi-class
        'activation_hidden': 'relu',
        'activation_output': 'sigmoid',  # or 'softmax' for multi-class
        'dropout_rate': 0.3
    }
    
    return model_config


def train_model(model_config, training_data):
    """
    Train the ANN model.
    
    TODO: Implement in Week 4 (Subgoal 4)
    """
    print("\n🏋️  Training model...")
    print("   [TEMPLATE] Full implementation in Subgoal 4")
    
    # Placeholder training configuration
    training_config = {
        'epochs': 50,
        'batch_size': 128,
        'optimizer': 'adam',
        'learning_rate': 0.001,
        'loss_function': 'binary_crossentropy',
        'validation_split': 0.2
    }
    
    print(f"   Training configuration: {training_config}")
    return None


def evaluate_model():
    """
    Evaluate model performance.
    
    TODO: Implement in Week 4 (Subgoal 4)
    """
    print("\n📊 Evaluating model...")
    print("   [TEMPLATE] Full implementation in Subgoal 4")
    
    # Expected metrics
    expected_metrics = {
        'accuracy': '92-98%',
        'precision': '92-96%',
        'recall': '95-98%',
        'f1_score': '0.93-0.97'
    }
    
    print(f"   Expected metrics: {expected_metrics}")
    return expected_metrics


def main():
    """
    Main training pipeline.
    """
    print("="*60)
    print("ANN MODEL TRAINING (TEMPLATE)")
    print("Course: M. Grum: Advanced AI-based Application Systems")
    print("University of Potsdam")
    print("="*60)
    
    print("\n⚠️  This is a TEMPLATE for Subgoal 1 (Git Setup)")
    print("   Full implementation will be done in Subgoal 4 (Week 4)")
    print("   Current focus: Establishing project structure\n")
    
    # Load data (this will work if preprocessing is complete)
    training_data = load_training_data()
    
    if training_data is not None:
        # Build model configuration
        model_config = build_ann_model()
        
        # Train model (placeholder)
        trained_model = train_model(model_config, training_data)
        
        # Evaluate model (placeholder)
        metrics = evaluate_model()
    
    print("\n" + "="*60)
    print("TEMPLATE SCRIPT COMPLETE")
    print("NEXT: Continue with Subgoal 2 (Data Scraping)")
    print("="*60)


if __name__ == "__main__":
    main()