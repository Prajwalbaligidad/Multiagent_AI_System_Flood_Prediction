"""
Multi-Source Flood Data Collection & Synthetic Generator
Autonomous Multi-Agent AI System for Disaster Prediction

This script generates 6 hydrologically coherent, spatiotemporally aligned
data sources for flood disaster prediction across 5 monitoring stations:
1. weather_stations.csv (Atmospheric & meteorological parameters)
2. rainfall_sensors.csv (Hourly rainfall, cumulative precipitation, intensity)
3. river_discharge_sensors.csv (River level, warning/danger limits, discharge rate, waterlogging)
4. satellite_imagery.csv (Cloud cover, NDWI, surface water extent, SAR anomaly)
5. terrain_parameters.csv (Slope, elevation, soil type, infiltration rate, runoff coefficient)
6. historical_flood_events.csv (Recorded past flood events, peak levels, return periods)
"""

import math
import random
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
import pandas as pd

# Set deterministic seed for reproducibility
np.random.seed(42)
random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DIR = BASE_DIR / "dataset" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Station Metadata across representative Assam River Basin locations
STATIONS = [
    {
        "station_id": "STN_001_GUW",
        "station_name": "Guwahati_AWRMI",
        "district": "Kamrup Metropolitan",
        "latitude": 26.1445,
        "longitude": 91.7362,
        "river": "Brahmaputra",
        "warning_level_m": 49.68,
        "danger_level_m": 50.50,
        "hfl_m": 51.46,  # Highest Flood Level recorded historically
        "elevation_m": 55.0,
        "slope_deg": 2.5,
        "soil_type": "Silty Clay Loam",
        "infiltration_capacity_mmh": 8.5,
        "land_cover": "Urban / Built-up",
        "runoff_coefficient": 0.78,
        "base_flow_cms": 18500.0,
        "drainage_capacity_mmh": 25.0
    },
    {
        "station_id": "STN_002_DHU",
        "station_name": "Dhubri_Ghat",
        "district": "Dhubri",
        "latitude": 26.0198,
        "longitude": 89.9889,
        "river": "Brahmaputra",
        "warning_level_m": 28.62,
        "danger_level_m": 29.84,
        "hfl_m": 30.52,
        "elevation_m": 28.0,
        "slope_deg": 0.6,
        "soil_type": "Alluvial Clay",
        "infiltration_capacity_mmh": 4.2,
        "land_cover": "Riverine Floodplain / Agricultural",
        "runoff_coefficient": 0.38,
        "base_flow_cms": 24000.0,
        "drainage_capacity_mmh": 15.0
    },
    {
        "station_id": "STN_003_SIL",
        "station_name": "Silchar_Barak",
        "district": "Cachar",
        "latitude": 24.8333,
        "longitude": 92.7789,
        "river": "Barak",
        "warning_level_m": 19.83,
        "danger_level_m": 20.85,
        "hfl_m": 21.98,
        "elevation_m": 42.0,
        "slope_deg": 1.8,
        "soil_type": "Clayey Silt",
        "infiltration_capacity_mmh": 6.0,
        "land_cover": "Semi-Urban / Lowland",
        "runoff_coefficient": 0.65,
        "base_flow_cms": 2800.0,
        "drainage_capacity_mmh": 18.0
    },
    {
        "station_id": "STN_004_UDA",
        "station_name": "Udalguri_Dhansiri",
        "district": "Udalguri",
        "latitude": 26.6958,
        "longitude": 92.2578,
        "river": "Dhansiri (North)",
        "warning_level_m": 68.50,
        "danger_level_m": 69.80,
        "hfl_m": 71.10,
        "elevation_m": 165.0,
        "slope_deg": 11.5,
        "soil_type": "Gravelly Sandy Loam",
        "infiltration_capacity_mmh": 22.0,
        "land_cover": "Foothills / Forest / Tea Garden",
        "runoff_coefficient": 0.42,
        "base_flow_cms": 350.0,
        "drainage_capacity_mmh": 35.0
    },
    {
        "station_id": "STN_005_BAR",
        "station_name": "Barpeta_Beki",
        "district": "Barpeta",
        "latitude": 26.3200,
        "longitude": 91.0050,
        "river": "Beki",
        "warning_level_m": 44.10,
        "danger_level_m": 45.10,
        "hfl_m": 46.25,
        "elevation_m": 35.0,
        "slope_deg": 0.8,
        "soil_type": "Alluvial Loam",
        "infiltration_capacity_mmh": 7.0,
        "land_cover": "Wetlands / Cropland",
        "runoff_coefficient": 0.32,
        "base_flow_cms": 1900.0,
        "drainage_capacity_mmh": 12.0
    }
]

