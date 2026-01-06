"""
Data Preprocessing Script for NSL-KDD Dataset
Course: M. Grum: Advanced AI-based Application Systems
University of Potsdam

This script:
1. Loads raw NSL-KDD data
2. Cleans and preprocesses
3. Creates train/test/activation splits
4. Saves processed CSV files
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import pickle


# NSL-KDD Feature Names (41 features + 1 label)
FEATURE_NAMES = [
    'duration', 'protocol_type', 'service', 'flag',
    'src_bytes', 'dst_bytes', 'land', 'wrong_fragment',
    'urgent', 'hot', 'num_failed_logins', 'logged_in',
    'num_compromised', 'root_shell', 'su_attempted', 'num_root',
    'num_file_creations', 'num_shells', 'num_access_files',
    'num_outbound_cmds', 'is_host_login', 'is_guest_login',
    'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
    'rerror_rate', 'srv_rerror_rate', 'same_srv_rate',
    'diff_srv_rate', 'srv_diff_host_rate',
    'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate',
    'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
    'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
    'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
    'dst_host_srv_rerror_rate', 'label', 'difficulty'
]


def load_nslkdd_data():
    """
    Load NSL-KDD dataset from raw files.
    """
    print("📂 Loading NSL-KDD dataset...")
    
    data_dir = Path("../../data/raw")
    train_file = data_dir / "KDDTrain+.txt"
    test_file = data_dir / "KDDTest+.txt"
    
    # Load training data
    try:
        df_train = pd.read_csv(train_file, header=None, names=FEATURE_NAMES)
        print(f"✅ Training data loaded: {len(df_train)} records")
    except FileNotFoundError:
        print(f"❌ Training file not found: {train_file}")
        print("   Run scraping script first: python code/scraping/scrape_nslkdd.py")
        return None, None
    
    # Load testing data
    try:
        df_test = pd.read_csv(test_file, header=None, names=FEATURE_NAMES)
        print(f"✅ Testing data loaded: {len(df_test)} records")
    except FileNotFoundError:
        print(f"❌ Testing file not found: {test_file}")
        return None, None
    
    return df_train, df_test


def clean_data(df):
    """
    Clean the dataset: handle missing values, duplicates, etc.
    """
    print(f"\n🧹 Cleaning data...")
    print(f"   Initial records: {len(df)}")
    
    # Remove difficulty column (not needed for training)
    if 'difficulty' in df.columns:
        df = df.drop('difficulty', axis=1)
    
    # Check for missing values
    missing = df.isnull().sum().sum()
    print(f"   Missing values: {missing}")
    
    if missing > 0:
        print("   Dropping rows with missing values...")
        df = df.dropna()
    
    # Remove duplicates
    duplicates = df.duplicated().sum()
    print(f"   Duplicate rows: {duplicates}")
    
    if duplicates > 0:
        print("   Removing duplicates...")
        df = df.drop_duplicates()
    
    print(f"   Final records: {len(df)}")
    return df


def encode_labels(df):
    """
    Encode attack labels:
    - Binary: normal (0) vs attack (1)
    - Multi-class: normal, dos, probe, r2l, u2r
    """
    print(f"\n🏷️  Encoding labels...")
    
    # Create binary label
    df['label_binary'] = df['label'].apply(lambda x: 0 if 'normal' in x else 1)
    
    # Create multi-class label
    def categorize_attack(label):
        label_lower = label.lower()
        if 'normal' in label_lower:
            return 'normal'
        elif any(attack in label_lower for attack in ['back', 'land', 'neptune', 'pod', 'smurf', 'teardrop']):
            return 'dos'
        elif any(attack in label_lower for attack in ['ipsweep', 'nmap', 'portsweep', 'satan']):
            return 'probe'
        elif any(attack in label_lower for attack in ['ftp_write', 'guess_passwd', 'imap', 'multihop', 'phf', 'spy', 'warezclient', 'warezmaster']):
            return 'r2l'
        elif any(attack in label_lower for attack in ['buffer_overflow', 'loadmodule', 'perl', 'rootkit']):
            return 'u2r'
        else:
            return 'unknown'
    
    df['label_multiclass'] = df['label'].apply(categorize_attack)
    
    # Print label distribution
    print(f"\n   Binary Label Distribution:")
    print(df['label_binary'].value_counts())
    print(f"\n   Multi-class Label Distribution:")
    print(df['label_multiclass'].value_counts())
    
    return df


def preprocess_features(df):
    """
    Preprocess features: encode categorical, normalize numerical.
    """
    print(f"\n🔧 Preprocessing features...")
    
    # Separate features and labels
    feature_cols = [col for col in df.columns if not col.startswith('label')]
    
    # Identify categorical columns
    categorical_cols = ['protocol_type', 'service', 'flag']
    
    # Encode categorical variables
    print(f"   Encoding categorical variables...")
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
    
    # Normalize numerical features
    print(f"   Normalizing numerical features...")
    numerical_cols = [col for col in feature_cols if col not in categorical_cols]
    
    scaler = MinMaxScaler()
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
    
    # Save scaler for future use
    output_dir = Path("../../data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / "scaler.pkl", 'wb') as f:
        pickle.dump(scaler, f)
    
    print(f"   ✅ Scaler saved to: {output_dir / 'scaler.pkl'}")
    
    return df


def create_data_splits(df_train, df_test):
    """
    Create required data splits:
    - joint_data_collection.csv (all data combined)
    - training_data.csv (80% of joint)
    - test_data.csv (20% of joint)
    - activation_data.csv (1 sample from test)
    """
    print(f"\n✂️  Creating data splits...")
    
    # Combine train and test
    df_joint = pd.concat([df_train, df_test], ignore_index=True)
    print(f"   Joint dataset: {len(df_joint)} records")
    
    # Split into 80/20
    df_train_split, df_test_split = train_test_split(
        df_joint,
        test_size=0.2,
        random_state=42,
        stratify=df_joint['label_binary']  # Maintain class distribution
    )
    
    print(f"   Training split: {len(df_train_split)} records (80%)")
    print(f"   Testing split: {len(df_test_split)} records (20%)")
    
    # Create activation data (1 normal + 1 attack example)
    normal_sample = df_test_split[df_test_split['label_binary'] == 0].sample(n=1, random_state=42)
    attack_sample = df_test_split[df_test_split['label_binary'] == 1].sample(n=1, random_state=42)
    df_activation = pd.concat([normal_sample, attack_sample], ignore_index=True)
    
    print(f"   Activation data: {len(df_activation)} records (1 normal + 1 attack)")
    
    return df_joint, df_train_split, df_test_split, df_activation


def save_processed_data(df_joint, df_train, df_test, df_activation):
    """
    Save processed data to CSV files.
    """
    print(f"\n💾 Saving processed data...")
    
    output_dir = Path("../../data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save files
    files = {
        'joint_data_collection.csv': df_joint,
        'training_data.csv': df_train,
        'test_data.csv': df_test,
        'activation_data.csv': df_activation
    }
    
    for filename, dataframe in files.items():
        filepath = output_dir / filename
        dataframe.to_csv(filepath, index=False)
        size_mb = filepath.stat().st_size / (1024 * 1024)
        print(f"   ✅ {filename}: {len(dataframe)} records, {size_mb:.2f} MB")
    
    print(f"\n✅ All files saved to: {output_dir.absolute()}")


def main():
    """
    Main preprocessing pipeline.
    """
    print("="*60)
    print("NSL-KDD DATA PREPROCESSING")
    print("Course: M. Grum: Advanced AI-based Application Systems")
    print("University of Potsdam")
    print("="*60)
    
    # Step 1: Load data
    df_train_raw, df_test_raw = load_nslkdd_data()
    if df_train_raw is None:
        return
    
    # Step 2: Clean data
    df_train_clean = clean_data(df_train_raw)
    df_test_clean = clean_data(df_test_raw)
    
    # Step 3: Encode labels
    df_train_labeled = encode_labels(df_train_clean)
    df_test_labeled = encode_labels(df_test_clean)
    
    # Step 4: Preprocess features
    df_train_processed = preprocess_features(df_train_labeled)
    df_test_processed = preprocess_features(df_test_labeled)
    
    # Step 5: Create splits
    df_joint, df_train_split, df_test_split, df_activation = create_data_splits(
        df_train_processed,
        df_test_processed
    )
    
    # Step 6: Save processed data
    save_processed_data(df_joint, df_train_split, df_test_split, df_activation)
    
    print("\n" + "="*60)
    print("PREPROCESSING COMPLETE!")
    print("NEXT STEP: Train ANN model")
    print("Command: python code/training/train_ann.py")
    print("="*60)


if __name__ == "__main__":
    main()