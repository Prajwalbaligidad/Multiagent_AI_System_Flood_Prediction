"""
Live Autonomous Multi-Agent Flood Disaster Monitor
Autonomous Multi-Agent AI System for Disaster Prediction

Takes any user-provided place/area name, retrieves live real-time telemetry
(Weather, Terrain DEM, GloFAS River Discharge, Satellite indices) via free APIs,
computes risk scores across all 4 specialist agents, fuses assessments via
the Local Cognitive LLM Engine, and performs dynamic continuous evacuation
safety re-assessment with automatic safe haven re-routing.
"""

import sys
import argparse
from datetime import datetime
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.services.live_data_service import LiveDataService
from src.agents.base_agent import MESSAGE_BUS
from src.agents.weather_agent import WeatherAgent
from src.agents.flood_agent import FloodAgent
from src.agents.terrain_agent import TerrainAgent
from src.agents.satellite_agent import SatelliteAgent
from src.agents.risk_assessment_fusion_agent import RiskAssessmentFusionAgent
from src.agents.decision_early_warning_agent import DecisionEarlyWarningAgent


def run_live_monitor(location_name: str, surge_mode: str = "LIVE"):
    """
    Executes live multi-agent flood prediction and dynamic evacuation re-assessment
    for any specified geographic area name.
    """
    print("\n" + "=" * 95)
    print(f"[+] AUTONOMOUS MULTI-AGENT LIVE DISASTER MONITOR: [{location_name.upper()}]")
    print(f"Mode: {'REAL-TIME TELEMETRY' if surge_mode == 'LIVE' else 'LIVE LOCATION + SIMULATED MONSOON CLOUDBURST STRESS'}")
    print("=" * 95)

    # 1. Geocode Location & Ingest Live Matrices
    print(f"\n[Step 1] Geocoding '{location_name}' and fetching live multi-modal matrices...")
    live_service = LiveDataService()
    geo = live_service.geocode(location_name)

    if not geo.get("found", True):
        print(f"  [!] Note: Exact match not found via geocoder, using regional coordinates for {location_name}.")

    lat = geo["latitude"]
    lon = geo["longitude"]
    district = geo["district"]
    state = geo["state"]
    country = geo["country"]
    base_elev = geo["elevation"]

    print(f"  * Geocoded Location: {geo['name']} ({district}, {state}, {country})")
    print(f"  * Coordinates:       Lat {lat:.4f} N | Lon {lon:.4f} E | Elevation: {base_elev}m")

    # Ingest Live Telemetry
    obs, stn_profile = live_service.fetch_live_matrices(
        lat=lat,
        lon=lon,
        location_name=geo["name"],
        district=district,
        state=state,
        river_name=geo.get("river", f"{district} River Basin"),
        convective_surge_mode="DELUGE" if surge_mode == "SURGE" else ("WATCH" if surge_mode == "WATCH" else None)
    )

    print("\n  >> LIVE SENSOR MATRICES RETRIEVED:")
    print(f"     * Weather:   Rainfall={obs['hourly_rainfall_mm']} mm/h | 24h Accum={obs['cumulative_24h_rainfall_mm']:.1f} mm | Wind={obs['wind_speed_kmh']} km/h")
    print(f"     * Terrain:   Elevation={obs['elevation_m']}m | Slope={obs['slope_deg']:.1f} deg | Wetness Index={obs['topographic_wetness_index']}")
    print(f"     * Hydrology: River Discharge={obs['discharge_rate_cumecs']} m3/s | Gauge Level={obs['water_level_m']}m (Danger={obs['danger_level_m']}m)")
    print(f"     * Satellite: Cloud Cover={obs['satellite_cloud_cover_pct']}% | SAR Backscatter={obs['sar_backscatter_db']} dB | NDWI={obs['ndwi_index']}")

    # 2. Initialize Agents Across All Layers
    MESSAGE_BUS.clear()
    weather_agent = WeatherAgent()
    flood_agent = FloodAgent()
    terrain_agent = TerrainAgent()
    satellite_agent = SatelliteAgent()
    fusion_agent = RiskAssessmentFusionAgent()
    decision_agent = DecisionEarlyWarningAgent()

    # 3. Layer 3: 4 Specialist Agents Deliberation
    print("\n--- [LAYER 3: 4 SPECIALIST AI AGENTS DELIBERATION] ---")
    w_packet = weather_agent.run_agent_cycle(obs, MESSAGE_BUS)
    t_packet = terrain_agent.run_agent_cycle(obs, MESSAGE_BUS)
    f_packet = flood_agent.run_agent_cycle(obs, MESSAGE_BUS)
    s_packet = satellite_agent.run_agent_cycle(obs, MESSAGE_BUS)

    packets = [w_packet, f_packet, t_packet, s_packet]
    for p in packets:
        flags_str = ", ".join(p.critical_flags) if p.critical_flags else "None"
        print(f"  +-- [{p.agent_type} AGENT] ({p.operational_state})")
        print(f"  |   * Risk Score:     {p.risk_score:.3f} ({p.risk_level}) | Model Confidence: {int(p.confidence * 100)}%")
        print(f"  |   * Critical Flags: {flags_str}")
        print(f"  |   * Action Trigger: {p.action_trigger}")
        if p.active_intentions:
            print(f"  |   * Intention:      {p.active_intentions[0]}")
        print(f"  +-------------------------------------------------------------")

    # 4. Layer 4: Risk Assessment and Fusion Agent (LLM Engine Confirmation)
    print("\n--- [LAYER 4: RISK ASSESSMENT & FUSION AGENT (LLM ENGINE)] ---")
    fused_assessment = fusion_agent.fuse_and_assess(
        station_profile=stn_profile,
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

    # 5. Layer 5: Decision, Early Warning & Continuous Evacuation Re-Assessment
    print("\n--- [LAYER 5: DECISION & EARLY WARNING AGENT (DYNAMIC RE-ROUTING)] ---")
    decision_packet = decision_agent.process_decision_cycle(
        assessment=fused_assessment,
        station_profile=stn_profile
    )

    print(f"  * ALERT LEVEL:                 {decision_packet.alert_level_display}")
    print(f"  * SIREN COMMAND DIRECTIVE:     {decision_packet.siren_command}")
    print(f"\n  * PUBLIC BROADCAST SMS:\n    \"{decision_packet.public_broadcast_sms}\"")

    print("\n  * TOP RECOMMENDED TACTICAL ACTIONS:")
    for act in decision_packet.recommended_tactical_actions[:3]:
        print(f"    - [{act['priority']}] {act['action']} ({act['designated_agency']})")

    # Display ASCII Visual Map
    print(decision_packet.ascii_risk_map)

    # Clickable Paths
    html_url = "file:///" + decision_packet.html_risk_map_path.replace("\\", "/")
    md_url = "file:///" + decision_packet.incident_report_md_path.replace("\\", "/")
    json_url = "file:///" + decision_packet.incident_report_json_path.replace("\\", "/")

    print("\n" + "=" * 95)
    print("AUTONOMOUS DISASTER OUTPUT ARTIFACTS GENERATED:")
    print(f"  [1] Interactive Dynamic Evacuation Map: {html_url}")
    print(f"  [2] Human Approval Incident Action Plan: {md_url}")
    print(f"  [3] Machine-Readable JSON Telemetry:     {json_url}")
    print("=" * 95)

    return decision_packet


def interactive_cli():
    print("=" * 95)
    print("   AUTONOMOUS MULTI-AGENT FLOOD DISASTER EARLY WARNING & LIVE MONITORING SYSTEM")
    print("   100% Free Live Telemetry | Cognitive LLM Engine | Continuous Evacuation Re-Assessment")
    print("=" * 95)

    default_loc = "Guwahati"
    print("\nEnter any place, city, or district name (e.g. Guwahati, Barpeta, Silchar, Patna, Kochi):")
    try:
        user_input = input(f"Location [Default: {default_loc}]: ").strip()
    except EOFError:
        user_input = default_loc

    target_loc = user_input if user_input else default_loc

    print("\nSelect Operating Mode:")
    print("  [1] Live Real-Time Telemetry (Current weather & river flow right now)")
    print("  [2] Live Location + Monsoon Deluge Surge Stress (Simulates severe flood event to test emergency re-routing)")
    try:
        mode_choice = input("Choice [1 or 2, Default: 1]: ").strip()
    except EOFError:
        mode_choice = "1"

    surge_mode = "SURGE" if mode_choice == "2" else "LIVE"
    run_live_monitor(target_loc, surge_mode=surge_mode)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Autonomous Multi-Agent Flood Disaster Monitor - Evaluates live location telemetry via Open-Meteo"
    )
    parser.add_argument("location", nargs="?", help="Name of any city, district, or region to evaluate (e.g. 'Cuttack', 'Mumbai', 'Guwahati')")
    parser.add_argument("--surge", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--watch", "--moderate", dest="watch", action="store_true", help=argparse.SUPPRESS)

    args = parser.parse_args()

    if args.location:
        mode = "SURGE" if args.surge else ("WATCH" if args.watch else "LIVE")
        run_live_monitor(args.location, surge_mode=mode)
    else:
        interactive_cli()
