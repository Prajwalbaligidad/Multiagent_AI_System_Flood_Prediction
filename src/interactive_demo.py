"""
Interactive Runtime Evaluator for Autonomous Multi-Agent Flood System
Enables live real-time input from evaluators/professors to test custom disaster scenarios.
"""

import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.agents import (
    WeatherAgent,
    FloodAgent,
    TerrainAgent,
    SatelliteAgent,
    MESSAGE_BUS
)

# Station Geomorphic & Threshold Profiles
STATION_PROFILES = {
    "1": {
        "station_id": "STN_001_GUW",
        "station_name": "Guwahati_AWRMI",
        "district": "Kamrup Metropolitan",
        "river_name": "Brahmaputra",
        "warning_level_m": 49.68,
        "danger_level_m": 50.50,
        "elevation_m": 55.0,
        "slope_deg": 2.5,
        "soil_type": "Silty Clay Loam",
        "infiltration_capacity_mmh": 8.5,
        "land_cover_class": "Urban / Built-up",
        "runoff_coefficient": 0.78,
        "topographic_wetness_index": 12.25
    },
    "2": {
        "station_id": "STN_002_DHU",
        "station_name": "Dhubri_Ghat",
        "district": "Dhubri",
        "river_name": "Brahmaputra",
        "warning_level_m": 28.62,
        "danger_level_m": 29.84,
        "elevation_m": 28.0,
        "slope_deg": 0.6,
        "soil_type": "Alluvial Clay",
        "infiltration_capacity_mmh": 4.2,
        "land_cover_class": "Riverine Floodplain",
        "runoff_coefficient": 0.38,
        "topographic_wetness_index": 13.58
    },
    "3": {
        "station_id": "STN_003_SIL",
        "station_name": "Silchar_Barak",
        "district": "Cachar",
        "river_name": "Barak",
        "warning_level_m": 19.83,
        "danger_level_m": 20.85,
        "elevation_m": 42.0,
        "slope_deg": 1.8,
        "soil_type": "Clayey Silt",
        "infiltration_capacity_mmh": 6.0,
        "land_cover_class": "Semi-Urban / Lowland",
        "runoff_coefficient": 0.60,
        "topographic_wetness_index": 12.74
    },
    "4": {
        "station_id": "STN_004_UDA",
        "station_name": "Udalguri_Dhansiri",
        "district": "Udalguri",
        "river_name": "Dhansiri (North)",
        "warning_level_m": 68.50,
        "danger_level_m": 69.80,
        "elevation_m": 165.0,
        "slope_deg": 11.5,
        "soil_type": "Gravelly Sandy Loam",
        "infiltration_capacity_mmh": 22.0,
        "land_cover_class": "Foothills / Forest",
        "runoff_coefficient": 0.42,
        "topographic_wetness_index": 5.95
    },
    "5": {
        "station_id": "STN_005_BAR",
        "station_name": "Barpeta_Beki",
        "district": "Barpeta",
        "river_name": "Beki",
        "warning_level_m": 44.10,
        "danger_level_m": 45.10,
        "elevation_m": 35.0,
        "slope_deg": 0.8,
        "soil_type": "Alluvial Loam",
        "infiltration_capacity_mmh": 7.0,
        "land_cover_class": "Wetlands / Cropland",
        "runoff_coefficient": 0.32,
        "topographic_wetness_index": 13.44
    }
}


def get_float_input(prompt: str, default: float) -> float:
    try:
        user_val = input(f"{prompt} [default {default}]: ").strip()
        if not user_val:
            return default
        return float(user_val)
    except ValueError:
        print(f"Invalid input, using default: {default}")
        return default


