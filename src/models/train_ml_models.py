"""
ML Model Training for Specialist Disaster Agents
Autonomous Multi-Agent AI System for Flood Prediction

Trains 4 dedicated Random Forest ML models (one for each specialist agent):
1. Weather ML Model (Rainfall, 6h/24h accumulation, pressure drops, wind gusts)
2. Flood ML Model (River water level, danger buffers, 3h rise rate, discharge, waterlogging)
3. Terrain ML Model (Slope, soil infiltration, runoff coefficient, TWI, surge index)
4. Satellite ML Model (Optical NDWI, cloud cover, water extent %, SAR backscatter)

Outputs lightweight trained .joblib models for 100% local, instant inference without any LLM or API.
"""

from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROCESSED_FILE = BASE_DIR / "dataset" / "processed" / "aligned_flood_multimodal.csv"
MODEL_DIR = BASE_DIR / "src" / "models" / "saved_models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def label_ground_truth(df: pd.DataFrame) -> pd.DataFrame:
    """Labels multi-class flood hazard levels based on physical hydrological benchmarks."""
    labels = []
    scores = []

    for _, row in df.iterrows():
        wl = row["water_level_m"]
        dl = row["danger_level_m"]
        warn = row["warning_level_m"]
        rain = row["hourly_rainfall_mm"]
        cum24 = row["cumulative_24h_rainfall_mm"]
        ndwi = row["ndwi_index"]
        extent_chg = row["water_extent_change_pct"]
        sar_db = row["sar_backscatter_db"]
        choke = row["drainage_choke_ratio"]

        # Critical: Active river breach, extreme cloudburst, or massive surface inundation
        if (wl >= dl) or (rain >= 50.0) or (cum24 >= 150.0 and choke >= 0.8) or (extent_chg >= 80.0 and sar_db <= -22.0):
            labels.append("CRITICAL")
            scores.append(0.90)
        # High: Warning level breach, heavy accumulation, or significant standing water
        elif (wl >= warn) or (cum24 >= 75.0) or (extent_chg >= 40.0 and ndwi >= 0.25):
            labels.append("HIGH")
            scores.append(0.65)
        # Moderate: Approaching warning, persistent rain buildup, or elevated moisture
        elif ((warn - wl) <= 0.6) or (cum24 >= 35.0) or (extent_chg >= 15.0):
            labels.append("MODERATE")
            scores.append(0.35)
        # Low: Normal baseline
        else:
            labels.append("LOW")
            scores.append(0.05)

    df = df.copy()
    df["hazard_label"] = labels
    df["hazard_score_target"] = scores
    return df


def train_models():
    print(f"Loading preprocessed multimodal dataset from: {PROCESSED_FILE}")
    if not PROCESSED_FILE.exists():
        raise FileNotFoundError(f"Processed dataset not found: {PROCESSED_FILE}")

    df = pd.read_csv(PROCESSED_FILE)
    df = label_ground_truth(df)

    print(f"Dataset shape: {df.shape}")
    print(f"Target distribution:\n{df['hazard_label'].value_counts()}\n")

    # Domain Feature Sets
    feature_sets = {
        "weather": [
            "hourly_rainfall_mm",
            "cumulative_6h_rainfall_mm",
            "cumulative_24h_rainfall_mm",
            "wind_speed_kmh",
            "wind_gusts_kmh",
            "atmospheric_pressure_hpa",
            "pressure_drop_3h_hpa",
            "relative_humidity_pct"
        ],
        "flood": [
            "water_level_m",
            "danger_buffer_m",
            "warning_buffer_m",
            "water_level_rise_1h_m",
            "water_level_rise_3h_m",
            "discharge_rate_cumecs",
            "flow_velocity_ms",
            "waterlogging_depth_cm",
            "drainage_choke_ratio"
        ],
        "terrain": [
            "slope_deg",
            "elevation_m",
            "infiltration_capacity_mmh",
            "runoff_coefficient",
            "topographic_wetness_index",
            "effective_runoff_surge_index",
            "cumulative_24h_rainfall_mm"
        ],
        "satellite": [
            "satellite_cloud_cover_pct",
            "optical_visibility_flag",
            "ndwi_index",
            "surface_water_extent_km2",
            "water_extent_change_pct",
            "sar_backscatter_db"
        ]
    }

    y = df["hazard_label"]

    trained_models = {}

    for domain, features in feature_sets.items():
        print("=" * 60)
        print(f"TRAINING ML MODEL: {domain.upper()} AGENT")
        print(f"Features ({len(features)}): {features}")

        X = df[features].copy()
        # Handle booleans
        for col in X.columns:
            if X[col].dtype == bool:
                X[col] = X[col].astype(int)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.20, random_state=42, stratify=y
        )

        clf = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=4,
            random_state=42
        )
        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"Model Accuracy on Test Set: {acc * 100:.2f}%")

        # Save model and feature list
        model_payload = {
            "model": clf,
            "features": features,
            "classes": clf.classes_.tolist(),
            "accuracy": acc
        }
        model_path = MODEL_DIR / f"{domain}_model.joblib"
        joblib.dump(model_payload, model_path)
        print(f"Saved model to: {model_path}")
        trained_models[domain] = model_payload

    print("\n" + "=" * 60)
    print("ALL 4 SPECIALIST ML MODELS TRAINED & SAVED SUCCESSFULLY")
    print("Zero LLM / Zero API dependencies required.")
    print("=" * 60)


if __name__ == "__main__":
    train_models()
