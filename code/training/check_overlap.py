"""
================================================================================
Title: Dataset Overlap Verification Script — Data Leakage Prevention

Course: M. Grum – Advanced AI-based Application Systems
Track: Data Science and Business Analytics
Instructor: Prof. Dr. Marcus Grum
Chair: Junior Chair for Business Information Science, especially AI-based Application Systems
Institution: University of Potsdam, Germany
Authors: Vaishnavi Vijaya

Description:
This script validates the integrity of training and testing datasets by
programmatically detecting identical records across splits, ensuring that
no data leakage occurs and that model evaluation metrics remain scientifically
sound and reproducible.

Key Design Principles:
- Automated data leakage detection and reporting
- Scientific validity and experimental integrity enforcement
- Scalable comparison logic for large-scale datasets
- Seamless integration with preprocessing and training pipelines

================================================================================
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
