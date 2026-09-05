# P1 — Data Preprocessing Report

## 1. Dataset

**Dataset:** CIC-IDS2017

The CIC-IDS2017 network traffic dataset was used as the primary dataset for the project. Multiple CSV files containing benign and attack traffic were processed and combined.

## 2. Input Data

The preprocessing pipeline processed the following traffic files:

- Friday-WorkingHours-Afternoon-DDos
- Friday-WorkingHours-Afternoon-PortScan
- Friday-WorkingHours-Morning
- Monday-WorkingHours
- Thursday-WorkingHours-Afternoon-Infilteration
- Thursday-WorkingHours-Morning-WebAttacks
- Tuesday-WorkingHours
- Wednesday-workingHours

## 3. Preprocessing Steps

The following preprocessing operations were performed:

1. Loaded the CIC-IDS2017 CSV files.
2. Inspected the dataset structure and column names.
3. Removed duplicate rows.
4. Handled missing values.
5. Handled infinite numerical values.
6. Encoded the target labels.
7. Separated input features from the target label.
8. Converted numerical features into a suitable numerical representation.
9. Normalized numerical features using standard scaling.
10. Combined the cleaned datasets into a single processed dataset.

## 4. Final Dataset

After preprocessing and combining the datasets:

- **Rows:** 2,572,640
- **Columns:** 79
- **Target column:** `Label`

### Label Encoding

| Encoded Value | Meaning |
|---|---|
| 0 | BENIGN |
| 1 | ATTACK |

### Final Label Distribution

| Label | Count |
|---|---:|
| BENIGN (0) | 2,146,899 |
| ATTACK (1) | 425,741 |

## 5. Data Quality

The preprocessing pipeline removed duplicate records and rows containing invalid/missing numerical values before creating the final dataset.

Infinite numerical values were also handled during preprocessing.

## 6. Normalization

Numerical input features were normalized using standard scaling so that features with different numerical ranges can be used effectively by downstream machine-learning and deep-learning models.

## 7. Output

The final processed dataset was saved as:

`data/CIC-IDS2017/processed_data.csv`

This file is the primary input dataset for the subsequent Network State and Temporal Dataset stage (P2).

## 8. P1 Status

**P1 — Data & Preprocessing: COMPLETED**

The processed dataset is ready for the next stage of the project.