def generate_multi_source_dataset(num_days=30, start_date_str="2024-06-15 00:00:00"):
    start_time = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S")
    total_hours = num_days * 24
    timestamps = [start_time + timedelta(hours=i) for i in range(total_hours)]

    print(f"Generating multi-source data for {len(STATIONS)} stations over {num_days} days ({total_hours} hourly timestamps)...")

    # Arrays to store tabular data
    weather_records = []
    rainfall_records = []
    river_records = []
    satellite_records = []

    for stn in STATIONS:
        stn_id = stn["station_id"]
        stn_name = stn["station_name"]
        lat = stn["latitude"]
        lon = stn["longitude"]
        river = stn["river"]
        wl = stn["warning_level_m"]
        dl = stn["danger_level_m"]
        base_flow = stn["base_flow_cms"]
        drain_cap = stn["drainage_capacity_mmh"]

        # Track rolling cumulative rainfall and hydrological state
        rain_buffer = []
        current_river_level = wl - 3.5  # start comfortably below warning level
        current_discharge = base_flow
        soil_sat_current = 0.35  # starting soil saturation (35%)

        for step, ts in enumerate(timestamps):
            day_fraction = step / 24.0

            # -------------------------------------------------------------
            # Meteorological Simulation: Storm cycles
            # Flood storm event centered around Days 15 to 22
            # -------------------------------------------------------------
            # Background diurnal cycles
            hour_of_day = ts.hour
            diurnal_temp = 3.0 * math.cos((hour_of_day - 14) * 2 * math.pi / 24)

            # Storm wave profile (Monsoon depression intensity)
            if day_fraction < 10.0:
                # Normal pre-monsoon: light sporadic showers
                storm_factor = 0.05 + 0.10 * max(0, math.sin(day_fraction * 0.8))
                pressure_anomaly = 0.0
            elif 10.0 <= day_fraction < 15.0:
                # Building monsoon front
                storm_factor = 0.30 + 0.40 * ((day_fraction - 10) / 5.0)
                pressure_anomaly = -5.0 * ((day_fraction - 10) / 5.0)
            elif 15.0 <= day_fraction <= 22.0:
                # Severe Storm / Cloudburst episode peak
                peak_phase = math.sin((day_fraction - 15.0) / 7.0 * math.pi)
                storm_factor = 0.85 + 0.65 * peak_phase + 0.3 * random.random()
                pressure_anomaly = -14.0 * peak_phase - 4.0 * random.random()
            else:
                # Post-flood recession phase
                decay = math.exp(-(day_fraction - 22.0) / 3.0)
                storm_factor = 0.15 * decay + 0.05
                pressure_anomaly = -3.0 * decay

            # 1. Weather Station Parameters
            base_temp = 31.0 - (stn["elevation_m"] * 0.005)
            temperature = round(base_temp + diurnal_temp - (storm_factor * 6.5) + np.random.normal(0, 0.4), 2)
            humidity = min(99.5, max(45.0, round(65.0 + storm_factor * 33.0 + np.random.normal(0, 2.0), 1)))
            pressure_hpa = round(1008.0 + pressure_anomaly + np.random.normal(0, 0.6), 1)
            wind_speed = max(1.0, round(8.0 + storm_factor * 38.0 + np.random.normal(0, 2.5), 1))
            wind_gusts = max(wind_speed, round(wind_speed * (1.3 + 0.4 * random.random()), 1))
            wind_dir_deg = int((190 + storm_factor * 40 + np.random.normal(0, 15)) % 360)

            weather_records.append({
                "station_id": stn_id,
                "station_name": stn_name,
                "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
                "latitude": lat,
                "longitude": lon,
                "temperature_c": temperature,
                "relative_humidity_pct": humidity,
                "atmospheric_pressure_hpa": pressure_hpa,
                "wind_speed_kmh": wind_speed,
                "wind_gusts_kmh": wind_gusts,
                "wind_direction_deg": wind_dir_deg,
                "cloud_cover_pct": min(100, max(5, int(20 + storm_factor * 78 + np.random.normal(0, 5)))),
                "solar_radiation_wm2": max(0.0, round((800.0 * max(0, math.sin((hour_of_day - 6) * math.pi / 12)) * (1.0 - (humidity / 120.0))), 1))
            })

            # 2. Rainfall Sensor Parameters
            if storm_factor > 0.6:
                # Heavy to extreme convective rainfall
                rain_intensity_mean = storm_factor * 35.0
                hourly_rain = max(0.0, round(np.random.exponential(rain_intensity_mean), 2))
                if random.random() < 0.15:  # Occasional cloudburst spike
                    hourly_rain += round(np.random.uniform(25.0, 65.0), 2)
            elif storm_factor > 0.2:
                # Moderate rain
                hourly_rain = max(0.0, round(np.random.gamma(shape=1.5, scale=storm_factor * 8.0), 2))
            else:
                # Trace or no rain
                hourly_rain = round(random.choice([0.0, 0.0, 0.0, 0.2, 0.8, 1.5]), 2)

            rain_buffer.append(hourly_rain)
            cum_6h = round(sum(rain_buffer[-6:]), 2)
            cum_24h = round(sum(rain_buffer[-24:]), 2)

            if hourly_rain > 64.4:
                rain_cat = "Extremely Heavy Rain"
            elif hourly_rain > 35.5:
                rain_cat = "Very Heavy Rain"
            elif hourly_rain > 15.5:
                rain_cat = "Heavy Rain"
            elif hourly_rain > 2.5:
                rain_cat = "Moderate Rain"
            elif hourly_rain > 0.1:
                rain_cat = "Light Rain"
            else:
                rain_cat = "No Rain"

            rainfall_records.append({
                "station_id": stn_id,
                "station_name": stn_name,
                "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
                "latitude": lat,
                "longitude": lon,
                "hourly_rainfall_mm": hourly_rain,
                "cumulative_6h_rainfall_mm": cum_6h,
                "cumulative_24h_rainfall_mm": cum_24h,
                "rainfall_intensity_category": rain_cat
            })

            # 3. Hydrological & River Sensors (Flow routing simulation)
            # Upstream stations respond rapidly; downstream stations accumulate lagged flow
            lag = 4 if "UDA" in stn_id else (16 if "DHU" in stn_id else 8)
            effective_upstream_rain = np.mean(rain_buffer[-lag:]) if len(rain_buffer) >= lag else hourly_rain

            # Soil moisture infiltration vs runoff dynamics
            soil_sat_current = min(1.0, max(0.15, soil_sat_current + (hourly_rain * 0.008) - 0.003))

            # Hydrological target level based on rainfall and runoff
            runoff_volume_factor = (effective_upstream_rain * stn["runoff_coefficient"]) * (1.0 + 0.8 * soil_sat_current)
            target_level = (wl - 3.5) + (runoff_volume_factor * 0.12)
            if storm_factor > 0.8:
                # Peak overtopping simulation
                target_level = dl + 0.85 + (stn["hfl_m"] - dl) * (0.6 + 0.3 * random.random())

            # Smooth level inertia
            current_river_level = current_river_level * 0.94 + target_level * 0.06
            current_river_level = round(current_river_level, 3)

            # Discharge increases with power law relative to level
            head_ratio = max(0.2, (current_river_level - (wl - 5.0)) / 5.0)
            discharge_rate = round(base_flow * (head_ratio ** 1.8), 1)
            flow_velocity = round(1.2 * (head_ratio ** 0.5), 2)

            # Urban waterlogging occurs when rain exceeds drainage capacity or river overtops
            overtop_excess = max(0.0, current_river_level - dl)
            drainage_overload = max(0.0, hourly_rain - drain_cap)
            waterlogging_depth = round((overtop_excess * 75.0) + (drainage_overload * 1.4), 1)
            drainage_choke_ratio = min(1.0, round(0.10 + (waterlogging_depth / 60.0) + (0.35 * soil_sat_current), 2))

            river_records.append({
                "station_id": stn_id,
                "station_name": stn_name,
                "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
                "latitude": lat,
                "longitude": lon,
                "river_name": river,
                "water_level_m": current_river_level,
                "warning_level_m": wl,
                "danger_level_m": dl,
                "highest_flood_level_m": stn["hfl_m"],
                "discharge_rate_cumecs": discharge_rate,
                "flow_velocity_ms": flow_velocity,
                "waterlogging_depth_cm": waterlogging_depth,
                "drainage_choke_ratio": drainage_choke_ratio
            })

            # 4. Satellite Imagery & Remote Sensing Indicators
            # Cloud obstruction prevents optical view during storms; SAR detects surface water
            cloud_pct = min(100.0, max(5.0, round(15.0 + storm_factor * 82.0 + np.random.normal(0, 3.0), 1)))
            is_optical_occluded = cloud_pct > 65.0

            # Baseline water body area in observation footprint
            base_water_area_km2 = 25.0 if "GUW" in stn_id or "DHU" in stn_id else 8.0
            inundation_expansion_factor = max(1.0, 1.0 + (overtop_excess * 2.2) + (cum_24h * 0.008))
            surface_water_area_km2 = round(base_water_area_km2 * inundation_expansion_factor, 2)
            water_extent_change_pct = round(((surface_water_area_km2 - base_water_area_km2) / base_water_area_km2) * 100.0, 1)

            # NDWI (Normalized Difference Water Index: -1 to +1; open water > 0.3)
            ndwi_val = -0.25 + (0.65 * (surface_water_area_km2 / (base_water_area_km2 * 2.5)))
            ndwi = round(min(0.85, max(-0.45, ndwi_val + np.random.normal(0, 0.03))), 3)

            # SAR backscatter drops significantly over smooth open water sheets (dB becomes more negative)
            sar_backscatter_db = round(-12.5 - (min(15.0, water_extent_change_pct * 0.12)), 2)
            flood_confidence_pct = round(min(98.0, max(10.0, 20.0 + (water_extent_change_pct * 0.65))), 1)

            satellite_records.append({
                "station_id": stn_id,
                "station_name": stn_name,
                "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
                "latitude": lat,
                "longitude": lon,
                "cloud_cover_pct": cloud_pct,
                "optical_visibility_flag": not is_optical_occluded,
                "ndwi_index": ndwi,
                "surface_water_extent_km2": surface_water_area_km2,
                "water_extent_change_pct": water_extent_change_pct,
                "sar_backscatter_db": sar_backscatter_db,
                "satellite_flood_confidence_pct": flood_confidence_pct
            })

    # Save to CSV
    df_weather = pd.DataFrame(weather_records)
    df_rain = pd.DataFrame(rainfall_records)
    df_river = pd.DataFrame(river_records)
    df_sat = pd.DataFrame(satellite_records)

    df_weather.to_csv(RAW_DIR / "weather_stations.csv", index=False)
    df_rain.to_csv(RAW_DIR / "rainfall_sensors.csv", index=False)
    df_river.to_csv(RAW_DIR / "river_discharge_sensors.csv", index=False)
    df_sat.to_csv(RAW_DIR / "satellite_imagery.csv", index=False)

    # 5. Terrain Parameters (Static Geomorphological & Soil Profile)
    terrain_records = []
    for stn in STATIONS:
        terrain_records.append({
            "station_id": stn["station_id"],
            "station_name": stn["station_name"],
            "district": stn["district"],
            "latitude": stn["latitude"],
            "longitude": stn["longitude"],
            "elevation_m": stn["elevation_m"],
            "slope_deg": stn["slope_deg"],
            "soil_type": stn["soil_type"],
            "infiltration_capacity_mmh": stn["infiltration_capacity_mmh"],
            "land_cover_class": stn["land_cover"],
            "runoff_coefficient": stn["runoff_coefficient"],
            "drainage_density_km_km2": round(1.2 + (stn["slope_deg"] * 0.15), 2),
            "topographic_wetness_index": round(14.0 - (stn["slope_deg"] * 0.7), 2)
        })
    df_terrain = pd.DataFrame(terrain_records)
    df_terrain.to_csv(RAW_DIR / "terrain_parameters.csv", index=False)

    # 6. Historical Flood Disaster Records
    historical_events = [
        {"event_id": "FLD_HIST_2004", "station_id": "STN_001_GUW", "year": 2004, "peak_water_level_m": 51.46, "severity": "Catastrophic", "return_period_yrs": 50, "flood_duration_days": 18, "affected_population_k": 210.0, "breach_reported": True},
        {"event_id": "FLD_HIST_2012", "station_id": "STN_001_GUW", "year": 2012, "peak_water_level_m": 50.92, "severity": "Severe", "return_period_yrs": 20, "flood_duration_days": 12, "affected_population_k": 140.0, "breach_reported": False},
        {"event_id": "FLD_HIST_2020", "station_id": "STN_001_GUW", "year": 2020, "peak_water_level_m": 51.05, "severity": "Severe", "return_period_yrs": 25, "flood_duration_days": 15, "affected_population_k": 185.0, "breach_reported": True},
        {"event_id": "FLD_HIST_2022", "station_id": "STN_001_GUW", "year": 2022, "peak_water_level_m": 51.30, "severity": "Catastrophic", "return_period_yrs": 35, "flood_duration_days": 21, "affected_population_k": 260.0, "breach_reported": True},

        {"event_id": "FLD_HIST_2016", "station_id": "STN_002_DHU", "year": 2016, "peak_water_level_m": 30.22, "severity": "Severe", "return_period_yrs": 25, "flood_duration_days": 16, "affected_population_k": 320.0, "breach_reported": True},
        {"event_id": "FLD_HIST_2020", "station_id": "STN_002_DHU", "year": 2020, "peak_water_level_m": 30.40, "severity": "Catastrophic", "return_period_yrs": 35, "flood_duration_days": 22, "affected_population_k": 450.0, "breach_reported": True},
        {"event_id": "FLD_HIST_2022", "station_id": "STN_002_DHU", "year": 2022, "peak_water_level_m": 30.52, "severity": "Catastrophic", "return_period_yrs": 50, "flood_duration_days": 25, "affected_population_k": 520.0, "breach_reported": True},

        {"event_id": "FLD_HIST_2004", "station_id": "STN_003_SIL", "year": 2004, "peak_water_level_m": 21.65, "severity": "Severe", "return_period_yrs": 30, "flood_duration_days": 14, "affected_population_k": 180.0, "breach_reported": True},
        {"event_id": "FLD_HIST_2022", "station_id": "STN_003_SIL", "year": 2022, "peak_water_level_m": 21.98, "severity": "Catastrophic (Bethukandi breach)", "return_period_yrs": 100, "flood_duration_days": 28, "affected_population_k": 380.0, "breach_reported": True},

        {"event_id": "FLD_HIST_2017", "station_id": "STN_004_UDA", "year": 2017, "peak_water_level_m": 70.80, "severity": "Severe Flash Flood", "return_period_yrs": 20, "flood_duration_days": 4, "affected_population_k": 45.0, "breach_reported": True},
        {"event_id": "FLD_HIST_2022", "station_id": "STN_004_UDA", "year": 2022, "peak_water_level_m": 71.10, "severity": "Severe Flash Flood", "return_period_yrs": 25, "flood_duration_days": 6, "affected_population_k": 62.0, "breach_reported": True},

        {"event_id": "FLD_HIST_2019", "station_id": "STN_005_BAR", "year": 2019, "peak_water_level_m": 45.85, "severity": "Severe", "return_period_yrs": 20, "flood_duration_days": 19, "affected_population_k": 290.0, "breach_reported": True},
        {"event_id": "FLD_HIST_2022", "station_id": "STN_005_BAR", "year": 2022, "peak_water_level_m": 46.25, "severity": "Catastrophic", "return_period_yrs": 40, "flood_duration_days": 24, "affected_population_k": 410.0, "breach_reported": True}
    ]
    df_hist = pd.DataFrame(historical_events)
    df_hist.to_csv(RAW_DIR / "historical_flood_events.csv", index=False)

    print("\nDataset Generation Complete!")
    print(f"1. weather_stations.csv:        {len(df_weather)} rows")
    print(f"2. rainfall_sensors.csv:        {len(df_rain)} rows")
    print(f"3. river_discharge_sensors.csv: {len(df_river)} rows")
    print(f"4. satellite_imagery.csv:       {len(df_sat)} rows")
    print(f"5. terrain_parameters.csv:      {len(df_terrain)} rows")
    print(f"6. historical_flood_events.csv: {len(df_hist)} rows")
    print(f"Saved into: {RAW_DIR}")

if __name__ == "__main__":
    generate_multi_source_dataset()
