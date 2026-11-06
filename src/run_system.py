"""
Autonomous Multi-Agent Flood Prediction & Emergency Response System
End-to-End Autonomous Pipeline with BDI Architecture & LLM Decision Intelligence

Architecture Layers:
1. Multi-Source Ingestion (IMD Weather, CWC River, Sentinel-1 SAR, SRTM DEM, Historical)
2. Data Preprocessing Agent (IQR Clamping, Missing Imputation, Temporal Alignment)
3. 4 Specialist Autonomous AI Agents (Weather, Flood, Terrain, Satellite)
4. Central Blackboard Message Bus (Asynchronous Inter-Agent Pub/Sub)
5. Risk Assessment and Fusion Agent (Multi-Modal Cross-Validation + LLM Flood Confirmation)
6. Decision and Early Warning Agent (Spatial Risk Maps, Alerts, Tactical Actions, Human Reports)
"""

import json
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import pandas as pd

from src.preprocessing.data_processing_agent import DataProcessingAgent
from src.agents import (
    WeatherAgent,
    FloodAgent,
    TerrainAgent,
    SatelliteAgent,
    RiskAssessmentFusionAgent,
    DecisionEarlyWarningAgent,
    MESSAGE_BUS,
    get_station_profile
)

DATASET_DIR = BASE_DIR / "dataset"
PROCESSED_FILE = DATASET_DIR / "processed" / "aligned_flood_multimodal.csv"
OUTPUT_DIR = BASE_DIR / "analysis_output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def run_pipeline(station_filter=None, sample_indices=None):
    start_time = datetime.now()
    MESSAGE_BUS.clear()

    print("=" * 100)
    print("AUTONOMOUS MULTI-AGENT AI FLOOD PREDICTION & EMERGENCY RESPONSE SYSTEM")
    print("Layer 1-3: Data Ingestion & 4 Specialist AI Agents (Weather, Flood, Terrain, Satellite)")
    print("Layer 4:   Risk Assessment & Fusion Agent (LLM Multi-Modal Confirmation)")
    print("Layer 5:   Decision & Early Warning Agent (Spatial Risk Maps, Alerts, Actions, Human Approval)")
    print("=" * 100)

    # -------------------------------------------------------------
    # Step 1: Data Ingestion & Preprocessing
    # -------------------------------------------------------------
    if not PROCESSED_FILE.exists():
        print("\n[Step 1] Running Data Preprocessing Agent...")
        preprocessor = DataProcessingAgent()
        df = preprocessor.process()
    else:
        print(f"\n[Step 1] Loading aligned multimodal dataset: {PROCESSED_FILE.name}")
        df = pd.read_csv(PROCESSED_FILE)

    print(f"Total synchronized multi-modal records available: {len(df)}")

    # -------------------------------------------------------------
    # Step 2: Initialize Agents Across All Layers
    # -------------------------------------------------------------
    print("\n[Step 2] Initializing Autonomous AI Agents...")
    weather_agent = WeatherAgent()
    flood_agent = FloodAgent()
    terrain_agent = TerrainAgent()
    satellite_agent = SatelliteAgent()
    fusion_agent = RiskAssessmentFusionAgent()
    decision_agent = DecisionEarlyWarningAgent()

    specialists = [weather_agent, flood_agent, terrain_agent, satellite_agent]
    for ag in specialists:
        print(f"  - [{ag.agent_id}] Goal: {ag.primary_goal}")
    print(f"  - [{fusion_agent.agent_id}] Goal: {fusion_agent.primary_goal}")
    print(f"  - [{decision_agent.agent_id}] Goal: {decision_agent.primary_goal}")

    # -------------------------------------------------------------
    # Step 3: Evaluate Benchmark Lifecycle Scenarios
    # -------------------------------------------------------------
    if sample_indices is None:
        target_station = station_filter or "Guwahati_AWRMI"
        stn_df = df[df["station_name"] == target_station].reset_index(drop=True)

        if len(stn_df) >= 700:
            eval_indices = [0, 241, 264, 440]
            eval_rows = stn_df.iloc[eval_indices]
        else:
            eval_rows = stn_df.head(4)
    else:
        eval_rows = df.iloc[sample_indices]

    print(f"\n[Step 3] Executing End-to-End Decision Cycles across {len(eval_rows)} disaster scenarios...")

    all_fusion_payloads = []
    summary_table = []

    for idx, (_, row) in enumerate(eval_rows.iterrows()):
        obs = row.to_dict()
        ts = obs.get("timestamp")
        stn = obs.get("station_name")
        stn_profile = get_station_profile(stn)

        print("\n" + "#" * 100)
        print(f"DISASTER SCENARIO {idx+1}: Station: {stn} ({stn_profile['district']}) | Timestamp: {ts}")
        print(f"Telemetry: Rain={obs.get('hourly_rainfall_mm')} mm/h | River Level={obs.get('water_level_m')}m (Danger={obs.get('danger_level_m')}m) | NDWI={obs.get('ndwi_index')}")
        print("#" * 100)

        # 1. Specialist Agents: Sense-Reason-Decide-Act Cycles
        w_packet = weather_agent.run_agent_cycle(obs, MESSAGE_BUS)
        t_packet = terrain_agent.run_agent_cycle(obs, MESSAGE_BUS)
        f_packet = flood_agent.run_agent_cycle(obs, MESSAGE_BUS)
        s_packet = satellite_agent.run_agent_cycle(obs, MESSAGE_BUS)

        packets = [w_packet, f_packet, t_packet, s_packet]

        print("\n--- [LAYER 3: 4 SPECIALIST AI AGENTS] ---")
        for p in packets:
            flags_str = ", ".join(p.critical_flags) if p.critical_flags else "None"
            print(f"  +-- [{p.agent_type} AGENT] ({p.operational_state})")
            print(f"  |   * risk_score:     {p.risk_score:.3f} ({p.risk_level}) | confidence: {int(p.confidence * 100)}%")
            print(f"  |   * critical_flags: {flags_str}")
            print(f"  |   * action_trigger: {p.action_trigger}")
            if p.active_intentions:
                print(f"  |   * intentions:     {', '.join(p.active_intentions[:2])}")
            print(f"  +-------------------------------------------------------------")

        # Display inter-agent messages dispatched on Blackboard
        scenario_messages = [msg for msg in MESSAGE_BUS.message_history if msg.timestamp == ts]
        if scenario_messages:
            print("\n  >> INTER-AGENT MESSAGES EXCHANGED ON BLACKBOARD BUS:")
            for msg in scenario_messages:
                print(f"     * [{msg.sender_agent} -> {msg.recipient_agent}] {msg.performative}: {msg.subject}")

        # 2. Layer 4: Risk Assessment and Fusion Agent (Multi-Modal + LLM Confirmation)
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

        # 3. Layer 5: Decision and Early Warning Agent (Maps, Alerts, Actions, Reports)
        print("\n--- [LAYER 5: DECISION & EARLY WARNING AGENT] ---")
        decision_packet = decision_agent.process_decision_cycle(
            assessment=fused_assessment,
            station_profile=stn_profile
        )

        print(f"  * ALERT DISPATCH:              {decision_packet.alert_level_display}")
        print(f"  * SIREN COMMAND:               {decision_packet.siren_command}")
        print(f"  * PUBLIC BROADCAST SMS:        \"{decision_packet.public_broadcast_sms}\"")
        print("\n  * TOP RECOMMENDED TACTICAL ACTIONS:")
        for act in decision_packet.recommended_tactical_actions[:3]:
            print(f"    - [{act['priority']}] {act['action']} ({act['designated_agency']})")

        print("\n  * SPATIAL RISK MAP VISUALIZATION:")
        print(decision_packet.ascii_risk_map)

        print(f"\n  * ARTIFACTS GENERATED FOR INCIDENT COMMAND:")
        print(f"    - Interactive HTML Risk Map: file:///{decision_packet.html_risk_map_path.replace('\\', '/')}")
        print(f"    - Human Approval Report (MD): file:///{decision_packet.incident_report_md_path.replace('\\', '/')}")
        print(f"    - Machine-Readable Plan (JSON): file:///{decision_packet.incident_report_json_path.replace('\\', '/')}")

        # Accumulate output records
        summary_table.append({
            "scenario": idx + 1,
            "timestamp": ts,
            "station_name": stn,
            "district": stn_profile["district"],
            "composite_risk": fused_assessment.composite_risk_score,
            "flood_confirmed": fused_assessment.flood_occurrence_confirmed,
            "flood_status": fused_assessment.flood_event_status,
            "severity_tier": fused_assessment.overall_severity_tier,
            "lead_time": fused_assessment.estimated_lead_time,
            "alert_code": decision_packet.alert_code,
            "vulnerable_locations": "; ".join(fused_assessment.identified_vulnerable_locations)
        })

        all_fusion_payloads.append({
            "scenario": idx + 1,
            "timestamp": ts,
            "station": stn,
            "specialist_packets": {
                "weather": w_packet.model_dump(),
                "flood": f_packet.model_dump(),
                "terrain": t_packet.model_dump(),
                "satellite": s_packet.model_dump()
            },
            "fused_risk_assessment": fused_assessment.model_dump(),
            "decision_early_warning": decision_packet.model_dump()
        })

    # Save comprehensive outputs
    json_path = OUTPUT_DIR / "autonomous_system_master_output.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_fusion_payloads, f, indent=2)

    csv_path = OUTPUT_DIR / "autonomous_system_master_summary.csv"
    df_summary = pd.DataFrame(summary_table)
    df_summary.to_csv(csv_path, index=False)

    print("\n" + "=" * 100)
    print("CONSOLIDATED AUTONOMOUS DISASTER DECISION TABLE")
    print("=" * 100)
    cols_to_show = ["scenario", "station_name", "composite_risk", "flood_confirmed", "severity_tier", "alert_code"]
    print(df_summary[cols_to_show].to_string(index=False))

    elapsed_ms = (datetime.now() - start_time).total_seconds() * 1000

    print("\n" + "=" * 100)
    print(f"AUTONOMOUS MULTI-AGENT FLOOD EARLY WARNING SYSTEM COMPLETE ({elapsed_ms:.1f} ms)")
    print(f"Master Output JSON: {json_path}")
    print(f"Executive CSV:     {csv_path}")
    print("=" * 100)

    return all_fusion_payloads


if __name__ == "__main__":
    if "--interactive" in sys.argv or "-i" in sys.argv:
        from src.interactive_demo import run_interactive_evaluator
        run_interactive_evaluator()
    else:
        run_pipeline()
