"""
Dataset Overlap Check Script
Course: M. Grum: Advanced AI-based Application Systems
University of Potsdam

Purpose:
This script verifies that there is no data leakage between the training
and testing datasets by checking for identical rows in both files.

Why this matters:
If the same records appear in both training and test sets, model performance
metrics (accuracy, precision, recall, ROC-AUC) can be artificially inflated.
This check ensures the evaluation results are scientifically valid.

Author: V (ML Engineer)
"""

import pandas as pd


def main():
    """
    Main function to check for overlapping rows between training and test datasets.
    """

    # -----------------------------
    # Step 1: Load Datasets
    # -----------------------------
    # Read the preprocessed training and testing CSV files
    train_path = "data/processed/training_data.csv"
    test_path = "data/processed/test_data.csv"

    print("📂 Loading datasets...")
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)

    print(f"✅ Training samples: {len(train)}")
    print(f"✅ Test samples:     {len(test)}")

    # -----------------------------
    # Step 2: Check for Overlap
    # -----------------------------
    # Perform an inner join on all columns
    # This will return only rows that are exactly identical in both datasets
    overlap_df = pd.merge(train, test, how="inner")

    overlap_count = overlap_df.shape[0]

    # -----------------------------
    # Step 3: Report Results
    # -----------------------------
    print("\n🔍 Overlap Analysis")
    print("-" * 40)
    print(f"Overlap rows found: {overlap_count}")

    # -----------------------------
    # Step 4: Interpretation
    # -----------------------------
    if overlap_count == 0:
        print("✅ No data leakage detected")
        print("   Training and test sets are cleanly separated.")
    else:
        print("⚠️ WARNING: Potential data leakage detected!")
        print("   Identical rows appear in both training and test sets.")
        print("   This can artificially inflate performance metrics.")
        print("   Recommendation: Re-split the dataset before retraining the model.")


if __name__ == "__main__":
    main()