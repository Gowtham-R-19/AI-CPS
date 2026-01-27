import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path("data/processed")

LABEL_COLS = {
    "binary": "label_binary",
    "multiclass": "label_multiclass_encoded"
}

def validate():
    train = pd.read_csv(DATA_DIR / "training_data.csv")
    test = pd.read_csv(DATA_DIR / "test_data.csv")

    print("\n📊 Dataset Validation Report")
    print("=" * 60)

    # 1. Column consistency
    if train.columns.equals(test.columns):
        print("✅ Column order and names match between train and test")
    else:
        print("❌ Column mismatch between train and test")

    # 2. Separate numeric vs non-numeric
    numeric_cols = train.select_dtypes(include=[np.number]).columns
    non_numeric_cols = train.select_dtypes(exclude=[np.number]).columns

    print(f"\n📈 Feature Types:")
    print(f"   Numeric columns: {len(numeric_cols)}")
    print(f"   Non-numeric columns: {len(non_numeric_cols)}")

    if len(non_numeric_cols) > 0:
        print("   ⚠️ Non-numeric columns detected:")
        for col in non_numeric_cols:
            print(f"     - {col}")

    # 3. Missing / Infinite values (numeric only)
    nan_count = train[numeric_cols].isna().sum().sum()
    inf_count = np.isinf(train[numeric_cols].to_numpy()).sum()

    print(f"\n🧪 Data Integrity:")
    print(f"   NaN values (numeric): {nan_count}")
    print(f"   Inf values (numeric): {inf_count}")

    # 4. Label validation
    print(f"\n🏷️ Label Check:")
    for name, col in LABEL_COLS.items():
        if col in train.columns:
            unique_vals = np.sort(train[col].unique())
            print(f"   {name.capitalize()} labels in '{col}': {unique_vals}")

    # 5. Feature scale snapshot
    print("\n📊 Feature Scale Sample (first 5 numeric features):")
    print(train[numeric_cols].describe().T[["min", "max"]].head())

    # 6. Final verdict
    if nan_count == 0 and inf_count == 0:
        print("\n✅ Dataset is numerically clean and model-ready")
    else:
        print("\n⚠️ Dataset has integrity issues — clean before training")

    print("\nValidation complete.")

if __name__ == "__main__":
    validate()