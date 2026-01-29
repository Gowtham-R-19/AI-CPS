"""
================================================================================
Title: ANN Model Training Script — Full Implementation

Course: M. Grum – Advanced AI-based Application Systems
Track: Data Science and Business Analytics
Instructor: Prof. Dr. Marcus Grum
Chair: Junior Chair for Business Information Science, especially AI-based Application Systems
Institution: University of Potsdam, Germany
Authors: Gowtham Ramakrishna, Vaishnavi Vijaya

Description:
This script implements a deep Artificial Neural Network (ANN) training pipeline
for binary network intrusion detection, including feature scaling, model
architecture configuration, training orchestration, and performance evaluation
under a reproducible and research-grade workflow.

Key Design Principles:
- Deterministic training and evaluation for reproducible experiments
- Modular ANN architecture design for rapid experimentation
- Integrated performance tracking and metric reporting
- Seamless handoff to model inference and deployment pipelines

================================================================================
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

from sklearn.preprocessing import StandardScaler
import joblib

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_curve, auc,
   precision_recall_curve
)

# -----------------------------
# Reproducibility Controls
# -----------------------------
# Fix random behavior across Python, NumPy, and TensorFlow
# This ensures the same dataset + same code = same results
import random
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

class CyberAttackANN:
    """
    Deep Neural Network for Cyber Attack Detection.
    """
    
    def __init__(self, model_type='binary'):
        """
        Initialize the ANN trainer.
        
        Args:
            model_type: 'binary' or 'multiclass'
        """
        self.model_type = model_type
        self.model = None
        self.history = None
        
        # Paths
        self.data_dir = Path(__file__).parent.parent.parent / "data" / "processed"
        self.model_dir = Path(__file__).parent.parent.parent / "models"
        self.viz_dir = Path(__file__).parent.parent.parent / "visualizations"
        
        # # Create directories
        # self.model_dir.mkdir(parents=True, exist_ok=True)
        # self.viz_dir.mkdir(parents=True, exist_ok=True)

        # -----------------------------
        # Create & Bind Run ID (Source of Truth) Added by Gowtham
        # -----------------------------
        self.run_id = datetime.now().strftime("run_%Y-%m-%d_%H-%M-%S")

        base_dir = Path(__file__).parent.parent.parent

        self.model_dir = base_dir / "models" / self.run_id / "ann"
        self.viz_dir = base_dir / "visualizations" / self.run_id / "ann"

        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.viz_dir.mkdir(parents=True, exist_ok=True)

        # Write latest run pointer
        run_id_file = base_dir / "models" / "LATEST_RUN.txt"
        run_id_file.write_text(self.run_id)

        print(f"🆔 Run ID: {self.run_id}")
        print(f"📁 ANN model dir: {self.model_dir}")
        print(f"📁 ANN viz dir: {self.viz_dir}")

        # Training statistics
        self.stats = {
            'model_type': model_type,
            'start_time': None,
            'end_time': None,
            'training_time_seconds': 0,
            'epochs_trained': 0,
            'best_epoch': 0,
            'train_accuracy': 0,
            'val_accuracy': 0,
            'test_accuracy': 0,
            'test_precision': 0,
            'test_recall': 0,
            'test_f1': 0,
        }
    
    def load_data(self):
        """
        Load preprocessed training and testing data.
        """
        print("="*60)
        print("STEP 1: LOADING DATA")
        print("="*60)
        
        train_file = self.data_dir / "training_data.csv"
        test_file = self.data_dir / "test_data.csv"
        
        print(f"\n📂 Loading training data...")
        df_train = pd.read_csv(train_file)
        print(f"✅ Loaded {len(df_train):,} training records")
        
        print(f"\n📂 Loading testing data...")
        df_test = pd.read_csv(test_file)
        print(f"✅ Loaded {len(df_test):,} testing records")
        
        # Separate features and labels
        label_col = 'label_binary' if self.model_type == 'binary' else 'label_multiclass_encoded'
        exclude_cols = ['label', 'label_binary', 'label_multiclass', 'label_multiclass_encoded']
        
        feature_cols = [col for col in df_train.columns if col not in exclude_cols]
        
        # X_train = df_train[feature_cols].values
        # y_train = df_train[label_col].values
        # 
        # X_test = df_test[feature_cols].values
        # y_test = df_test[label_col].values

        # -----------------------------
        # Feature Scaling
        # -----------------------------
        scaler = StandardScaler()

        X_train = scaler.fit_transform(df_train[feature_cols].values)
        y_train = df_train[label_col].values

        X_test = scaler.transform(df_test[feature_cols].values)
        y_test = df_test[label_col].values

        # Save scaler for inference
        scaler_path = self.model_dir / "scaler.pkl"
        joblib.dump(scaler, scaler_path)

        print(f"💾 Feature scaler saved to: {scaler_path}")
        
        print(f"\n📊 Data shapes:")
        print(f"   X_train: {X_train.shape}")
        print(f"   y_train: {y_train.shape}")
        print(f"   X_test: {X_test.shape}")
        print(f"   y_test: {y_test.shape}")
        
        # Show label distribution
        print(f"\n📊 Label distribution (training):")
        unique, counts = np.unique(y_train, return_counts=True)
        for label, count in zip(unique, counts):
            print(f"   Class {label}: {count:,} ({count/len(y_train)*100:.1f}%)")
        
        return X_train, y_train, X_test, y_test, feature_cols
    
    def build_model(self, input_dim, output_dim=1):
        """
        Build the neural network architecture.
        
        Architecture:
        - Input Layer: input_dim neurons
        - Hidden Layer 1: 64 neurons, ReLU, Dropout(0.3)
        - Hidden Layer 2: 32 neurons, ReLU, Dropout(0.2)
        - Output Layer: output_dim neurons, Sigmoid/Softmax
        """
        print("\n" + "="*60)
        print("STEP 2: BUILDING NEURAL NETWORK")
        print("="*60)
        
        print(f"\n🧠 Architecture:")
        print(f"   Input Layer: {input_dim} features")
        print(f"   Hidden Layer 1: 64 neurons (ReLU + Dropout 0.3)")
        print(f"   Hidden Layer 2: 32 neurons (ReLU + Dropout 0.2)")
        
        if self.model_type == 'binary':
            print(f"   Output Layer: 1 neuron (Sigmoid)")
            output_activation = 'sigmoid'
            output_neurons = 1
        else:
            print(f"   Output Layer: {output_dim} neurons (Softmax)")
            output_activation = 'softmax'
            output_neurons = output_dim
        
        # Build model
        model = models.Sequential([
            # Input layer
            layers.Input(shape=(input_dim,)),
            
            # Hidden layer 1
            layers.Dense(64, activation='relu', name='hidden1'),
            layers.Dropout(0.3, name='dropout1'),
            
            # Hidden layer 2
            layers.Dense(32, activation='relu', name='hidden2'),
            layers.Dropout(0.2, name='dropout2'),
            
            # Output layer
            layers.Dense(output_neurons, activation=output_activation, name='output')
        ])
        
        # Compile model
        if self.model_type == 'binary':
            loss = 'binary_crossentropy'
            metrics = ['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
        else:
            loss = 'sparse_categorical_crossentropy'
            metrics = ['accuracy']
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss=loss,
            metrics=metrics
        )
        
        print(f"\n📋 Model Summary:")
        model.summary()
        
        # Count parameters
        total_params = model.count_params()
        print(f"\n📊 Total parameters: {total_params:,}")
        
        self.model = model
        return model
    
    def train_model(self, X_train, y_train, X_test, y_test):
        """
        Train the neural network.
        """
        print("\n" + "="*60)
        print("STEP 3: TRAINING NEURAL NETWORK")
        print("="*60)
        
        # Training configuration
        batch_size = 128
        epochs = 50
        validation_split = 0.2
        
        print(f"\n⚙️  Training Configuration:")
        print(f"   Batch size: {batch_size}")
        print(f"   Max epochs: {epochs}")
        print(f"   Validation split: {validation_split}")
        print(f"   Optimizer: Adam (lr=0.001)")
        
        # Callbacks
        callbacks = [
            # Early stopping
            EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True,
                verbose=1
            ),
            
            # Model checkpoint
            ModelCheckpoint(
                str(self.model_dir / 'best_model.h5'),
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            ),
            
            # Reduce learning rate on plateau
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=0.00001,
                verbose=1
            )
        ]
        
        print(f"\n🏋️  Starting training...")
        print(f"   This will take 10-15 minutes...\n")
        
        # Record start time
        self.stats['start_time'] = datetime.now().isoformat()
        start_time = datetime.now()
        
        # Train model
        self.history = self.model.fit(
            X_train, y_train,
            batch_size=batch_size,
            epochs=epochs,
            validation_split=validation_split,
            callbacks=callbacks,
            verbose=1
        )
        
        # Record end time
        end_time = datetime.now()
        self.stats['end_time'] = end_time.isoformat()
        training_time = (end_time - start_time).total_seconds()
        self.stats['training_time_seconds'] = training_time
        
        print(f"\n✅ Training complete!")
        print(f"   Total time: {training_time:.1f} seconds ({training_time/60:.1f} minutes)")
        print(f"   Epochs trained: {len(self.history.history['loss'])}")
        
        # Find best epoch
        best_epoch = np.argmax(self.history.history['val_accuracy']) + 1
        best_val_acc = max(self.history.history['val_accuracy'])
        
        self.stats['epochs_trained'] = len(self.history.history['loss'])
        self.stats['best_epoch'] = int(best_epoch)
        self.stats['train_accuracy'] = float(self.history.history['accuracy'][-1])
        self.stats['val_accuracy'] = float(best_val_acc)
        
        print(f"\n📊 Training Results:")
        print(f"   Best epoch: {best_epoch}")
        print(f"   Best validation accuracy: {best_val_acc:.4f} ({best_val_acc*100:.2f}%)")
        
        return self.history
    
    def evaluate_model(self, X_test, y_test):
        """
        Evaluate model on test set.
        """
        print("\n" + "="*60)
        print("STEP 4: EVALUATING MODEL")
        print("="*60)
        
        print(f"\n🔬 Evaluating on test set ({len(y_test):,} samples)...")
        
        # Get predictions
        if self.model_type == 'binary':
            y_pred_proba = self.model.predict(X_test, verbose=0).flatten()
            y_pred = (y_pred_proba > 0.5).astype(int)
        else:
            y_pred_proba = self.model.predict(X_test, verbose=0)
            y_pred = np.argmax(y_pred_proba, axis=1)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='binary' if self.model_type == 'binary' else 'weighted')
        recall = recall_score(y_test, y_pred, average='binary' if self.model_type == 'binary' else 'weighted')
        f1 = f1_score(y_test, y_pred, average='binary' if self.model_type == 'binary' else 'weighted')
        
        # Store metrics
        self.stats['test_accuracy'] = float(accuracy)
        self.stats['test_precision'] = float(precision)
        self.stats['test_recall'] = float(recall)
        self.stats['test_f1'] = float(f1)
        
        print(f"\n📊 Test Set Performance:")
        print(f"   Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"   Precision: {precision:.4f} ({precision*100:.2f}%)")
        print(f"   Recall:    {recall:.4f} ({recall*100:.2f}%)")
        print(f"   F1-Score:  {f1:.4f}")
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        print(f"\n📊 Confusion Matrix:")
        print(cm)
        
        # Classification report
        print(f"\n📊 Detailed Classification Report:")
        if self.model_type == 'binary':
            target_names = ['Normal', 'Attack']
        else:
            target_names = ['Normal', 'DoS', 'Probe', 'R2L', 'U2R']
        
        print(classification_report(y_test, y_pred, target_names=target_names[:len(np.unique(y_test))]))
        
        # Check if we met the >90% accuracy goal
        if accuracy >= 0.90:
            print(f"\n✅ SUCCESS! Achieved >90% accuracy target!")
        else:
            print(f"\n⚠️  Did not reach 90% target. Consider:")
            print(f"    - Increasing epochs")
            print(f"    - Adding more hidden layers")
            print(f"    - Adjusting learning rate")

        # -----------------------------
        # Save Predictions for OLS Statistical Testing (Added by Gowtham)
        # -----------------------------
        preds_path = self.model_dir / "ann_predictions.npy"
        np.save(preds_path, y_pred)

        print(f"💾 ANN predictions saved to: {preds_path}")
        
        return {
            'y_true': y_test,
            'y_pred': y_pred,
            'y_pred_proba': y_pred_proba,
            'confusion_matrix': cm,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1
        }
    
    def create_visualizations(self, eval_results):
        """
        Create all required visualizations.
        """
        print("\n" + "="*60)
        print("STEP 5: CREATING VISUALIZATIONS")
        print("="*60)
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
        
        # 1. Training and Validation Loss Curves
        print(f"\n📈 Creating loss curves...")
        plt.figure(figsize=(12, 5))
        
        plt.subplot(1, 2, 1)
        plt.plot(self.history.history['loss'], label='Training Loss', linewidth=2)
        plt.plot(self.history.history['val_loss'], label='Validation Loss', linewidth=2)
        plt.title('Model Loss Over Epochs', fontsize=14, fontweight='bold')
        plt.xlabel('Epoch', fontsize=12)
        plt.ylabel('Loss', fontsize=12)
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        
        # 2. Training and Validation Accuracy Curves
        plt.subplot(1, 2, 2)
        plt.plot(self.history.history['accuracy'], label='Training Accuracy', linewidth=2)
        plt.plot(self.history.history['val_accuracy'], label='Validation Accuracy', linewidth=2)
        plt.title('Model Accuracy Over Epochs', fontsize=14, fontweight='bold')
        plt.xlabel('Epoch', fontsize=12)
        plt.ylabel('Accuracy', fontsize=12)
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.viz_dir / 'ann_training_curves.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✅ Saved: ann_training_curves.png")
        
        # 3. Confusion Matrix
        print(f"\n📊 Creating confusion matrix...")
        plt.figure(figsize=(8, 6))
        
        cm = eval_results['confusion_matrix']
        
        if self.model_type == 'binary':
            labels = ['Normal', 'Attack']
        else:
            labels = ['Normal', 'DoS', 'Probe', 'R2L', 'U2R']
            labels = labels[:cm.shape[0]]
        
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=labels, yticklabels=labels,
                   cbar_kws={'label': 'Count'})
        plt.title('Confusion Matrix - ANN Model', fontsize=14, fontweight='bold')
        plt.xlabel('Predicted Label', fontsize=12)
        plt.ylabel('True Label', fontsize=12)
        
        plt.tight_layout()
        plt.savefig(self.viz_dir / 'ann_confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✅ Saved: ann_confusion_matrix.png")
        
        # 4. ROC Curve (for binary classification)
        if self.model_type == 'binary':
            print(f"\n📈 Creating ROC curve...")
            plt.figure(figsize=(8, 6))
            
            fpr, tpr, thresholds = roc_curve(eval_results['y_true'], eval_results['y_pred_proba'])
            roc_auc = auc(fpr, tpr)
            
            plt.plot(fpr, tpr, color='darkorange', lw=2, 
                    label=f'ROC curve (AUC = {roc_auc:.4f})')
            plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('False Positive Rate', fontsize=12)
            plt.ylabel('True Positive Rate', fontsize=12)
            plt.title('ROC Curve - ANN Model', fontsize=14, fontweight='bold')
            plt.legend(loc="lower right", fontsize=10)
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(self.viz_dir / 'ann_roc_curve.png', dpi=300, bbox_inches='tight')
            plt.close()
            print(f"   ✅ Saved: ann_roc_curve.png")
            
            self.stats['roc_auc'] = float(roc_auc)
            
            # 5. Precision-Recall Curve
            print(f"\n📈 Creating precision-recall curve...")
            plt.figure(figsize=(8, 6))
            
            precision_curve, recall_curve, _ = precision_recall_curve(
                eval_results['y_true'], eval_results['y_pred_proba']
            )
            
            plt.plot(recall_curve, precision_curve, color='green', lw=2)
            plt.xlabel('Recall', fontsize=12)
            plt.ylabel('Precision', fontsize=12)
            plt.title('Precision-Recall Curve - ANN Model', fontsize=14, fontweight='bold')
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(self.viz_dir / 'ann_precision_recall_curve.png', dpi=300, bbox_inches='tight')
            plt.close()
            print(f"   ✅ Saved: ann_precision_recall_curve.png")
        
        print(f"\n✅ All visualizations saved to: {self.viz_dir.absolute()}")
    
    def save_model(self):
        """
        Save the trained model and statistics.
        """
        print("\n" + "="*60)
        print("STEP 6: SAVING MODEL")
        print("="*60)
        
        # Save model in H5 format
        model_path = self.model_dir / 'currentAiSolution.h5'
        self.model.save(model_path)
        print(f"\n💾 Model saved to: {model_path}")
        
        # Save model size info
        model_size_mb = model_path.stat().st_size / (1024 * 1024)
        self.stats['model_size_mb'] = float(model_size_mb)
        print(f"   Model size: {model_size_mb:.2f} MB")
        
        # Save statistics
        stats_path = self.model_dir / 'ann_training_stats.json'
        with open(stats_path, 'w') as f:
            json.dump(self.stats, f, indent=2)
        print(f"\n💾 Statistics saved to: {stats_path}")
        
        print(f"\n✅ Model artifacts saved successfully!")

    def calibrate_temperature(self, X_calib, y_calib):
        """
        Learn temperature parameter for probability calibration
        using logit reconstruction (stable & architecture-safe).
        """
        print("\n" + "=" * 60)
        print("STEP 7: CALIBRATING CONFIDENCE (TEMPERATURE SCALING)")
        print("=" * 60)
    
        # Get predicted probabilities
        probs = self.model.predict(X_calib, verbose=0).flatten()
    
        # Numerical safety
        eps = 1e-7
        probs = np.clip(probs, eps, 1 - eps)
    
        # Convert probabilities → logits
        logits = np.log(probs / (1 - probs))
    
        T = tf.Variable(1.0, dtype=tf.float32)
    
        def nll():
            scaled_logits = logits / T
            scaled_probs = tf.sigmoid(scaled_logits)
            return tf.reduce_mean(
                tf.keras.losses.binary_crossentropy(y_calib, scaled_probs)
            )
    
        optimizer = tf.keras.optimizers.Adam(learning_rate=0.05)
    
        for _ in range(200):
            optimizer.minimize(nll, var_list=[T])
    
        temperature = float(T.numpy())
    
        # Save temperature
        temp_path = self.model_dir / "temperature.json"
        with open(temp_path, "w") as f:
            json.dump({"temperature": temperature}, f, indent=2)
    
        print(f"🌡️  Temperature learned: {temperature:.4f}")
        print(f"💾 Saved to: {temp_path}")
    
        return temperature

    def run(self):
        """
        Execute complete training pipeline.
        """
        print("="*60)
        print("ANN MODEL TRAINING - CYBER ATTACK DETECTION")
        print("Course: M. Grum: Advanced AI-based Application Systems")
        print("University of Potsdam")
        print("Author: V (ML Engineer)")
        print("="*60)
        
        # Load data
        X_train, y_train, X_test, y_test, feature_cols = self.load_data()
        
        # Build model
        if self.model_type == 'binary':
            output_dim = 1
        else:
            output_dim = len(np.unique(y_train))
        
        self.build_model(input_dim=X_train.shape[1], output_dim=output_dim)
        
        # Train model
        self.train_model(X_train, y_train, X_test, y_test)

        # -----------------------------
        # Temperature Calibration (NEW) Added by Gowtham
        # -----------------------------
        calib_size = int(0.2 * len(X_test))
        X_calib = X_test[:calib_size]
        y_calib = y_test[:calib_size]

        self.calibrate_temperature(X_calib, y_calib)
        
        # Evaluate model
        eval_results = self.evaluate_model(X_test, y_test)
        
        # Create visualizations
        self.create_visualizations(eval_results)
        
        # Save model
        self.save_model()
        
        # Final summary
        print("\n" + "="*60)
        print("✅ ANN TRAINING COMPLETE!")
        print("="*60)
        print(f"\n📊 Final Performance:")
        print(f"   Test Accuracy: {self.stats['test_accuracy']:.4f} ({self.stats['test_accuracy']*100:.2f}%)")
        print(f"   Test Precision: {self.stats['test_precision']:.4f}")
        print(f"   Test Recall: {self.stats['test_recall']:.4f}")
        print(f"   Test F1-Score: {self.stats['test_f1']:.4f}")
        
        if self.model_type == 'binary' and 'roc_auc' in self.stats:
            print(f"   ROC-AUC: {self.stats['roc_auc']:.4f}")
        
        print(f"\n⏱️  Training Time: {self.stats['training_time_seconds']:.1f} seconds")
        print(f"\n📁 Output Files:")
        print(f"   Model: {self.model_dir / 'currentAiSolution.h5'}")
        print(f"   Stats: {self.model_dir / 'ann_training_stats.json'}")
        print(f"   Visualizations: {self.viz_dir.absolute()}")
        
        print(f"\n🎯 NEXT STEP: Train OLS baseline")
        print("   Command: python code/training/train_ols.py")
        print("="*60)
        
        return self.stats


def main():
    """Main entry point."""
    # Train binary classifier (normal vs attack)
    print("Training Binary Classifier (Normal vs Attack)...\n")
    
    trainer = CyberAttackANN(model_type='binary')
    stats = trainer.run()
    
    # Success message
    if stats['test_accuracy'] >= 0.90:
        print("\n🎉 SUCCESS! ANN model achieved >90% accuracy!")
        print(f"   Actual accuracy: {stats['test_accuracy']*100:.2f}%")
    
    return stats


if __name__ == "__main__":
    main()
