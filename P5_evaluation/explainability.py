"""
P5 - Explainability
SIH26153: Future Network Attack Forecasting

Purpose:
    Identify important features influencing model predictions.

Method:
    Permutation Feature Importance

Permutation importance measures how much model performance
decreases when a feature is randomly shuffled.

A large decrease means that the feature is important.

Important:
    - Use the test set only for final explanation/evaluation.
    - Do not train the model using the test set.
    - Do not include future-derived information as features.
"""

import argparse
import json
import pickle
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from sklearn.inspection import permutation_importance
from sklearn.metrics import accuracy_score


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate model feature importance."
    )

    parser.add_argument(
        "--model",
        required=True,
        help="Path to saved model (.pkl)."
    )

    parser.add_argument(
        "--test",
        required=True,
        help="Path to test CSV file."
    )

    parser.add_argument(
        "--target",
        required=True,
        help="Target/label column."
    )

    parser.add_argument(
        "--output",
        default="P5_evaluation/feature_importance.png",
        help="Output feature importance plot."
    )

    parser.add_argument(
        "--json-output",
        default="P5_evaluation/feature_importance.json",
        help="Output machine-readable importance data."
    )

    parser.add_argument(
        "--top",
        type=int,
        default=15,
        help="Number of top features to display."
    )

    return parser.parse_args()


def load_model(model_path):
    """
    Load a Python pickle model.
    """

    path = Path(model_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Model file not found: {path}"
        )

    with open(path, "rb") as file:
        model = pickle.load(file)

    return model


def main():

    args = parse_arguments()

    # ---------------------------------------------------------
    # 1. Load model
    # ---------------------------------------------------------

    print("Loading model...")

    model = load_model(
        args.model
    )

    # ---------------------------------------------------------
    # 2. Load test data
    # ---------------------------------------------------------

    print("Loading test data...")

    test_path = Path(args.test)

    if not test_path.exists():
        raise FileNotFoundError(
            f"Test file not found: {test_path}"
        )

    test_df = pd.read_csv(
        test_path
    )

    if args.target not in test_df.columns:
        raise ValueError(
            f"Target '{args.target}' not found "
            f"in test data."
        )

    X_test = test_df.drop(
        columns=[args.target]
    )

    y_test = test_df[args.target]

    # ---------------------------------------------------------
    # 3. Calculate baseline score
    # ---------------------------------------------------------

    print("Calculating baseline performance...")

    baseline_predictions = model.predict(
        X_test
    )

    baseline_score = accuracy_score(
        y_test,
        baseline_predictions
    )

    print(
        f"Baseline accuracy: {baseline_score:.4f}"
    )

    # ---------------------------------------------------------
    # 4. Calculate permutation importance
    # ---------------------------------------------------------

    print(
        "Calculating permutation feature importance..."
    )

    importance_result = permutation_importance(
        model,
        X_test,
        y_test,
        scoring="accuracy",
        n_repeats=10,
        random_state=42,
        n_jobs=-1
    )

    importance_df = pd.DataFrame(
        {
            "feature": X_test.columns,
            "importance_mean": (
                importance_result.importances_mean
            ),
            "importance_std": (
                importance_result.importances_std
            ),
        }
    )

    importance_df = (
        importance_df
        .sort_values(
            "importance_mean",
            ascending=False
        )
        .reset_index(drop=True)
    )

    # ---------------------------------------------------------
    # 5. Save JSON
    # ---------------------------------------------------------

    json_output = Path(
        args.json_output
    )

    json_output.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    top_features = importance_df.head(
        args.top
    )

    json_data = {
        "method": "Permutation Feature Importance",
        "scoring": "accuracy",
        "baseline_accuracy": float(
            baseline_score
        ),
        "features": [
            {
                "feature": row["feature"],
                "importance_mean": float(
                    row["importance_mean"]
                ),
                "importance_std": float(
                    row["importance_std"]
                ),
            }
            for _, row in top_features.iterrows()
        ],
    }

    with open(
        json_output,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            json_data,
            file,
            indent=4
        )

    # ---------------------------------------------------------
    # 6. Generate feature importance plot
    # ---------------------------------------------------------

    print("Generating feature importance plot...")

    plot_df = (
        top_features
        .sort_values(
            "importance_mean"
        )
    )

    plt.figure(
        figsize=(10, 7)
    )

    plt.barh(
        plot_df["feature"],
        plot_df["importance_mean"]
    )

    plt.xlabel(
        "Mean decrease in accuracy"
    )

    plt.ylabel(
        "Feature"
    )

    plt.title(
        "Top Features - Permutation Importance"
    )

    plt.tight_layout()

    output_path = Path(
        args.output
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    plt.savefig(
        output_path,
        dpi=300
    )

    plt.close()

    # ---------------------------------------------------------
    # 7. Display important features
    # ---------------------------------------------------------

    print()
    print("=" * 55)
    print("TOP IMPORTANT FEATURES")
    print("=" * 55)

    for _, row in top_features.iterrows():

        print(
            f"{row['feature']}: "
            f"{row['importance_mean']:.6f}"
        )

    print("=" * 55)

    print()
    print(
        f"Plot saved to: {output_path}"
    )

    print(
        f"Feature importance JSON saved to: "
        f"{json_output}"
    )


if __name__ == "__main__":
    main()