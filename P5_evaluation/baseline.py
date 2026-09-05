import argparse
import json
import pickle
from pathlib import Path

import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def calculate_fpr(y_true, y_pred):
    """
    Calculate False Positive Rate:
    FPR = FP / (FP + TN)
    """
    cm = confusion_matrix(y_true, y_pred)

    if cm.shape != (2, 2):
        return None

    tn, fp, fn, tp = cm.ravel()

    denominator = fp + tn

    if denominator == 0:
        return 0.0

    return fp / denominator


def main():
    parser = argparse.ArgumentParser(
        description="Logistic Regression baseline for network attack prediction."
    )

    parser.add_argument(
        "--train",
        required=True,
        help="Path to training CSV file."
    )

    parser.add_argument(
        "--test",
        required=True,
        help="Path to test CSV file."
    )

    parser.add_argument(
        "--target",
        required=True,
        help="Name of the target column."
    )

    parser.add_argument(
        "--output",
        default="P5_evaluation/baseline_metrics.json",
        help="Output JSON file for evaluation metrics."
    )

    parser.add_argument(
        "--model-output",
        default="P5_evaluation/logistic_regression_model.pkl",
        help="Output path for the trained Logistic Regression model."
    )

    args = parser.parse_args()

    # ---------------------------------------------------------
    # 1. Load datasets
    # ---------------------------------------------------------

    train_path = Path(args.train)
    test_path = Path(args.test)

    if not train_path.exists():
        raise FileNotFoundError(
            f"Training file not found: {train_path}"
        )

    if not test_path.exists():
        raise FileNotFoundError(
            f"Test file not found: {test_path}"
        )

    print("Loading training data...")
    train_df = pd.read_csv(train_path)

    print("Loading test data...")
    test_df = pd.read_csv(test_path)

    print(f"Training samples: {len(train_df)}")
    print(f"Test samples: {len(test_df)}")

    # ---------------------------------------------------------
    # 2. Check target column
    # ---------------------------------------------------------

    if args.target not in train_df.columns:
        raise ValueError(
            f"Target column '{args.target}' not found in training data."
        )

    if args.target not in test_df.columns:
        raise ValueError(
            f"Target column '{args.target}' not found in test data."
        )

    # ---------------------------------------------------------
    # 3. Use only common feature columns
    # ---------------------------------------------------------

    feature_columns = [
        column
        for column in train_df.columns
        if column in test_df.columns and column != args.target
    ]

    if not feature_columns:
        raise ValueError("No common feature columns found.")

    print(f"Number of features: {len(feature_columns)}")

    X_train = train_df[feature_columns]
    y_train = train_df[args.target]

    X_test = test_df[feature_columns]
    y_test = test_df[args.target]

    # ---------------------------------------------------------
    # 4. Check target
    # ---------------------------------------------------------

    print("\nTarget distribution in training data:")
    print(y_train.value_counts())

    if y_train.nunique() != 2:
        raise ValueError(
            "This baseline currently expects a binary target with exactly "
            "two classes."
        )

    # ---------------------------------------------------------
    # 5. Identify numerical and categorical features
    # ---------------------------------------------------------

    numeric_features = X_train.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_features = X_train.select_dtypes(
        exclude=["number"]
    ).columns.tolist()

    print(f"\nNumerical features: {len(numeric_features)}")
    print(f"Categorical features: {len(categorical_features)}")

    # ---------------------------------------------------------
    # 6. Numerical preprocessing
    # ---------------------------------------------------------

    numeric_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="median")
            ),
            (
                "scaler",
                StandardScaler()
            ),
        ]
    )

    # ---------------------------------------------------------
    # 7. Categorical preprocessing
    # ---------------------------------------------------------

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="most_frequent")
            ),
            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="ignore"
                )
            ),
        ]
    )

    # ---------------------------------------------------------
    # 8. Combine preprocessing
    # ---------------------------------------------------------

    transformers = []

    if numeric_features:
        transformers.append(
            (
                "numeric",
                numeric_pipeline,
                numeric_features
            )
        )

    if categorical_features:
        transformers.append(
            (
                "categorical",
                categorical_pipeline,
                categorical_features
            )
        )

    preprocessor = ColumnTransformer(
        transformers=transformers
    )

    # ---------------------------------------------------------
    # 9. Logistic Regression model
    # ---------------------------------------------------------

    logistic_model = LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        random_state=42
    )

    model = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor
            ),
            (
                "classifier",
                logistic_model
            ),
        ]
    )

    # ---------------------------------------------------------
    # 10. Train ONLY on training data
    # ---------------------------------------------------------

    print("\nTraining Logistic Regression baseline...")

    model.fit(
        X_train,
        y_train
    )

    print("Training completed.")

    # ---------------------------------------------------------
    # 11. Save trained model
    # ---------------------------------------------------------

    model_output_path = Path(args.model_output)

    model_output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        model_output_path,
        "wb"
    ) as file:
        pickle.dump(
            model,
            file
        )

    print(
        f"Model saved to: {model_output_path}"
    )

    # ---------------------------------------------------------
    # 12. Make predictions on TEST data
    # ---------------------------------------------------------

    print("\nGenerating test predictions...")

    y_pred = model.predict(X_test)

    probabilities = model.predict_proba(X_test)

    # Probability of positive class
    positive_probability = probabilities[:, 1]

    # ---------------------------------------------------------
    # 13. Calculate metrics
    # ---------------------------------------------------------

    pos_label = "ATTACK" if "ATTACK" in model.classes_ else (1 if 1 in model.classes_ else model.classes_[1])

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    precision = precision_score(
        y_test,
        y_pred,
        pos_label=pos_label,
        average="binary",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        pos_label=pos_label,
        average="binary",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        pos_label=pos_label,
        average="binary",
        zero_division=0
    )

    fpr = calculate_fpr(
        y_test,
        y_pred
    )

    try:
        roc_auc = roc_auc_score(
            y_test,
            positive_probability
        )
    except ValueError:
        roc_auc = None

    cm = confusion_matrix(
        y_test,
        y_pred
    )

    # ---------------------------------------------------------
    # 14. Convert confusion matrix to list
    # ---------------------------------------------------------

    confusion_matrix_list = cm.tolist()

    # ---------------------------------------------------------
    # 15. Prepare results
    # ---------------------------------------------------------

    results = {
        "model": "Logistic Regression",
        "dataset": {
            "train_file": str(train_path),
            "test_file": str(test_path),
            "train_samples": int(len(train_df)),
            "test_samples": int(len(test_df)),
            "num_features": int(len(feature_columns))
        },
        "metrics": {
            "accuracy": float(accuracy),
            "precision": float(precision),
            "recall": float(recall),
            "f1_score": float(f1),
            "false_positive_rate": (
                float(fpr)
                if fpr is not None
                else None
            ),
            "roc_auc": (
                float(roc_auc)
                if roc_auc is not None
                else None
            )
        },
        "confusion_matrix": confusion_matrix_list,
        "target_column": args.target,
        "features": feature_columns,
        "model_file": str(model_output_path)
    }

    # ---------------------------------------------------------
    # 16. Save metrics
    # ---------------------------------------------------------

    output_path = Path(args.output)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            results,
            file,
            indent=4
        )

    # ---------------------------------------------------------
    # 17. Display results
    # ---------------------------------------------------------

    print("\n========================================")
    print("LOGISTIC REGRESSION BASELINE RESULTS")
    print("========================================")

    print(f"Accuracy           : {accuracy:.4f}")
    print(f"Precision          : {precision:.4f}")
    print(f"Recall             : {recall:.4f}")
    print(f"F1-score           : {f1:.4f}")

    if fpr is not None:
        print(f"False Positive Rate: {fpr:.4f}")
    else:
        print("False Positive Rate: N/A")

    if roc_auc is not None:
        print(f"ROC-AUC            : {roc_auc:.4f}")
    else:
        print("ROC-AUC            : N/A")

    print("\nConfusion Matrix:")
    print(cm)

    print(
        f"\nMetrics saved to: {output_path}"
    )

    print(
        f"Model saved to: {model_output_path}"
    )


if __name__ == "__main__":
    main()