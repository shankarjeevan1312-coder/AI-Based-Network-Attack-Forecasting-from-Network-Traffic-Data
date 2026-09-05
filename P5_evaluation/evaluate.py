"""
P5 - Evaluation Engine
SIH26153: Future Network Attack Forecasting

This script evaluates predictions against ground-truth values.

Classification metrics:
    - Accuracy
    - Precision
    - Recall
    - F1-score
    - False Positive Rate
    - ROC-AUC
    - Confusion Matrix

Forecasting metrics:
    - MAE
    - RMSE

Important:
    Test/ground-truth data must not be used for model training.
"""

import argparse
import json
from pathlib import Path

import numpy as np

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    recall_score,
    roc_auc_score,
)


def load_array(file_path):
    """
    Load prediction/label data from CSV or NPY file.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {path}"
        )

    if path.suffix.lower() == ".npy":
        return np.load(path)

    if path.suffix.lower() == ".csv":
        data = np.loadtxt(
            path,
            delimiter=",",
            skiprows=1
        )
        return data

    raise ValueError(
        "Supported file formats are .csv and .npy"
    )


def flatten_array(array):
    """
    Convert an array to a one-dimensional vector.
    """

    return np.asarray(array).reshape(-1)


def calculate_classification_metrics(
    y_true,
    y_pred,
    y_probability=None
):
    """
    Calculate all requested classification metrics.
    """

    y_true = flatten_array(y_true)
    y_pred = flatten_array(y_pred)

    if len(y_true) != len(y_pred):
        raise ValueError(
            "y_true and y_pred must have the same length."
        )

    cm = confusion_matrix(
        y_true,
        y_pred
    )

    false_positive_rate = None

    if cm.shape == (2, 2):

        tn, fp, fn, tp = cm.ravel()

        if (fp + tn) > 0:
            false_positive_rate = fp / (fp + tn)
        else:
            false_positive_rate = 0.0

    results = {
        "accuracy": float(
            accuracy_score(
                y_true,
                y_pred
            )
        ),

        "precision": float(
            precision_score(
                y_true,
                y_pred,
                zero_division=0
            )
        ),

        "recall": float(
            recall_score(
                y_true,
                y_pred,
                zero_division=0
            )
        ),

        "f1_score": float(
            f1_score(
                y_true,
                y_pred,
                zero_division=0
            )
        ),

        "false_positive_rate": (
            float(false_positive_rate)
            if false_positive_rate is not None
            else None
        ),

        "confusion_matrix": cm.tolist(),
    }

    # ROC-AUC requires probability/score values
    # and at least two classes in y_true.
    if y_probability is not None:

        y_probability = flatten_array(
            y_probability
        )

        if len(y_probability) != len(y_true):
            raise ValueError(
                "Probability and label lengths "
                "must match."
            )

        try:
            results["roc_auc"] = float(
                roc_auc_score(
                    y_true,
                    y_probability
                )
            )

        except ValueError:
            results["roc_auc"] = None

    else:
        results["roc_auc"] = None

    return results


def calculate_forecasting_metrics(
    y_true,
    y_pred
):
    """
    Calculate MAE and RMSE for future-state prediction.
    """

    y_true = flatten_array(y_true)
    y_pred = flatten_array(y_pred)

    if len(y_true) != len(y_pred):
        raise ValueError(
            "Forecast arrays must have the same length."
        )

    mae = mean_absolute_error(
        y_true,
        y_pred
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_true,
            y_pred
        )
    )

    return {
        "mae": float(mae),
        "rmse": float(rmse),
    }


def main():

    parser = argparse.ArgumentParser(
        description="Evaluate network attack predictions."
    )

    parser.add_argument(
        "--true",
        required=True,
        help="Ground-truth labels (.csv or .npy)."
    )

    parser.add_argument(
        "--pred",
        required=True,
        help="Predicted labels (.csv or .npy)."
    )

    parser.add_argument(
        "--probability",
        required=False,
        help="Prediction probabilities/scores."
    )

    parser.add_argument(
        "--future-true",
        required=False,
        help="Actual future-state values."
    )

    parser.add_argument(
        "--future-pred",
        required=False,
        help="Predicted future-state values."
    )

    parser.add_argument(
        "--model",
        default="LSTM",
        help="Model name."
    )

    parser.add_argument(
        "--output",
        default="P5_evaluation/metrics.json",
        help="Output JSON file."
    )

    args = parser.parse_args()

    # ---------------------------------------------------------
    # Load classification data
    # ---------------------------------------------------------

    print("Loading ground-truth labels...")

    y_true = load_array(
        args.true
    )

    print("Loading predictions...")

    y_pred = load_array(
        args.pred
    )

    y_probability = None

    if args.probability:

        print(
            "Loading prediction probabilities..."
        )

        y_probability = load_array(
            args.probability
        )

    # ---------------------------------------------------------
    # Classification metrics
    # ---------------------------------------------------------

    print(
        "Calculating classification metrics..."
    )

    classification_metrics = (
        calculate_classification_metrics(
            y_true,
            y_pred,
            y_probability
        )
    )

    # ---------------------------------------------------------
    # Build results
    # ---------------------------------------------------------

    results = {
        "model": args.model,
        "classification": classification_metrics,
    }

    # ---------------------------------------------------------
    # Future-state metrics
    # ---------------------------------------------------------

    if args.future_true and args.future_pred:

        print(
            "Calculating future-state MAE/RMSE..."
        )

        future_true = load_array(
            args.future_true
        )

        future_pred = load_array(
            args.future_pred
        )

        forecasting_metrics = (
            calculate_forecasting_metrics(
                future_true,
                future_pred
            )
        )

        results["future_state"] = (
            forecasting_metrics
        )

    # ---------------------------------------------------------
    # Save JSON
    # ---------------------------------------------------------

    output_path = Path(
        args.output
    )

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
    # Display results
    # ---------------------------------------------------------

    print()
    print("=" * 55)
    print(f"{args.model} EVALUATION")
    print("=" * 55)

    for name, value in classification_metrics.items():

        print(
            f"{name}: {value}"
        )

    if "future_state" in results:

        print()
        print("Future-state metrics:")

        print(
            f"MAE:  "
            f"{results['future_state']['mae']}"
        )

        print(
            f"RMSE: "
            f"{results['future_state']['rmse']}"
        )

    print("=" * 55)

    print()
    print(
        f"Results saved to: {output_path}"
    )


if __name__ == "__main__":
    main()