"""
Interactive Runtime Evaluator for Autonomous Multi-Agent Flood System
Enables live real-time input from evaluators/professors to test custom disaster scenarios
across all 5 layers: Specialists -> Blackboard -> Fusion Agent -> Decision & Early Warning Agent.
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
    RiskAssessmentFusionAgent,
    DecisionEarlyWarningAgent,
    MESSAGE_BUS,
    STATION_PROFILES,
    get_station_profile
)


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
    print("=" * 95)
    print("AUTONOMOUS MULTI-AGENT FLOOD SYSTEM - LIVE RUNTIME EVALUATOR")
    print("Complete 5-Layer Autonomous Architecture with LLM Risk Assessment & Decision Guidance")
    print("=" * 95)

    if custom_obs is None:
        print("\nSelect a Monitoring Station:")
        print("  [1] Guwahati_AWRMI   (Brahmaputra Basin, Warning: 49.68m, Danger: 50.50m)")
        print("  [2] Dhubri_Ghat      (Downstream Floodplain, Warning: 28.62m, Danger: 29.84m)")
        print("  [3] Silchar_Barak    (Barak Valley, Warning: 19.83m, Danger: 20.85m)")
        print("  [4] Udalguri_Dhansiri(Foothill Tributary, Warning: 68.50m, Danger: 69.80m)")
        print("  [5] Barpeta_Beki     (Lowland Wetlands, Warning: 44.10m, Danger: 45.10m)")
        
        stn_choice = input("\nEnter choice [1-5] (default 1): ").strip() or "1"
        stn_keys = {"1": "Guwahati_AWRMI", "2": "Dhubri_Ghat", "3": "Silchar_Barak", "4": "Udalguri_Dhansiri", "5": "Barpeta_Beki"}
        stn_key = stn_keys.get(stn_choice, "Guwahati_AWRMI")
        stn = STATION_PROFILES[stn_key]

        print(f"\nEnter Live Telemetry for {stn['station_name']} (Press Enter to accept default):")
        print("-" * 75)
        
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
        stn = get_station_profile(obs.get("station_name", "Guwahati_AWRMI"))

    print("\n" + "=" * 95)
    print(f"RUNNING AGENT DELIBERATION FOR: {obs['station_name']} | Time: {obs['timestamp']}")
    print(f"Inputs: Rain={obs['hourly_rainfall_mm']} mm/h | River Level={obs['water_level_m']}m (Danger: {obs['danger_level_m']}m) | NDWI={obs['ndwi_index']} | Cloud={obs['satellite_cloud_cover_pct']}%")
    print("=" * 95)

    # 1. Instantiate the 4 Autonomous AI Agents
    weather_agent = WeatherAgent()
    flood_agent = FloodAgent()
    terrain_agent = TerrainAgent()
    satellite_agent = SatelliteAgent()
    fusion_agent = RiskAssessmentFusionAgent()
    decision_agent = DecisionEarlyWarningAgent()

    # 2. Execute Specialist Loops
    w_packet = weather_agent.run_agent_cycle(obs, MESSAGE_BUS)
    t_packet = terrain_agent.run_agent_cycle(obs, MESSAGE_BUS)
    f_packet = flood_agent.run_agent_cycle(obs, MESSAGE_BUS)
    s_packet = satellite_agent.run_agent_cycle(obs, MESSAGE_BUS)

    packets = [w_packet, f_packet, t_packet, s_packet]

    print("\n--- [LAYER 3: 4 SPECIALIST AGENT DECISIONS] ---")
    for p in packets:
        flags_str = ", ".join(p.critical_flags) if p.critical_flags else "None"
        print(f"  +-- [{p.agent_type} AGENT] ({p.operational_state})")
        print(f"  |   * risk_score:     {p.risk_score:.3f} ({p.risk_level}) | confidence: {int(p.confidence * 100)}%")
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

    # 3. Layer 4: Risk Assessment and Fusion Agent
    print("\n--- [LAYER 4: RISK ASSESSMENT & FUSION AGENT (LLM ENGINE)] ---")
    fused_assessment = fusion_agent.fuse_and_assess(
        station_profile=stn,
        weather_packet=w_packet,
        flood_packet=f_packet,
        terrain_packet=t_packet,
        satellite_packet=s_packet,
        bus=MESSAGE_BUS
    )

    confirm_badge = "[YES - CONFIRMED FLOOD EVENT]" if fused_assessment.flood_occurrence_confirmed else "[NO - BELOW FLOOD CRITERIA]"
    print(f"  * FLOOD OCCURRENCE CONFIRMED?   {confirm_badge}")
    print(f"  * Flood Event Status:          {fused_assessment.flood_event_status}")
    print(f"  * Flood Probability:           {fused_assessment.flood_probability_pct:.1f}%")
    print(f"  * Overall Severity Tier:       {fused_assessment.overall_severity_tier} (Risk Score: {fused_assessment.composite_risk_score:.3f})")
    print(f"  * Estimated Lead Time:         {fused_assessment.estimated_lead_time}")
    print(f"  * Primary Hazard Driver:       {fused_assessment.primary_hazard_driver}")
    print(f"  * Identified Vulnerable Zones: {', '.join(fused_assessment.identified_vulnerable_locations[:3])}")
    print(f"  * Headline Verdict:            \"{fused_assessment.headline_verdict}\"")

    # 4. Layer 5: Decision and Early Warning Agent
    print("\n--- [LAYER 5: DECISION & EARLY WARNING AGENT] ---")
    decision_packet = decision_agent.process_decision_cycle(
        assessment=fused_assessment,
        station_profile=stn
    )

    print(f"  * ALERT DISPATCH:              {decision_packet.alert_level_display}")
    print(f"  * SIREN COMMAND:               {decision_packet.siren_command}")
    print(f"  * PUBLIC BROADCAST SMS:        \"{decision_packet.public_broadcast_sms}\"")
    print("\n  * TOP RECOMMENDED TACTICAL ACTIONS:")
    for act in decision_packet.recommended_tactical_actions[:3]:
        print(f"    - [{act['priority']}] {act['action']} ({act['designated_agency']})")

    print("\n  * SPATIAL RISK MAP:")
    print(decision_packet.ascii_risk_map)

    print(f"\n  * GENERATED DECISION ARTIFACTS:")
    print(f"    - Interactive HTML Risk Map: file:///{decision_packet.html_risk_map_path.replace('\\', '/')}")
    print(f"    - Human Approval Report (MD): file:///{decision_packet.incident_report_md_path.replace('\\', '/')}")
    print(f"    - Machine-Readable Plan (JSON): file:///{decision_packet.incident_report_json_path.replace('\\', '/')}")

    print("\n" + "=" * 95)
    print("LIVE RUNTIME EVALUATION COMPLETE - 100% OFFLINE ZERO API TOKENS")
    print("=" * 95)

    return {
        "specialists": packets,
        "fused_assessment": fused_assessment,
        "decision_packet": decision_packet
    }


if __name__ == "__main__":
    run_interactive_evaluator()
