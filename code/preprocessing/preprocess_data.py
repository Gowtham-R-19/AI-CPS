"""
Data Preprocessing Script for NSL-KDD Dataset - FULL IMPLEMENTATION
Course: M. Grum: Advanced AI-based Application Systems
University of Potsdam

This script:
1. Loads raw NSL-KDD data from scraped files
2. Cleans and validates data
3. Encodes categorical variables
4. Normalizes numerical features
5. Creates train/test/activation splits
6. Saves processed CSV files as required by Subgoal 2

Author: G (Team Lead - Data Engineer)
Week: 2 (Subgoal 2: Data Preparation)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler
import pickle
import json
from datetime import datetime


# NSL-KDD Feature Names (41 features + 1 label + 1 difficulty)
FEATURE_NAMES = [
    # Basic connection features (9)
    'duration', 'protocol_type', 'service', 'flag',
    'src_bytes', 'dst_bytes', 'land', 'wrong_fragment', 'urgent',
    
    # Content features (13)
    'hot', 'num_failed_logins', 'logged_in', 'num_compromised',
    'root_shell', 'su_attempted', 'num_root', 'num_file_creations',
    'num_shells', 'num_access_files', 'num_outbound_cmds',
    'is_host_login', 'is_guest_login',
    
    # Time-based traffic features (9)
    'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
    'rerror_rate', 'srv_rerror_rate', 'same_srv_rate',
    'diff_srv_rate', 'srv_diff_host_rate',
    
    # Host-based features (10)
    'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate',
    'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
    'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
    'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
    'dst_host_srv_rerror_rate',
    
    # Labels
    'label', 'difficulty'
]


class NSLKDDPreprocessor:
    """
    Comprehensive preprocessor for NSL-KDD dataset.
    """
    
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        
        # Create processed directory
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Store preprocessing artifacts
        self.label_encoders = {}
        self.scaler = None
        self.feature_names_original = None
        self.feature_names_processed = None
        
        # Statistics
        self.stats = {
            'start_time': datetime.now().isoformat(),
            'raw_train_records': 0,
            'raw_test_records': 0,
            'cleaned_records': 0,
            'final_train_records': 0,
            'final_test_records': 0,
            'activation_records': 0,
        }
    
    def load_raw_data(self):
        """
        Load raw NSL-KDD data from scraped files.
        """
        print("="*60)
        print("STEP 1: LOADING RAW DATA")
        print("="*60)
        
        train_file = self.raw_dir / "KDDTrain+.txt"
        test_file = self.raw_dir / "KDDTest+.txt"
        
        # Load training data
        print(f"\n📂 Loading training data from: {train_file.name}")
        try:
            df_train = pd.read_csv(train_file, header=None, names=FEATURE_NAMES)
            self.stats['raw_train_records'] = len(df_train)
            print(f"✅ Loaded {len(df_train):,} training records")
        except FileNotFoundError:
            print(f"❌ Training file not found: {train_file}")
            print("   Run scraping first: python code/scraping/scrape_nslkdd.py")
            return None, None
        
        # Load testing data
        print(f"\n📂 Loading testing data from: {test_file.name}")
        try:
            df_test = pd.read_csv(test_file, header=None, names=FEATURE_NAMES)
            self.stats['raw_test_records'] = len(df_test)
            print(f"✅ Loaded {len(df_test):,} testing records")
        except FileNotFoundError:
            print(f"❌ Testing file not found: {test_file}")
            return None, None
        
        # Show data overview
        print(f"\n📊 Data Overview:")
        print(f"   Training records: {len(df_train):,}")
        print(f"   Testing records: {len(df_test):,}")
        print(f"   Total records: {len(df_train) + len(df_test):,}")
        print(f"   Features: {len(FEATURE_NAMES) - 2} (excluding label and difficulty)")
        
        return df_train, df_test
    
    def clean_data(self, df, dataset_name="dataset"):
        """
        Clean the dataset: handle missing values, duplicates, data types.
        """
        print(f"\n{'='*60}")
        print(f"STEP 2: CLEANING {dataset_name.upper()}")
        print("="*60)
        
        print(f"\n📊 Initial state:")
        print(f"   Records: {len(df):,}")
        print(f"   Features: {len(df.columns)}")
        
        # Remove difficulty column (not needed for training)
        if 'difficulty' in df.columns:
            df = df.drop('difficulty', axis=1)
            print(f"\n🗑️  Removed 'difficulty' column")
        
        # Check for missing values
        missing = df.isnull().sum().sum()
        print(f"\n🔍 Missing values: {missing}")
        
        if missing > 0:
            print("   Dropping rows with missing values...")
            df = df.dropna()
            print(f"   ✅ Dropped {missing} rows")
        
        # Remove duplicates
        duplicates = df.duplicated().sum()
        print(f"\n🔍 Duplicate rows: {duplicates}")
        
        if duplicates > 0:
            print("   Removing duplicates...")
            df = df.drop_duplicates()
            print(f"   ✅ Removed {duplicates} duplicates")
        
        # Validate data types
        print(f"\n🔍 Validating data types...")
        
        # Categorical columns
        categorical_cols = ['protocol_type', 'service', 'flag', 'label']
        for col in categorical_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        
        # Numerical columns should be numeric
        numerical_cols = [col for col in df.columns if col not in categorical_cols]
        for col in numerical_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Drop any rows that became NaN during type conversion
        before_count = len(df)
        df = df.dropna()
        after_count = len(df)
        
        if before_count != after_count:
            print(f"   ⚠️  Dropped {before_count - after_count} rows with invalid data types")
        
        print(f"\n✅ Cleaning complete:")
        print(f"   Final records: {len(df):,}")
        
        return df
    
    def encode_labels(self, df, dataset_name="dataset"):
        """
        Encode attack labels into binary and multi-class formats.
        """
        print(f"\n{'='*60}")
        print(f"STEP 3: ENCODING LABELS ({dataset_name.upper()})")
        print("="*60)
        
        # Clean label column (remove extra characters)
        df['label'] = df['label'].str.strip()
        
        # Create binary label (normal vs attack)
        df['label_binary'] = df['label'].apply(
            lambda x: 0 if 'normal' in x.lower() else 1
        )
        
        # Create multi-class label (normal, dos, probe, r2l, u2r)
        def categorize_attack(label):
            label_lower = label.lower()
            
            if 'normal' in label_lower:
                return 'normal'
            
            # DoS attacks
            dos_attacks = ['back', 'land', 'neptune', 'pod', 'smurf', 'teardrop',
                          'apache2', 'udpstorm', 'processtable', 'mailbomb']
            if any(attack in label_lower for attack in dos_attacks):
                return 'dos'
            
            # Probe attacks
            probe_attacks = ['ipsweep', 'nmap', 'portsweep', 'satan', 'mscan', 'saint']
            if any(attack in label_lower for attack in probe_attacks):
                return 'probe'
            
            # R2L attacks
            r2l_attacks = ['ftp_write', 'guess_passwd', 'imap', 'multihop', 'phf',
                          'spy', 'warezclient', 'warezmaster', 'sendmail', 'named',
                          'snmpgetattack', 'snmpguess', 'xlock', 'xsnoop', 'worm']
            if any(attack in label_lower for attack in r2l_attacks):
                return 'r2l'
            
            # U2R attacks
            u2r_attacks = ['buffer_overflow', 'loadmodule', 'perl', 'rootkit',
                          'httptunnel', 'ps', 'sqlattack', 'xterm']
            if any(attack in label_lower for attack in u2r_attacks):
                return 'u2r'
            
            return 'unknown'
        
        df['label_multiclass'] = df['label'].apply(categorize_attack)
        
        # Encode multi-class to numerical
        df['label_multiclass_encoded'] = df['label_multiclass'].map({
            'normal': 0,
            'dos': 1,
            'probe': 2,
            'r2l': 3,
            'u2r': 4,
            'unknown': -1
        })
        
        # Print label distributions
        print(f"\n📊 Binary Label Distribution:")
        print(df['label_binary'].value_counts().sort_index())
        print(f"\n   Normal: {(df['label_binary'] == 0).sum():,} ({(df['label_binary'] == 0).sum() / len(df) * 100:.1f}%)")
        print(f"   Attack: {(df['label_binary'] == 1).sum():,} ({(df['label_binary'] == 1).sum() / len(df) * 100:.1f}%)")
        
        print(f"\n📊 Multi-class Label Distribution:")
        print(df['label_multiclass'].value_counts())
        
        return df
    
    def encode_categorical_features(self, df_train, df_test):
        """
        Encode categorical variables using label encoding.
        """
        print(f"\n{'='*60}")
        print("STEP 4: ENCODING CATEGORICAL FEATURES")
        print("="*60)
        
        categorical_cols = ['protocol_type', 'service', 'flag']
        
        for col in categorical_cols:
            print(f"\n🔧 Encoding '{col}'...")
            print(f"   Unique values: {df_train[col].nunique()}")
            
            # Fit encoder on training data
            le = LabelEncoder()
            le.fit(df_train[col])
            
            # Transform both train and test
            df_train[col] = le.transform(df_train[col])
            
            # Handle unseen values in test set
            test_values = df_test[col].unique()
            unseen = set(test_values) - set(le.classes_)
            
            if unseen:
                print(f"   ⚠️  {len(unseen)} unseen values in test set")
                # Map unseen values to a default (most common class)
                df_test[col] = df_test[col].apply(
                    lambda x: le.transform([x])[0] if x in le.classes_ else le.transform([le.classes_[0]])[0]
                )
            else:
                df_test[col] = le.transform(df_test[col])
            
            # Store encoder for future use
            self.label_encoders[col] = le
            
            print(f"   ✅ Encoded to range: 0-{len(le.classes_)-1}")
        
        # Save encoders
        encoder_path = self.processed_dir / "label_encoders.pkl"
        with open(encoder_path, 'wb') as f:
            pickle.dump(self.label_encoders, f)
        print(f"\n💾 Saved label encoders to: {encoder_path.name}")
        
        return df_train, df_test
    
    def normalize_features(self, df_train, df_test):
        """
        Normalize numerical features using Min-Max scaling.
        """
        print(f"\n{'='*60}")
        print("STEP 5: NORMALIZING NUMERICAL FEATURES")
        print("="*60)
        
        # Identify numerical columns (exclude labels and categorical)
        exclude_cols = ['label', 'label_binary', 'label_multiclass', 
                       'label_multiclass_encoded', 'protocol_type', 'service', 'flag']
        
        numerical_cols = [col for col in df_train.columns if col not in exclude_cols]
        
        print(f"\n📊 Normalizing {len(numerical_cols)} numerical features")
        print(f"   Method: Min-Max Scaling (range: 0-1)")
        
        # Fit scaler on training data
        self.scaler = MinMaxScaler()
        df_train[numerical_cols] = self.scaler.fit_transform(df_train[numerical_cols])
        
        # Transform test data
        df_test[numerical_cols] = self.scaler.transform(df_test[numerical_cols])
        
        # Save scaler
        scaler_path = self.processed_dir / "scaler.pkl"
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        print(f"\n💾 Saved scaler to: {scaler_path.name}")
        
        # Show statistics
        print(f"\n✅ Normalization complete")
        print(f"   All numerical features now in range [0, 1]")
        
        return df_train, df_test
    
    def create_data_splits(self, df_train, df_test):
        """
        Create required data splits:
        - joint_data_collection.csv (all data combined)
        - training_data.csv (80% of joint)
        - test_data.csv (20% of joint)
        - activation_data.csv (1 sample from test)
        """
        print(f"\n{'='*60}")
        print("STEP 6: CREATING DATA SPLITS")
        print("="*60)
        
        # Combine train and test
        df_joint = pd.concat([df_train, df_test], ignore_index=True)
        print(f"\n📊 Joint dataset: {len(df_joint):,} records")
        self.stats['cleaned_records'] = len(df_joint)
        
        # Split into 80/20 with stratification
        print(f"\n✂️  Splitting into 80/20...")
        df_train_split, df_test_split = train_test_split(
            df_joint,
            test_size=0.2,
            random_state=42,
            stratify=df_joint['label_binary']  # Maintain class distribution
        )
        
        self.stats['final_train_records'] = len(df_train_split)
        self.stats['final_test_records'] = len(df_test_split)
        
        print(f"   Training split: {len(df_train_split):,} records (80%)")
        print(f"   Testing split: {len(df_test_split):,} records (20%)")
        
        # Verify stratification worked
        train_ratio = (df_train_split['label_binary'] == 1).sum() / len(df_train_split)
        test_ratio = (df_test_split['label_binary'] == 1).sum() / len(df_test_split)
        print(f"\n   Attack ratio in training: {train_ratio:.1%}")
        print(f"   Attack ratio in testing: {test_ratio:.1%}")
        print(f"   ✅ Stratification maintained")
        
        # Create activation data (1 normal + 1 attack example)
        print(f"\n🎯 Creating activation data...")
        normal_sample = df_test_split[df_test_split['label_binary'] == 0].sample(n=1, random_state=42)
        attack_sample = df_test_split[df_test_split['label_binary'] == 1].sample(n=1, random_state=42)
        df_activation = pd.concat([normal_sample, attack_sample], ignore_index=True)
        
        self.stats['activation_records'] = len(df_activation)
        
        print(f"   Activation data: {len(df_activation)} records")
        print(f"   - 1 normal traffic sample")
        print(f"   - 1 attack traffic sample")
        
        return df_joint, df_train_split, df_test_split, df_activation
    
    def save_processed_data(self, df_joint, df_train, df_test, df_activation):
        """
        Save processed data to CSV files as required by Subgoal 2.
        """
        print(f"\n{'='*60}")
        print("STEP 7: SAVING PROCESSED DATA")
        print("="*60)
        
        files = {
            'joint_data_collection.csv': df_joint,
            'training_data.csv': df_train,
            'test_data.csv': df_test,
            'activation_data.csv': df_activation
        }
        
        for filename, dataframe in files.items():
            filepath = self.processed_dir / filename
            dataframe.to_csv(filepath, index=False)
            
            size_mb = filepath.stat().st_size / (1024 * 1024)
            print(f"\n✅ {filename}")
            print(f"   Records: {len(dataframe):,}")
            print(f"   Size: {size_mb:.2f} MB")
            print(f"   Path: {filepath}")
        
        # Save processing statistics
        stats_path = self.processed_dir / "preprocessing_stats.json"
        self.stats['end_time'] = datetime.now().isoformat()
        
        with open(stats_path, 'w') as f:
            json.dump(self.stats, f, indent=2)
        
        print(f"\n💾 Saved statistics to: {stats_path.name}")
    
    def run(self):
        """
        Execute the complete preprocessing pipeline.
        """
        print("="*60)
        print("NSL-KDD DATA PREPROCESSING")
        print("Course: M. Grum: Advanced AI-based Application Systems")
        print("University of Potsdam")
        print("Author: G (Data Engineer)")
        print("="*60)
        
        # Step 1: Load raw data
        df_train_raw, df_test_raw = self.load_raw_data()
        if df_train_raw is None:
            return False
        
        # Step 2: Clean data
        df_train_clean = self.clean_data(df_train_raw, "training")
        df_test_clean = self.clean_data(df_test_raw, "testing")
        
        # Step 3: Encode labels
        df_train_labeled = self.encode_labels(df_train_clean, "training")
        df_test_labeled = self.encode_labels(df_test_clean, "testing")
        
        # Step 4: Encode categorical features
        df_train_encoded, df_test_encoded = self.encode_categorical_features(
            df_train_labeled, df_test_labeled
        )
        
        # Step 5: Normalize features
        df_train_normalized, df_test_normalized = self.normalize_features(
            df_train_encoded, df_test_encoded
        )
        
        # Step 6: Create splits
        df_joint, df_train_split, df_test_split, df_activation = self.create_data_splits(
            df_train_normalized, df_test_normalized
        )
        
        # Step 7: Save processed data
        self.save_processed_data(df_joint, df_train_split, df_test_split, df_activation)
        
        # Final summary
        print(f"\n{'='*60}")
        print("✅ PREPROCESSING COMPLETE!")
        print("="*60)
        print(f"\n📊 Final Statistics:")
        print(f"   Raw records processed: {self.stats['raw_train_records'] + self.stats['raw_test_records']:,}")
        print(f"   Final training records: {self.stats['final_train_records']:,}")
        print(f"   Final testing records: {self.stats['final_test_records']:,}")
        print(f"   Activation samples: {self.stats['activation_records']}")
        print(f"\n📁 Output location: {self.processed_dir.absolute()}")
        print(f"\n🎯 NEXT STEP: Train models (Week 4)")
        print("   - python code/training/train_ann.py")
        print("   - python code/training/train_ols.py")
        print("="*60)
        
        return True


def main():
    """Main entry point."""
    preprocessor = NSLKDDPreprocessor()
    success = preprocessor.run()
    
    import sys
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()