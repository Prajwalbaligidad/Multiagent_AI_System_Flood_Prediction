"""
Comprehensive Model Evaluation Script
Computes Accuracy, Precision, Recall, F1-Score, Confusion Matrix, MSE, and RMSE
for all 4 Specialist AI Agents.
"""

import sys
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    mean_squared_error
)
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.models.train_ml_models import label_ground_truth

PROCESSED_FILE = BASE_DIR / "dataset" / "processed" / "aligned_flood_multimodal.csv"
MODEL_DIR = BASE_DIR / "src" / "models" / "saved_models"
OUTPUT_DIR = BASE_DIR / "analysis_output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def evaluate_all():
    print("=" * 80)
    print("EVALUATING SPECIALIST AGENT ML MODELS")
    print("Metrics: Accuracy, Precision, Recall, F1-Score, Confusion Matrix, MSE, RMSE")
    print("=" * 80)

    df = pd.read_csv(PROCESSED_FILE)
    df = label_ground_truth(df)

    y_true_cls = df["hazard_label"]
    y_true_reg = df["hazard_score_target"]
    classes = ["LOW", "MODERATE", "HIGH", "CRITICAL"]

    class_weights = {"LOW": 0.05, "MODERATE": 0.35, "HIGH": 0.65, "CRITICAL": 0.95}

    all_metrics = {}

    for domain in ["weather", "flood", "terrain", "satellite"]:
        model_path = MODEL_DIR / f"{domain}_model.joblib"
        payload = joblib.load(model_path)
        model = payload["model"]
        features = payload["features"]
        model_classes = payload["classes"]

        X = df[features].copy()
        for col in X.columns:
            if X[col].dtype == bool:
                X[col] = X[col].astype(int)

        # Classification predictions
        y_pred_cls = model.predict(X)
        pred_proba = model.predict_proba(X)

        # Continuous risk score prediction
        y_pred_reg = np.array([
            sum(prob * class_weights.get(cls, 0.1) for cls, prob in zip(model_classes, probs))
            for probs in pred_proba
        ])

        acc = accuracy_score(y_true_cls, y_pred_cls)
        prec = precision_score(y_true_cls, y_pred_cls, average="weighted", zero_division=0)
        rec = recall_score(y_true_cls, y_pred_cls, average="weighted", zero_division=0)
        f1 = f1_score(y_true_cls, y_pred_cls, average="weighted", zero_division=0)
        cm = confusion_matrix(y_true_cls, y_pred_cls, labels=classes)

        mse = mean_squared_error(y_true_reg, y_pred_reg)
        rmse = np.sqrt(mse)

        print(f"\n--- {domain.upper()} AGENT EVALUATION ---")
        print(f"Accuracy:        {acc * 100:.2f}%")
        print(f"Precision (wtd): {prec * 100:.2f}%")
        print(f"Recall (wtd):    {rec * 100:.2f}%")
        print(f"F1-Score (wtd):  {f1 * 100:.2f}%")
        print(f"MSE:             {mse:.6f}")
        print(f"RMSE:            {rmse:.6f}")
        print("Confusion Matrix (Classes: LOW, MODERATE, HIGH, CRITICAL):")
        print(pd.DataFrame(cm, index=[f"Actual_{c}" for c in classes], columns=[f"Pred_{c}" for c in classes]))

        all_metrics[domain] = {
            "accuracy": round(acc, 4),
            "precision_weighted": round(prec, 4),
            "recall_weighted": round(rec, 4),
            "f1_score_weighted": round(f1, 4),
            "mse": round(mse, 6),
            "rmse": round(rmse, 6),
            "confusion_matrix": {
                "classes": classes,
                "matrix": cm.tolist()
            }
        }

    metrics_file = OUTPUT_DIR / "model_evaluation_metrics.json"
    with open(metrics_file, "w") as f:
        json.dump(all_metrics, f, indent=2)

    print(f"\nSaved evaluation metrics to: {metrics_file}")
    return all_metrics


if __name__ == "__main__":
    evaluate_all()
