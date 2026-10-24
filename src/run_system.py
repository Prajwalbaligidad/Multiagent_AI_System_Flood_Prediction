"""
Autonomous Multi-Agent Flood Prediction System Runner
BDI Cognitive Architecture & Inter-Agent Blackboard Message Bus

Coordinates 4 Autonomous AI Agents:
1. Autonomous Weather AI Agent (Goal: Convective storm & cloudburst early detection)
2. Autonomous Flood AI Agent (Goal: Riverine hydraulic defense & levee breach mitigation)
3. Autonomous Terrain AI Agent (Goal: Runoff basin routing & soil saturation management)
4. Autonomous Satellite AI Agent (Goal: Spaceborne observability & radar cloud penetration)

Outputs standardized packets and inter-agent communication logs ready for the Fusion Agent.
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
    MESSAGE_BUS
)

DATASET_DIR = BASE_DIR / "dataset"
PROCESSED_FILE = DATASET_DIR / "processed" / "aligned_flood_multimodal.csv"
OUTPUT_DIR = BASE_DIR / "analysis_output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def run_pipeline(station_filter=None, sample_indices=None):
    start_time = datetime.now()
    MESSAGE_BUS.clear()

    print("=" * 95)
    print("AUTONOMOUS MULTI-AGENT AI FLOOD PREDICTION SYSTEM (BDI COGNITIVE ARCHITECTURE)")
    print("Multi-Source Ingestion -> Preprocessing -> 4 Autonomous AI Agents -> Inter-Agent Bus -> Fusion")
    print("=" * 95)

    # Step 1: Data Ingestion
    if not PROCESSED_FILE.exists():
        print("\n[Step 1] Running Data Preprocessing Agent...")
        preprocessor = DataProcessingAgent()
        df = preprocessor.process()
    else:
        print(f"\n[Step 1] Loading aligned multimodal dataset: {PROCESSED_FILE.name}")
        df = pd.read_csv(PROCESSED_FILE)

    print(f"Total synchronized multi-modal records available: {len(df)}")

    # Step 2: Initialize the 4 Autonomous AI Agents
    print("\n[Step 2] Initializing the 4 Autonomous AI Agents with BDI Agent Minds...")
    weather_agent = WeatherAgent()
    flood_agent = FloodAgent()
    terrain_agent = TerrainAgent()
    satellite_agent = SatelliteAgent()

    agents = [weather_agent, flood_agent, terrain_agent, satellite_agent]
    for ag in agents:
        print(f"  - [{ag.agent_id}] Goal: {ag.primary_goal}")

    # Step 3: Evaluate temporal scenarios representing the 4 hazard tiers:
    # 1. Normal Baseline (LOW ~0.05)
    # 2. Early Warning Buildup (MODERATE ~0.30)
    # 3. High Pre-Disaster Surge (HIGH ~0.60)
    # 4. Catastrophic Peak Flood (CRITICAL ~0.95)
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

    print(f"\n[Step 3] Executing Autonomous Agent Decision Cycles across {len(eval_rows)} scenarios...")

    all_fusion_payloads = []
    summary_table = []

    for idx, (_, row) in enumerate(eval_rows.iterrows()):
        obs = row.to_dict()
        ts = obs.get("timestamp")
        stn = obs.get("station_name")

        print("\n" + "-" * 95)
        print(f"SCENARIO {idx+1}: Station: {stn} | Timestamp: {ts}")
        print(f"Telemetry: Rain={obs.get('hourly_rainfall_mm')} mm/h | River Level={obs.get('water_level_m')} m (Danger={obs.get('danger_level_m')} m) | NDWI={obs.get('ndwi_index')}")
        print("-" * 95)

        # Autonomous Agent Sense-Reason-Decide-Act Cycles
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

            summary_table.append({
                "scenario": idx + 1,
                "timestamp": ts,
                "station_id": p.station_id,
                "station_name": p.station_name,
                "agent_type": p.agent_type,
                "primary_goal": p.agent_goal,
                "operational_state": p.operational_state,
                "risk_score": p.risk_score,
                "risk_level": p.risk_level,
                "confidence": p.confidence,
                "action_trigger": p.action_trigger,
                "active_intentions": "; ".join(p.active_intentions),
                "critical_flags": "; ".join(p.critical_flags)
            })

        # Display inter-agent messages dispatched during this scenario
        scenario_messages = [msg for msg in MESSAGE_BUS.message_history if msg.timestamp == ts]
        if scenario_messages:
            print("\n  >> INTER-AGENT MESSAGES EXCHANGED ON BLACKBOARD BUS:")
            for msg in scenario_messages:
                print(f"     * [{msg.sender_agent} -> {msg.recipient_agent}] {msg.performative}: {msg.subject}")

        # Multi-Agent Coordination Packet ready for Risk Assessment and Fusion Agent
        fusion_payload = {
            "fusion_metadata": {
                "generated_at": datetime.now().isoformat(),
                "station_id": obs.get("station_id"),
                "station_name": stn,
                "timestamp": ts,
                "inter_agent_messages_exchanged": len(scenario_messages),
                "ready_for_risk_assessment_agent": True
            },
            "autonomous_agent_packets": {
                "weather": w_packet.model_dump(),
                "flood": f_packet.model_dump(),
                "terrain": t_packet.model_dump(),
                "satellite": s_packet.model_dump()
            }
        }
        all_fusion_payloads.append(fusion_payload)

    # Save outputs
    json_path = OUTPUT_DIR / "specialist_agents_output.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_fusion_payloads, f, indent=2)

    csv_path = OUTPUT_DIR / "specialist_agents_summary.csv"
    df_summary = pd.DataFrame(summary_table)
    df_summary.to_csv(csv_path, index=False)

    print("\n" + "=" * 95)
    print("CONSOLIDATED AUTONOMOUS AGENT DECISION TABLE")
    print("=" * 95)
    cols_to_show = ["scenario", "agent_type", "risk_score", "confidence", "action_trigger", "critical_flags"]
    print(df_summary[cols_to_show].to_string(index=False))

    elapsed_ms = (datetime.now() - start_time).total_seconds() * 1000

    print("\n" + "=" * 95)
    print(f"AUTONOMOUS MULTI-AGENT SYSTEM EXECUTION COMPLETE ({elapsed_ms:.1f} ms)")
    print(f"Total Inter-Agent Messages Exchanged: {len(MESSAGE_BUS.message_history)}")
    print(f"Coordinator Fusion JSON: {json_path}")
    print(f"Summary Results CSV:     {csv_path}")
    print("=" * 95)

    return all_fusion_payloads


if __name__ == "__main__":
    if "--interactive" in sys.argv or "-i" in sys.argv:
        from src.interactive_demo import run_interactive_evaluator
        run_interactive_evaluator()
    else:
        run_pipeline()
