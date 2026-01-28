"""
OLS Baseline Model Training Script - FULL IMPLEMENTATION
Course: M. Grum: Advanced AI-based Application Systems
University of Potsdam

This script trains a logistic regression baseline for comparison with ANN.
Expected accuracy: 75-82% (showing ANN improvement of 12-16%)

Author: V (Team Lead - ML Engineer)
Week: 4 (Subgoal 5: OLS Model Creation)
"""
# ==========================================================
# ⚖️ BASELINE GOVERNANCE NOTICE
# This OLS model serves as a scientific baseline for ANN
# performance comparison. It must:
# 1. Use the same feature scaling as ANN (scaler.pkl)
# 2. Be evaluated on a leakage-free dataset
#    (python code/training/check_overlap.py → Overlap = 0)
# 3. Be reported with statistical significance where possible
# ==========================================================

from unittest import result
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json
import pickle

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_curve, auc
)
import scipy.stats as stats
from statsmodels.stats.contingency_tables import mcnemar


class CyberAttackOLS:
    """
    Logistic Regression Baseline for Cyber Attack Detection.
    """
    
    def __init__(self, model_type='binary'):
        """
        Initialize the OLS trainer.
        
        Args:
            model_type: 'binary' or 'multiclass'
        """
        self.model_type = model_type
        self.model = None
        
        # Paths
        self.data_dir = Path(__file__).parent.parent.parent / "data" / "processed"
        #self.model_dir = Path(__file__).parent.parent.parent / "models"
        #self.viz_dir = Path(__file__).parent.parent.parent / "visualizations"

        # -----------------------------
        # Link OLS to Latest ANN Run (Source of Truth) Added by Gowtham
        # -----------------------------
        base_dir = Path(__file__).parent.parent.parent

        run_id_file = base_dir / "models" / "LATEST_RUN.txt"
        if not run_id_file.exists():
            raise RuntimeError("❌ LATEST_RUN.txt not found. Train ANN first.")

        run_id = run_id_file.read_text().strip()
        
        self.ann_dir = base_dir / "models" / run_id / "ann" # Path to ANN model directory
        self.model_dir = base_dir / "models" / run_id / "ols"
        self.viz_dir = base_dir / "visualizations" / run_id / "ols"

        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.viz_dir.mkdir(parents=True, exist_ok=True)

        print(f"📁 OLS linked to ANN run: {run_id}")
        
        # Create directories
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.viz_dir.mkdir(parents=True, exist_ok=True)
        
        # Training statistics
        self.stats = {
            'model_type': model_type,
            'start_time': None,
            'end_time': None,
            'training_time_seconds': 0,
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
        # Feature Scaling (Fair Comparison with ANN) Updated Version 
        # -----------------------------
        scaler_path = self.model_dir.parent / "ann" / "scaler.pkl" # Path to ANN scaler

        if scaler_path.exists():
            print(f"🔧 Loading scaler from ANN run: {scaler_path}")
            import joblib
            scaler = joblib.load(scaler_path)

            X_train = scaler.transform(df_train[feature_cols].values)
            X_test = scaler.transform(df_test[feature_cols].values)
        else:
            print("⚠️  No scaler found. Using raw features (comparison may be biased).")
            X_train = df_train[feature_cols].values
            X_test = df_test[feature_cols].values

        y_train = df_train[label_col].values
        y_test = df_test[label_col].values
        
        print(f"\n📊 Data shapes:")
        print(f"   X_train: {X_train.shape}")
        print(f"   y_train: {y_train.shape}")
        print(f"   X_test: {X_test.shape}")
        print(f"   y_test: {y_test.shape}")
        
        return X_train, y_train, X_test, y_test, feature_cols
    
    def build_and_train_model(self, X_train, y_train):
        """
        Build and train logistic regression model.
        """
        print("\n" + "="*60)
        print("STEP 2: BUILDING AND TRAINING OLS MODEL")
        print("="*60)
        
        print(f"\n📊 Model Configuration:")
        print(f"   Algorithm: Logistic Regression")
        print(f"   Solver: lbfgs")
        print(f"   Max iterations: 1000")
        
        if self.model_type == 'binary':
            print(f"   Classification: Binary (Normal vs Attack)")
        else:
            print(f"   Classification: Multi-class (5 categories)")
            print(f"   Strategy: One-vs-Rest (OvR)")
        
        # Create model
        self.model = LogisticRegression(
            solver='lbfgs',
            max_iter=1000,
            multi_class='ovr' if self.model_type == 'multiclass' else 'auto',
            random_state=42,
            n_jobs=-1,  # Use all CPU cores
            verbose=0
        )
        
        print(f"\n🏋️  Training model...")
        print(f"   This will take <1 minute (much faster than ANN)...\n")
        
        # Record start time
        self.stats['start_time'] = datetime.now().isoformat()
        start_time = datetime.now()
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Record end time
        end_time = datetime.now()
        self.stats['end_time'] = end_time.isoformat()
        training_time = (end_time - start_time).total_seconds()
        self.stats['training_time_seconds'] = training_time
        
        print(f"✅ Training complete!")
        print(f"   Total time: {training_time:.2f} seconds")
        print(f"   Converged in {self.model.n_iter_[0]} iterations")
        
        # Training accuracy
        train_accuracy = self.model.score(X_train, y_train)
        print(f"\n📊 Training accuracy: {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
        
        return self.model
    
    def evaluate_model(self, X_test, y_test):
        """
        Evaluate model on test set.
        """
        print("\n" + "="*60)
        print("STEP 3: EVALUATING MODEL")
        print("="*60)
        
        print(f"\n🔬 Evaluating on test set ({len(y_test):,} samples)...")
        
        # Get predictions
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)
        
        # For binary classification, get probability of positive class
        if self.model_type == 'binary':
            y_pred_proba_positive = y_pred_proba[:, 1]
        else:
            y_pred_proba_positive = np.max(y_pred_proba, axis=1)
        
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
        
        return {
            'y_true': y_test,
            'y_pred': y_pred,
            'y_pred_proba': y_pred_proba_positive,
            'confusion_matrix': cm,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1
        }
    
    def create_diagnostic_plots(self, X_test, eval_results):
        """
        Create OLS diagnostic plots.
        """
        print("\n" + "="*60)
        print("STEP 4: CREATING DIAGNOSTIC PLOTS")
        print("="*60)
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
        
        # 1. Confusion Matrix
        print(f"\n📊 Creating confusion matrix...")
        plt.figure(figsize=(8, 6))
        
        cm = eval_results['confusion_matrix']
        
        if self.model_type == 'binary':
            labels = ['Normal', 'Attack']
        else:
            labels = ['Normal', 'DoS', 'Probe', 'R2L', 'U2R']
            labels = labels[:cm.shape[0]]
        
        sns.heatmap(cm, annot=True, fmt='d', cmap='Greens',
                   xticklabels=labels, yticklabels=labels,
                   cbar_kws={'label': 'Count'})
        plt.title('Confusion Matrix - OLS Baseline', fontsize=14, fontweight='bold')
        plt.xlabel('Predicted Label', fontsize=12)
        plt.ylabel('True Label', fontsize=12)
        
        plt.tight_layout()
        plt.savefig(self.viz_dir / 'ols_confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✅ Saved: ols_confusion_matrix.png")
        
        # 2. ROC Curve (for binary classification)
        if self.model_type == 'binary':
            print(f"\n📈 Creating ROC curve...")
            plt.figure(figsize=(8, 6))
            
            fpr, tpr, thresholds = roc_curve(eval_results['y_true'], eval_results['y_pred_proba'])
            roc_auc = auc(fpr, tpr)
            
            plt.plot(fpr, tpr, color='green', lw=2,
                    label=f'ROC curve (AUC = {roc_auc:.4f})')
            plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('False Positive Rate', fontsize=12)
            plt.ylabel('True Positive Rate', fontsize=12)
            plt.title('ROC Curve - OLS Baseline', fontsize=14, fontweight='bold')
            plt.legend(loc="lower right", fontsize=10)
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(self.viz_dir / 'ols_roc_curve.png', dpi=300, bbox_inches='tight')
            plt.close()
            print(f"   ✅ Saved: ols_roc_curve.png")
            
            self.stats['roc_auc'] = float(roc_auc)
        
        # 3. Residual Plot
        print(f"\n📈 Creating residual plot...")
        plt.figure(figsize=(10, 6))
        
        # Get predicted probabilities
        y_pred_proba_all = self.model.predict_proba(X_test)
        
        # Calculate residuals (difference between actual and predicted)
        if self.model_type == 'binary':
            residuals = eval_results['y_true'] - y_pred_proba_all[:, 1]
        else:
            residuals = eval_results['y_true'] - np.argmax(y_pred_proba_all, axis=1)
        
        plt.scatter(range(len(residuals)), residuals, alpha=0.3, s=10)
        plt.axhline(y=0, color='r', linestyle='--', linewidth=2, label='Zero Residual')
        plt.xlabel('Sample Index', fontsize=12)
        plt.ylabel('Residual', fontsize=12)
        plt.title('Residual Plot - OLS Baseline', fontsize=14, fontweight='bold')
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.viz_dir / 'ols_residual_plot.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✅ Saved: ols_residual_plot.png")
        
        # 4. Predicted vs Actual Scatter Plot
        print(f"\n📈 Creating predicted vs actual plot...")
        plt.figure(figsize=(8, 8))
        
        plt.scatter(eval_results['y_true'], eval_results['y_pred'], alpha=0.3, s=20)
        
        # Add perfect prediction line
        min_val = min(eval_results['y_true'].min(), eval_results['y_pred'].min())
        max_val = max(eval_results['y_true'].max(), eval_results['y_pred'].max())
        plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')
        
        plt.xlabel('True Label', fontsize=12)
        plt.ylabel('Predicted Label', fontsize=12)
        plt.title('Predicted vs Actual - OLS Baseline', fontsize=14, fontweight='bold')
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.viz_dir / 'ols_predicted_vs_actual.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✅ Saved: ols_predicted_vs_actual.png")
        
        print(f"\n✅ All diagnostic plots saved to: {self.viz_dir.absolute()}")
    
    def compare_with_ann(self):
        """
        Compare OLS performance with ANN.
        """
        print("\n" + "="*60)
        print("STEP 5: COMPARING WITH ANN")
        print("="*60)
        
        # Load ANN stats if available
        
        ann_stats_file = self.model_dir.parent / "ann" / "ann_training_stats.json" # Path to ANN stats
        
        if not ann_stats_file.exists():
            print("\n⚠️  ANN statistics not found. Train ANN first:")
            print("   python code/training/train_ann.py")
            return None
        
        with open(ann_stats_file, 'r') as f:
            ann_stats = json.load(f)
        
        print(f"\n📊 Performance Comparison:")
        print(f"\n   Metric          | OLS Baseline | ANN Model  | Improvement")
        print(f"   " + "-"*60)
        print(f"   Accuracy        | {self.stats['test_accuracy']*100:>6.2f}%      | {ann_stats['test_accuracy']*100:>6.2f}%   | {(ann_stats['test_accuracy'] - self.stats['test_accuracy'])*100:>+6.2f}%")
        print(f"   Precision       | {self.stats['test_precision']*100:>6.2f}%      | {ann_stats['test_precision']*100:>6.2f}%   | {(ann_stats['test_precision'] - self.stats['test_precision'])*100:>+6.2f}%")
        print(f"   Recall          | {self.stats['test_recall']*100:>6.2f}%      | {ann_stats['test_recall']*100:>6.2f}%   | {(ann_stats['test_recall'] - self.stats['test_recall'])*100:>+6.2f}%")
        print(f"   F1-Score        | {self.stats['test_f1']:.4f}     | {ann_stats['test_f1']:.4f}    | {ann_stats['test_f1'] - self.stats['test_f1']:>+.4f}")
        
        if self.model_type == 'binary' and 'roc_auc' in self.stats and 'roc_auc' in ann_stats:
            print(f"   ROC-AUC         | {self.stats['roc_auc']:.4f}     | {ann_stats['roc_auc']:.4f}    | {ann_stats['roc_auc'] - self.stats['roc_auc']:>+.4f}")
        
        print(f"\n   Training Time   | {self.stats['training_time_seconds']:.1f}s        | {ann_stats['training_time_seconds']:.1f}s      | {ann_stats['training_time_seconds'] - self.stats['training_time_seconds']:>+.1f}s")
        
        # Create comparison bar chart
        print(f"\n📊 Creating comparison chart...")
        plt.figure(figsize=(10, 6))
        
        metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
        ols_values = [
            self.stats['test_accuracy'],
            self.stats['test_precision'],
            self.stats['test_recall'],
            self.stats['test_f1']
        ]
        ann_values = [
            ann_stats['test_accuracy'],
            ann_stats['test_precision'],
            ann_stats['test_recall'],
            ann_stats['test_f1']
        ]
        
        x = np.arange(len(metrics))
        width = 0.35
        
        plt.bar(x - width/2, ols_values, width, label='OLS Baseline', color='green', alpha=0.8)
        plt.bar(x + width/2, ann_values, width, label='ANN Model', color='orange', alpha=0.8)
        
        plt.xlabel('Metric', fontsize=12)
        plt.ylabel('Score', fontsize=12)
        plt.title('OLS vs ANN Performance Comparison', fontsize=14, fontweight='bold')
        plt.xticks(x, metrics)
        plt.ylim([0, 1.1])
        plt.legend(fontsize=10)
        plt.grid(True, axis='y', alpha=0.3)
        
        # Add value labels on bars
        for i, (ols_val, ann_val) in enumerate(zip(ols_values, ann_values)):
            plt.text(i - width/2, ols_val + 0.02, f'{ols_val:.3f}', 
                    ha='center', va='bottom', fontsize=9)
            plt.text(i + width/2, ann_val + 0.02, f'{ann_val:.3f}', 
                    ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(self.viz_dir / 'ols_vs_ann_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✅ Saved: ols_vs_ann_comparison.png")
        
        # Store comparison
        improvement = (ann_stats['test_accuracy'] - self.stats['test_accuracy']) * 100
        self.stats['ann_improvement_percentage'] = float(improvement)
        
        if improvement >= 12:
            print(f"\n✅ SUCCESS! ANN shows {improvement:.1f}% improvement over OLS!")
            print(f"   Target: >12% improvement")
        else:
            print(f"\n⚠️  ANN improvement ({improvement:.1f}%) is below 12% target")

        # -----------------------------
        # Statistical Significance Test (McNemar’s Test) Code Added by Gowtham
        # -----------------------------
        print("\n📐 Statistical Significance Test (McNemar’s Test)")
        print("   (Evaluates if ANN improvement is statistically significant)")

        try:
            # Reload test data
            _, _, X_test, y_test, _ = self.load_data()

            ann_preds_path = self.ann_dir / "ann_predictions.npy" # Path to ANN predictions

            if ann_preds_path.exists():
                ann_preds = np.load(ann_preds_path)
                ols_preds = self.model.predict(X_test)

                # Contingency values
                both_correct = np.sum((ann_preds == y_test) & (ols_preds == y_test))
                ann_correct_ols_wrong = np.sum((ann_preds == y_test) & (ols_preds != y_test))
                ann_wrong_ols_correct = np.sum((ann_preds != y_test) & (ols_preds == y_test))
                both_wrong = np.sum((ann_preds != y_test) & (ols_preds != y_test))

                table = [[both_correct, ann_correct_ols_wrong],
                         [ann_wrong_ols_correct, both_wrong]]

                result = mcnemar(table, exact=False, correction=True)

                print(f"   chi² statistic: {result.statistic:.4f}")
                print(f"   p-value: {result.pvalue:.6f}")

                if result.pvalue < 0.05:
                    print("   ✅ ANN improvement is statistically significant (p < 0.05)")
                else:
                    print("   ⚠️  ANN improvement is NOT statistically significant")
            else:
                print("⚠️  ANN predictions not found. Skipping significance test.")
        except Exception as e:
            print(f"⚠️  Could not perform statistical test: {e}")
        
        return ann_stats
    
    def save_model(self):
        """
        Save the trained model and statistics.
        """
        print("\n" + "="*60)
        print("STEP 6: SAVING MODEL")
        print("="*60)
        
        # Save model in pickle format
        model_path = self.model_dir / 'currentOlsSolution.pkl'
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"\n💾 Model saved to: {model_path}")
        
        # Save model size info
        model_size_mb = model_path.stat().st_size / (1024 * 1024)
        self.stats['model_size_mb'] = float(model_size_mb)
        print(f"   Model size: {model_size_mb:.2f} MB")
        
        # Save statistics
        stats_path = self.model_dir / 'ols_training_stats.json'
        with open(stats_path, 'w') as f:
            json.dump(self.stats, f, indent=2)
        print(f"\n💾 Statistics saved to: {stats_path}")
        
        print(f"\n✅ Model artifacts saved successfully!")
    
    def run(self):
        """
        Execute complete training pipeline.
        """
        print("="*60)
        print("OLS BASELINE MODEL TRAINING - CYBER ATTACK DETECTION")
        print("Course: M. Grum: Advanced AI-based Application Systems")
        print("University of Potsdam")
        print("Author: V (ML Engineer)")
        print("="*60)
        
        # Load data
        X_train, y_train, X_test, y_test, feature_cols = self.load_data()
        
        # Build and train model
        self.build_and_train_model(X_train, y_train)
        
        # Evaluate model
        eval_results = self.evaluate_model(X_test, y_test)
        
        # Create diagnostic plots
        self.create_diagnostic_plots(X_test, eval_results)
        
        # Compare with ANN
        self.compare_with_ann()
        
        # Save model
        self.save_model()
        
        # Final summary
        print("\n" + "="*60)
        print("✅ OLS TRAINING COMPLETE!")
        print("="*60)
        print(f"\n📊 Final Performance:")
        print(f"   Test Accuracy: {self.stats['test_accuracy']:.4f} ({self.stats['test_accuracy']*100:.2f}%)")
        print(f"   Test Precision: {self.stats['test_precision']:.4f}")
        print(f"   Test Recall: {self.stats['test_recall']:.4f}")
        print(f"   Test F1-Score: {self.stats['test_f1']:.4f}")
        
        if self.model_type == 'binary' and 'roc_auc' in self.stats:
            print(f"   ROC-AUC: {self.stats['roc_auc']:.4f}")
        
        print(f"\n⏱️  Training Time: {self.stats['training_time_seconds']:.2f} seconds")
        
        if 'ann_improvement_percentage' in self.stats:
            print(f"\n📈 ANN Improvement: +{self.stats['ann_improvement_percentage']:.1f}% over OLS")
        
        print(f"\n📁 Output Files:")
        print(f"   Model: {self.model_dir / 'currentOlsSolution.pkl'}")
        print(f"   Stats: {self.model_dir / 'ols_training_stats.json'}")
        print(f"   Visualizations: {self.viz_dir.absolute()}")
        
        print(f"\n🎯 NEXT STEP: Create Docker model images (Week 5)")
        print("="*60)
        
        return self.stats


def main():
    """Main entry point."""
    # Train binary classifier (normal vs attack)
    print("Training OLS Baseline (Normal vs Attack)...\n")
    
    trainer = CyberAttackOLS(model_type='binary')
    stats = trainer.run()
    
    return stats


if __name__ == "__main__":
    main()
    