"""
Layer 4: Risk Assessment and Fusion Agent
Autonomous Multi-Agent AI System for Disaster Prediction

Responsibilities:
- Ingests prediction packets from the 4 Specialist Agents (Weather, Flood, Terrain, Satellite).
- Ingests inter-agent communications exchanged over the Blackboard Message Bus.
- Computes multi-modal cross-validated composite risk score and fused sensor confidence.
- Executes LLM-powered Chain-of-Thought (CoT) reasoning to provide authoritative confirmation
  on whether a flood will occur, the probability %, estimated lead time, and vulnerable locations.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from src.llm.local_llm_engine import LocalLLMEngine
from .base_agent import AgentPredictionPacket, InterAgentMessageBus


class FusedRiskAssessmentPacket(BaseModel):
    """Standardized output packet from the Risk Assessment and Fusion Agent."""
    assessment_id: str
    station_id: str
    station_name: str
    district: str
    river_name: str
    timestamp: str
    
    # Mathematical / Physical Fusion
    composite_risk_score: float = Field(..., ge=0.0, le=1.0)
    composite_confidence: float = Field(..., ge=0.0, le=1.0)
    primary_hazard_driver: str
    hard_safety_override_triggered: bool = False
    
    # LLM Result Confirmation
    flood_occurrence_confirmed: bool
    flood_event_status: str
    flood_probability_pct: float
    overall_severity_tier: str
    estimated_lead_time: str
    identified_vulnerable_locations: List[str]
    headline_verdict: str
    chain_of_thought_reasoning: str
    
    # Specialist Agent Inputs Preserved for Full Provenance
    weather_risk: float
    flood_risk: float
    terrain_risk: float
    satellite_risk: float
    specialist_flags: List[str]
    inter_agent_messages_count: int


class RiskAssessmentFusionAgent:
    """
    Autonomous AI Agent that fuses multi-modal specialist outputs and uses
    an LLM reasoning engine to confirm flood occurrence and evaluate vulnerability.
    """

    def __init__(self, agent_id: str = "AUTONOMOUS_RISK_FUSION_AGENT"):
        self.agent_id = agent_id
        self.agent_type = "FUSION_RISK_ASSESSMENT"
        self.primary_goal = "SYNTHESIZE_MULTI_AGENT_PREDICTIONS_AND_CONFIRM_FLOOD_DISASTERS"
        self.llm_engine = LocalLLMEngine()

        # Domain weights derived from hydrological sensitivity analysis
        self.weights = {
            "flood": 0.35,     # Direct in-situ river gauge stage (ground truth)
            "weather": 0.30,   # Convective storm & rainfall accumulation (surge cause)
            "satellite": 0.20, # Spaceborne radar extent & surface water signature
            "terrain": 0.15    # Topographic runoff generation & soil permeability
        }

    def fuse_and_assess(
        self,
        station_profile: Dict[str, Any],
        weather_packet: AgentPredictionPacket,
        flood_packet: AgentPredictionPacket,
        terrain_packet: AgentPredictionPacket,
        satellite_packet: AgentPredictionPacket,
        bus: InterAgentMessageBus
    ) -> FusedRiskAssessmentPacket:
        """
        Executes the full fusion and assessment cycle:
        1. Numerical & Physics-grounded Fusion
        2. Cognitive LLM Multimodal Confirmation
        """
        stn_id = station_profile.get("station_id", flood_packet.station_id)
        stn_name = station_profile.get("station_name", flood_packet.station_name)
        district = station_profile.get("district", "Assam River Basin")
        river = station_profile.get("river_name", "Brahmaputra")
        ts = flood_packet.timestamp

        w_risk = weather_packet.risk_score
        f_risk = flood_packet.risk_score
        t_risk = terrain_packet.risk_score
        s_risk = satellite_packet.risk_score

        # -------------------------------------------------------------
        # 1. Mathematical Weighted Fusion
        # -------------------------------------------------------------
        raw_composite_risk = (
            self.weights["flood"] * f_risk +
            self.weights["weather"] * w_risk +
            self.weights["satellite"] * s_risk +
            self.weights["terrain"] * t_risk
        )

        # Fused Confidence: Weighted average of individual sensor certainty
        fused_confidence = (
            self.weights["flood"] * flood_packet.confidence +
            self.weights["weather"] * weather_packet.confidence +
            self.weights["satellite"] * satellite_packet.confidence +
            self.weights["terrain"] * terrain_packet.confidence
        )

        # -------------------------------------------------------------
        # 2. Deterministic Fail-Safe Safety Overrides
        # -------------------------------------------------------------
        hard_override = False
        primary_driver = "BALANCED_MULTI_MODAL"

        # Rule A: Physical river stage at or above danger level is an absolute breach
        if "RIVER_BREACHED_DANGER_LEVEL" in flood_packet.critical_flags:
            composite_risk = max(raw_composite_risk, 0.95)
            hard_override = True
            primary_driver = "PHYSICAL_RIVER_DANGER_BREACH"
        # Rule B: Extreme cloudburst with choked drainage network causes flash waterlogging
        elif "EXTREME_24H_ACCUMULATION" in weather_packet.critical_flags and "DRAINAGE_NETWORK_COLLAPSE" in flood_packet.critical_flags:
            composite_risk = max(raw_composite_risk, 0.90)
            hard_override = True
            primary_driver = "CLOUDBURST_PLUS_DRAINAGE_COLLAPSE"
        # Rule C: Warning level exceeded + SAR radar specular surface water expansion
        elif "RIVER_ABOVE_WARNING_LEVEL" in flood_packet.critical_flags and "EXTREME_SURFACE_WATER_EXPANSION" in satellite_packet.critical_flags:
            composite_risk = max(raw_composite_risk, 0.85)
            primary_driver = "RIVER_SURGE_VERIFIED_BY_RADAR"
        else:
            composite_risk = raw_composite_risk
            # Determine dominant contributing agent
            scores = {"FLOOD": f_risk, "WEATHER": w_risk, "SATELLITE": s_risk, "TERRAIN": t_risk}
            dominant = max(scores, key=scores.get)
            primary_driver = f"DOMINANT_{dominant}_ELEVATION" if scores[dominant] > 0.4 else "ROUTINE_BASELINE"

        # Gather all critical flags across agents
        all_flags = list(set(
            weather_packet.critical_flags +
            flood_packet.critical_flags +
            terrain_packet.critical_flags +
            satellite_packet.critical_flags
        ))

        # Retrieve relevant inter-agent messages
        scenario_messages = [
            msg.model_dump() for msg in bus.message_history
            if msg.timestamp == ts
        ]

        # -------------------------------------------------------------
        # 3. LLM Cognitive Synthesis & Accurate Flood Confirmation
        # -------------------------------------------------------------
        llm_assessment = self.llm_engine.reason_risk_assessment(
            station_profile=station_profile,
            weather_packet=weather_packet.model_dump(),
            flood_packet=flood_packet.model_dump(),
            terrain_packet=terrain_packet.model_dump(),
            satellite_packet=satellite_packet.model_dump(),
            composite_risk=composite_risk,
            composite_confidence=fused_confidence,
            inter_agent_messages=scenario_messages
        )

        return FusedRiskAssessmentPacket(
            assessment_id=f"ASSESS_{stn_id}_{ts.replace(' ', '_').replace(':', '-')}",
            station_id=stn_id,
            station_name=stn_name,
            district=district,
            river_name=river,
            timestamp=ts,
            composite_risk_score=round(composite_risk, 3),
            composite_confidence=round(fused_confidence, 2),
            primary_hazard_driver=primary_driver,
            hard_safety_override_triggered=hard_override,
            flood_occurrence_confirmed=llm_assessment["flood_occurrence_confirmed"],
            flood_event_status=llm_assessment["flood_event_status"],
            flood_probability_pct=llm_assessment["flood_probability_pct"],
            overall_severity_tier=llm_assessment["overall_severity_tier"],
            estimated_lead_time=llm_assessment["estimated_lead_time"],
            identified_vulnerable_locations=llm_assessment["identified_vulnerable_locations"],
            headline_verdict=llm_assessment["headline_verdict"],
            chain_of_thought_reasoning=llm_assessment["chain_of_thought_reasoning"],
            weather_risk=w_risk,
            flood_risk=f_risk,
            terrain_risk=t_risk,
            satellite_risk=s_risk,
            specialist_flags=all_flags,
            inter_agent_messages_count=len(scenario_messages)
        )
