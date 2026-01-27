"""
Clean Dataset Re-Split Script
Course: M. Grum: Advanced AI-based Application Systems
University of Potsdam

Purpose:
This script removes duplicate records from the combined dataset and
recreates clean training and test splits to eliminate data leakage.

Why this matters:
Overlapping samples between training and test sets artificially inflate
model performance metrics and invalidate evaluation results. This script
ensures scientific integrity and reproducibility.

Author: V (ML Engineer)
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path


def main():
    # -----------------------------
    # Configuration
    # -----------------------------
    data_dir = Path("data/processed")
    train_file = data_dir / "training_data.csv"
    test_file = data_dir / "test_data.csv"

    output_train = data_dir / "training_data.csv"
    output_test = data_dir / "test_data.csv"

    test_size = 0.2
    random_state = 42

    print("📂 Loading existing datasets...")
    train_df = pd.read_csv(train_file)
    test_df = pd.read_csv(test_file)

    print(f"✅ Original training samples: {len(train_df)}")
    print(f"✅ Original test samples:     {len(test_df)}")

    # -----------------------------
    # Step 1: Combine Datasets
    # -----------------------------
    combined_df = pd.concat([train_df, test_df], ignore_index=True)
    print(f"\n🔗 Combined samples: {len(combined_df)}")

    # -----------------------------
    # Step 2: Remove Duplicates
    # -----------------------------
    before_dedup = len(combined_df)
    combined_df = combined_df.drop_duplicates()
    after_dedup = len(combined_df)

    print(f"\n🧹 Deduplication Results:")
    print(f"   Rows before: {before_dedup}")
    print(f"   Rows after:  {after_dedup}")
    print(f"   Removed:     {before_dedup - after_dedup}")

    # -----------------------------
    # Step 3: Stratified Re-Split
    # -----------------------------
    # Preserve class distribution using binary label
    label_col = "label_binary"

    train_clean, test_clean = train_test_split(
        combined_df,
        test_size=test_size,
        random_state=random_state,
        stratify=combined_df[label_col]
    )

    print(f"\n📊 Clean split:")
    print(f"   Training samples: {len(train_clean)}")
    print(f"   Test samples:     {len(test_clean)}")

    # -----------------------------
    # Step 4: Save Clean Files
    # -----------------------------
    train_clean.to_csv(output_train, index=False)
    test_clean.to_csv(output_test, index=False)

    print(f"\n💾 Clean datasets saved:")
    print(f"   {output_train}")
    print(f"   {output_test}")

    print("\n✅ Dataset successfully cleaned and re-split")
    print("   You can now safely retrain your models.")


if __name__ == "__main__":
    main()
    