def run_interactive_evaluator(custom_obs=None):
    MESSAGE_BUS.clear()
    print("=" * 90)
    print("AUTONOMOUS MULTI-AGENT FLOOD SYSTEM - LIVE RUNTIME EVALUATOR")
    print("Input custom real-time sensor parameters to test autonomous agent deliberation")
    print("=" * 90)

    if custom_obs is None:
        print("\nSelect a Monitoring Station:")
        print("  [1] Guwahati_AWRMI   (Brahmaputra Basin, Warning: 49.68m, Danger: 50.50m)")
        print("  [2] Dhubri_Ghat      (Downstream Floodplain, Warning: 28.62m, Danger: 29.84m)")
        print("  [3] Silchar_Barak    (Barak Valley, Warning: 19.83m, Danger: 20.85m)")
        print("  [4] Udalguri_Dhansiri(Foothill Tributary, Warning: 68.50m, Danger: 69.80m)")
        print("  [5] Barpeta_Beki     (Lowland Wetlands, Warning: 44.10m, Danger: 45.10m)")
        
        stn_choice = input("\nEnter choice [1-5] (default 1): ").strip() or "1"
        stn = STATION_PROFILES.get(stn_choice, STATION_PROFILES["1"])

        print(f"\nEnter Live Telemetry for {stn['station_name']} (Press Enter to accept default):")
        print("-" * 70)
        
        # Suggested default baseline values
        def_rain = 15.0
        def_cum24 = 65.0
        def_wl = stn["warning_level_m"] - 0.5
        def_wl_rise_3h = 0.15
        def_logging = 15.0
        def_choke = 0.35
        def_cloud = 45.0
        def_ndwi = 0.15
        def_sar = -14.5
        def_pressure = 1004.0
        def_pressure_drop = 2.0
        def_gusts = 35.0

        rain = get_float_input("  * Hourly Rainfall (mm/h)", def_rain)
        cum24 = get_float_input("  * 24h Cumulative Rainfall (mm)", def_cum24)
        wl = get_float_input(f"  * River Water Level (meters) [Danger: {stn['danger_level_m']}m]", def_wl)
        wl_rise_3h = get_float_input("  * 3h River Rise Rate (meters)", def_wl_rise_3h)
        logging = get_float_input("  * Street Waterlogging Depth (cm)", def_logging)
        choke = min(1.0, max(0.0, get_float_input("  * Drainage Choke Ratio (0.0 to 1.0)", def_choke)))
        cloud = min(100.0, max(0.0, get_float_input("  * Satellite Cloud Cover (%)", def_cloud)))
        ndwi = min(1.0, max(-1.0, get_float_input("  * Satellite Optical NDWI (-1.0 to +1.0)", def_ndwi)))
        sar = get_float_input("  * SAR Radar Backscatter in dB (e.g. -12 normal, -24 flooded)", def_sar)
        pressure = get_float_input("  * Barometric Pressure (hPa)", def_pressure)
        pressure_drop = get_float_input("  * 3h Barometric Pressure Drop (hPa)", def_pressure_drop)
        gusts = get_float_input("  * Wind Gusts (km/h)", def_gusts)

        # Assemble full observation vector
        obs = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "station_id": stn["station_id"],
            "station_name": stn["station_name"],
            "district": stn["district"],
            "river_name": stn["river_name"],
            "warning_level_m": stn["warning_level_m"],
            "danger_level_m": stn["danger_level_m"],
            "elevation_m": stn["elevation_m"],
            "slope_deg": stn["slope_deg"],
            "soil_type": stn["soil_type"],
            "infiltration_capacity_mmh": stn["infiltration_capacity_mmh"],
            "land_cover_class": stn["land_cover_class"],
            "runoff_coefficient": stn["runoff_coefficient"],
            "topographic_wetness_index": stn["topographic_wetness_index"],
            "hourly_rainfall_mm": rain,
            "cumulative_6h_rainfall_mm": round(rain * 2.8, 1),
            "cumulative_24h_rainfall_mm": cum24,
            "rainfall_intensity_category": "Heavy Rain" if rain >= 15.5 else "Moderate Rain",
            "water_level_m": wl,
            "water_level_rise_1h_m": round(wl_rise_3h / 3.0, 3),
            "water_level_rise_3h_m": wl_rise_3h,
            "danger_buffer_m": round(wl - stn["danger_level_m"], 3),
            "warning_buffer_m": round(wl - stn["warning_level_m"], 3),
            "discharge_rate_cumecs": round(2500.0 * (max(0.2, (wl - (stn['warning_level_m'] - 3.0))) ** 1.8), 1),
            "flow_velocity_ms": 1.45,
            "waterlogging_depth_cm": logging,
            "drainage_choke_ratio": choke,
            "satellite_cloud_cover_pct": cloud,
            "optical_visibility_flag": cloud < 65.0,
            "ndwi_index": ndwi,
            "surface_water_extent_km2": 32.5 if ndwi < 0.3 else 125.0,
            "water_extent_change_pct": 25.0 if ndwi < 0.3 else 150.0,
            "sar_backscatter_db": sar,
            "satellite_flood_confidence_pct": 92.0,
            "atmospheric_pressure_hpa": pressure,
            "pressure_drop_3h_hpa": pressure_drop,
            "wind_speed_kmh": round(gusts * 0.7, 1),
            "wind_gusts_kmh": gusts,
            "relative_humidity_pct": 85.0,
            "effective_runoff_surge_index": round((rain * stn["runoff_coefficient"]) / max(1.0, stn["infiltration_capacity_mmh"]), 2)
        }
    else:
        obs = custom_obs

    print("\n" + "=" * 90)
    print(f"RUNNING AGENT DELIBERATION FOR: {obs['station_name']} | Time: {obs['timestamp']}")
    print(f"Inputs: Rain={obs['hourly_rainfall_mm']} mm/h | River Level={obs['water_level_m']}m (Danger: {obs['danger_level_m']}m) | NDWI={obs['ndwi_index']} | Cloud={obs['satellite_cloud_cover_pct']}%")
    print("=" * 90)

    # Instantiate the 4 Autonomous AI Agents
    weather_agent = WeatherAgent()
    flood_agent = FloodAgent()
    terrain_agent = TerrainAgent()
    satellite_agent = SatelliteAgent()

    # Execute Autonomous Agent Loop
    w_packet = weather_agent.run_agent_cycle(obs, MESSAGE_BUS)
    t_packet = terrain_agent.run_agent_cycle(obs, MESSAGE_BUS)
    f_packet = flood_agent.run_agent_cycle(obs, MESSAGE_BUS)
    s_packet = satellite_agent.run_agent_cycle(obs, MESSAGE_BUS)

    packets = [w_packet, f_packet, t_packet, s_packet]

    for p in packets:
        flags_str = ", ".join(p.critical_flags) if p.critical_flags else "None"
        print(f"\n  +-- [{p.agent_type} AGENT] ({p.operational_state})")
        print(f"  |   * risk_score:     {p.risk_score:.3f} ({p.risk_level})")
        print(f"  |   * confidence:     {p.confidence:.2f} ({int(p.confidence * 100)}%)")
        print(f"  |   * critical_flags: {flags_str}")
        print(f"  |   * action_trigger: {p.action_trigger}")
        if p.active_intentions:
            print(f"  |   * intentions:     {', '.join(p.active_intentions[:2])}")
        print(f"  +-------------------------------------------------------------")

    # Display inter-agent messages
    if MESSAGE_BUS.message_history:
        print("\n  >> INTER-AGENT MESSAGES EXCHANGED ON BLACKBOARD BUS:")
        for msg in MESSAGE_BUS.message_history:
            print(f"     * [{msg.sender_agent} -> {msg.recipient_agent}] {msg.performative}: {msg.subject}")

    print("\n" + "=" * 90)
    print("LIVE EVALUATION COMPLETE - 100% LOCAL REAL-TIME INFERENCE")
    print("=" * 90)

    return packets


if __name__ == "__main__":
    run_interactive_evaluator()
