import pandas as pd
import numpy as np
import glob
import os

# ==============================
# P1 - DATA PREPROCESSING
# ==============================

INPUT_FOLDER = r".\data\CIC-IDS2017\MachineLearningCVE"
OUTPUT_FILE = r".\data\CIC-IDS2017\processed_data.csv"

files = glob.glob(os.path.join(INPUT_FOLDER, "*.csv"))

print("=" * 70)
print("P1 DATA PREPROCESSING STARTED")
print("=" * 70)

all_data = []

for file in files:

    # Skip our own output file if it already exists
    if os.path.basename(file) == "processed_data.csv":
        continue

    print("\nProcessing:", os.path.basename(file))

    # Read CSV
    df = pd.read_csv(file, low_memory=False)

    print("Original rows:", len(df))

    # Remove spaces from column names
    df.columns = df.columns.str.strip()

    # Find Label column safely
    label_column = None

    for col in df.columns:
        if col.strip().lower() == "label":
            label_column = col
            break

    if label_column is None:
        print("ERROR: Label column not found!")
        continue

    # Rename it consistently
    df.rename(columns={label_column: "Label"}, inplace=True)

    # Convert infinite values to NaN
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Remove duplicate rows
    before_duplicates = len(df)
    df.drop_duplicates(inplace=True)

    print("Duplicates removed:", before_duplicates - len(df))

    # Remove rows containing missing values
    before_missing = len(df)
    df.dropna(inplace=True)

    print("Missing-value rows removed:", before_missing - len(df))

    # Clean labels
    df["Label"] = df["Label"].astype(str).str.strip()

    # Convert BENIGN = 0, everything else = 1
    df["Label"] = df["Label"].apply(
        lambda x: 0 if x.upper() == "BENIGN" else 1
    )

    print("Clean rows:", len(df))
    print("Labels:", df["Label"].value_counts().to_dict())

    all_data.append(df)


# ==============================
# COMBINE ALL FILES
# ==============================

print("\n" + "=" * 70)
print("COMBINING DATASETS")
print("=" * 70)

processed = pd.concat(all_data, ignore_index=True)

print("Combined rows:", len(processed))
print("Columns:", len(processed.columns))


# ==============================
# HANDLE NUMERICAL VALUES
# ==============================

print("\nPreparing numerical features...")

feature_columns = processed.columns.drop("Label")

# Convert feature columns to numeric
for col in feature_columns:
    processed[col] = pd.to_numeric(processed[col], errors="coerce")

# Replace any new infinite values
processed.replace([np.inf, -np.inf], np.nan, inplace=True)

# Remove rows that became invalid
processed.dropna(inplace=True)


# ==============================
# NORMALIZATION
# ==============================

print("Normalizing numerical features...")

from sklearn.preprocessing import StandardScaler

X = processed.drop(columns=["Label"])
y = processed["Label"]

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

processed = pd.DataFrame(
    X_scaled,
    columns=X.columns
)

processed["Label"] = y.values


# ==============================
# SAVE FINAL DATASET
# ==============================

processed.to_csv(OUTPUT_FILE, index=False)

print("\n" + "=" * 70)
print("P1 PREPROCESSING COMPLETED")
print("=" * 70)

print("FINAL ROWS:", len(processed))
print("FINAL COLUMNS:", len(processed.columns))

print("\nFINAL LABEL COUNTS:")
print(processed["Label"].value_counts())

print("\nSAVED TO:")
print(OUTPUT_FILE)

print("=" * 70)