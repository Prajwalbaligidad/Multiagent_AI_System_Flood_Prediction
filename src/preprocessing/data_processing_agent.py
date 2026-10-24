"""
Data Preprocessing Agent
Autonomous Multi-Agent AI System for Disaster Prediction

Responsibilities (from System Architecture):
- Cleans: Imputes missing values, trims noise, clamps physical bounds, removes duplicates.
- Validates: Checks physical sanity, schema constraints, and hydrological consistency rules.
- Aligns: Spatiotemporal alignment across station coordinates and hourly timestamps.
- Combines: Merges weather, rainfall, river, satellite, terrain, and historical records into
  a single multimodal dataset: aligned_flood_multimodal.csv
"""

import json
from pathlib import Path
from datetime import datetime
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DIR = BASE_DIR / "dataset" / "raw"
PROCESSED_DIR = BASE_DIR / "dataset" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

class DataProcessingAgent:
    def __init__(self, raw_dir: Path = RAW_DIR, processed_dir: Path = PROCESSED_DIR):
        self.raw_dir = raw_dir
        self.processed_dir = processed_dir
        self.report = {
            "execution_timestamp": datetime.now().isoformat(),
            "status": "INITIALIZING",
            "datasets_loaded": {},
            "cleaning_summary": {},
            "validation_results": {},
            "aligned_records_count": 0
        }

    def load_data(self):
        """Loads all multi-source raw files."""
        files = {
            "weather": self.raw_dir / "weather_stations.csv",
            "rainfall": self.raw_dir / "rainfall_sensors.csv",
            "river": self.raw_dir / "river_discharge_sensors.csv",
            "satellite": self.raw_dir / "satellite_imagery.csv",
            "terrain": self.raw_dir / "terrain_parameters.csv",
            "historical": self.raw_dir / "historical_flood_events.csv"
        }

        dfs = {}
        for key, filepath in files.items():
            if not filepath.exists():
                raise FileNotFoundError(f"Required raw dataset not found: {filepath}")
            dfs[key] = pd.read_csv(filepath)
            self.report["datasets_loaded"][key] = {
                "filepath": str(filepath),
                "rows": len(dfs[key]),
                "columns": list(dfs[key].columns)
            }
        return dfs

    def clean_datasets(self, dfs):
        """Cleans and standardizes raw datasets."""
        cleaning_stats = {}

        # 1. Weather cleaning
        w_df = dfs["weather"].copy()
        w_df["timestamp"] = pd.to_datetime(w_df["timestamp"])
        w_df = w_df.drop_duplicates(subset=["station_id", "timestamp"]).sort_values(["station_id", "timestamp"])
        w_df["temperature_c"] = w_df["temperature_c"].clip(lower=-10.0, upper=55.0)
        w_df["relative_humidity_pct"] = w_df["relative_humidity_pct"].clip(lower=0.0, upper=100.0)
        w_df["atmospheric_pressure_hpa"] = w_df["atmospheric_pressure_hpa"].clip(lower=870.0, upper=1080.0)
        w_df["wind_speed_kmh"] = w_df["wind_speed_kmh"].clip(lower=0.0, upper=250.0)
        w_df["wind_gusts_kmh"] = np.maximum(w_df["wind_speed_kmh"], w_df["wind_gusts_kmh"].fillna(w_df["wind_speed_kmh"]))
        cleaning_stats["weather_cleaned_rows"] = len(w_df)

        # 2. Rainfall cleaning
        r_df = dfs["rainfall"].copy()
        r_df["timestamp"] = pd.to_datetime(r_df["timestamp"])
        r_df = r_df.drop_duplicates(subset=["station_id", "timestamp"]).sort_values(["station_id", "timestamp"])
        r_df["hourly_rainfall_mm"] = r_df["hourly_rainfall_mm"].clip(lower=0.0, upper=500.0)
        cleaning_stats["rainfall_cleaned_rows"] = len(r_df)

        # 3. River discharge cleaning
        riv_df = dfs["river"].copy()
        riv_df["timestamp"] = pd.to_datetime(riv_df["timestamp"])
        riv_df = riv_df.drop_duplicates(subset=["station_id", "timestamp"]).sort_values(["station_id", "timestamp"])
        riv_df["water_level_m"] = riv_df["water_level_m"].clip(lower=0.0, upper=200.0)
        riv_df["discharge_rate_cumecs"] = riv_df["discharge_rate_cumecs"].clip(lower=0.0)
        riv_df["waterlogging_depth_cm"] = riv_df["waterlogging_depth_cm"].clip(lower=0.0, upper=500.0)
        riv_df["drainage_choke_ratio"] = riv_df["drainage_choke_ratio"].clip(lower=0.0, upper=1.0)
        cleaning_stats["river_cleaned_rows"] = len(riv_df)

        # 4. Satellite cleaning
        s_df = dfs["satellite"].copy()
        s_df["timestamp"] = pd.to_datetime(s_df["timestamp"])
        s_df = s_df.drop_duplicates(subset=["station_id", "timestamp"]).sort_values(["station_id", "timestamp"])
        s_df["cloud_cover_pct"] = s_df["cloud_cover_pct"].clip(lower=0.0, upper=100.0)
        s_df["ndwi_index"] = s_df["ndwi_index"].clip(lower=-1.0, upper=1.0)
        s_df["satellite_flood_confidence_pct"] = s_df["satellite_flood_confidence_pct"].clip(lower=0.0, upper=100.0)
        cleaning_stats["satellite_cleaned_rows"] = len(s_df)

        # 5. Terrain & Historical validation
        t_df = dfs["terrain"].copy()
        t_df["runoff_coefficient"] = t_df["runoff_coefficient"].clip(lower=0.05, upper=0.98)
        cleaning_stats["terrain_stations"] = len(t_df)

        h_df = dfs["historical"].copy()
        cleaning_stats["historical_events"] = len(h_df)

        self.report["cleaning_summary"] = cleaning_stats
        return {"weather": w_df, "rainfall": r_df, "river": riv_df, "satellite": s_df, "terrain": t_df, "historical": h_df}

    def validate_hydrology(self, dfs):
        """Validates physical and logical consistency."""
        validations = {}
        riv_df = dfs["river"]
        t_df = dfs["terrain"]

        # Check warning < danger < hfl
        inconsistent_levels = riv_df[
            (riv_df["warning_level_m"] >= riv_df["danger_level_m"]) |
            (riv_df["danger_level_m"] > riv_df["highest_flood_level_m"])
        ]
        validations["gauge_levels_consistent"] = len(inconsistent_levels) == 0

        # Check terrain slope & infiltration are positive
        validations["terrain_attributes_positive"] = bool((t_df["slope_deg"] >= 0).all() and (t_df["infiltration_capacity_mmh"] > 0).all())

        self.report["validation_results"] = validations
        return True

    def align_and_combine(self, dfs):
        """Spatiotemporally joins all data streams and engineers multimodal features."""
        w_df = dfs["weather"]
        r_df = dfs["rainfall"]
        riv_df = dfs["river"]
        s_df = dfs["satellite"]
        t_df = dfs["terrain"]
        h_df = dfs["historical"]

        # Rename duplicate cloud cover column before merge
        w_df = w_df.rename(columns={"cloud_cover_pct": "weather_cloud_cover_pct"})
        s_df = s_df.rename(columns={"cloud_cover_pct": "satellite_cloud_cover_pct"})

        # Merge dynamic streams on (station_id, timestamp)
        # Weather + Rainfall
        m1 = pd.merge(
            w_df,
            r_df[["station_id", "timestamp", "hourly_rainfall_mm", "cumulative_6h_rainfall_mm", "cumulative_24h_rainfall_mm", "rainfall_intensity_category"]],
            on=["station_id", "timestamp"],
            how="inner"
        )

        # + River sensors
        m2 = pd.merge(
            m1,
            riv_df[["station_id", "timestamp", "river_name", "water_level_m", "warning_level_m", "danger_level_m", "highest_flood_level_m", "discharge_rate_cumecs", "flow_velocity_ms", "waterlogging_depth_cm", "drainage_choke_ratio"]],
            on=["station_id", "timestamp"],
            how="inner"
        )

        # + Satellite imagery
        m3 = pd.merge(
            m2,
            s_df[["station_id", "timestamp", "satellite_cloud_cover_pct", "optical_visibility_flag", "ndwi_index", "surface_water_extent_km2", "water_extent_change_pct", "sar_backscatter_db", "satellite_flood_confidence_pct"]],
            on=["station_id", "timestamp"],
            how="inner"
        )

        # + Static Terrain attributes on station_id
        m4 = pd.merge(
            m3,
            t_df[["station_id", "district", "elevation_m", "slope_deg", "soil_type", "infiltration_capacity_mmh", "land_cover_class", "runoff_coefficient", "drainage_density_km_km2", "topographic_wetness_index"]],
            on="station_id",
            how="left"
        )

        # Summarize historical context per station (max historical level and most severe event)
        hist_summary = h_df.groupby("station_id").agg(
            hist_max_peak_level_m=("peak_water_level_m", "max"),
            hist_events_count=("event_id", "count"),
            hist_worst_return_period_yrs=("return_period_yrs", "max")
        ).reset_index()

        combined_df = pd.merge(m4, hist_summary, on="station_id", how="left")
        combined_df["hist_events_count"] = combined_df["hist_events_count"].fillna(0).astype(int)

        # -------------------------------------------------------------
        # Feature Engineering: Rate of change, anomalies & cross-modal indices
        # -------------------------------------------------------------
        combined_df = combined_df.sort_values(["station_id", "timestamp"]).reset_index(drop=True)

        # 1-hour and 3-hour river water level rate of rise
        combined_df["water_level_rise_1h_m"] = combined_df.groupby("station_id")["water_level_m"].diff().fillna(0.0).round(3)
        combined_df["water_level_rise_3h_m"] = combined_df.groupby("station_id")["water_level_m"].diff(3).fillna(0.0).round(3)

        # Danger level proximity metrics
        combined_df["danger_buffer_m"] = (combined_df["water_level_m"] - combined_df["danger_level_m"]).round(3)
        combined_df["warning_buffer_m"] = (combined_df["water_level_m"] - combined_df["warning_level_m"]).round(3)
        combined_df["is_above_warning"] = combined_df["water_level_m"] >= combined_df["warning_level_m"]
        combined_df["is_above_danger"] = combined_df["water_level_m"] >= combined_df["danger_level_m"]

        # Atmospheric pressure sudden drop over 3 hours
        combined_df["pressure_drop_3h_hpa"] = (-combined_df.groupby("station_id")["atmospheric_pressure_hpa"].diff(3)).fillna(0.0).round(2)

        # Runoff generation potential (Rainfall vs Infiltration capacity)
        combined_df["effective_runoff_surge_index"] = (
            (combined_df["hourly_rainfall_mm"] * combined_df["runoff_coefficient"]) / np.maximum(1.0, combined_df["infiltration_capacity_mmh"])
        ).round(3)

        self.report["aligned_records_count"] = len(combined_df)
        self.report["status"] = "SUCCESS"

        return combined_df

    def process(self):
        """Executes full pipeline and writes outputs."""
        print("DataProcessingAgent: Starting pipeline...")
        raw_dfs = self.load_data()
        cleaned_dfs = self.clean_datasets(raw_dfs)
        self.validate_hydrology(cleaned_dfs)
        combined_df = self.align_and_combine(cleaned_dfs)

        output_file = self.processed_dir / "aligned_flood_multimodal.csv"
        combined_df.to_csv(output_file, index=False)
        print(f"DataProcessingAgent: Wrote {len(combined_df)} aligned multimodal records to {output_file}")

        report_file = self.processed_dir / "preprocessing_report.json"
        with open(report_file, "w") as f:
            json.dump(self.report, f, indent=2)
        print(f"DataProcessingAgent: Audit report saved to {report_file}")

        return combined_df

if __name__ == "__main__":
    agent = DataProcessingAgent()
    agent.process()
