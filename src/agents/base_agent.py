"""
Autonomous AI Agent Architecture (BDI: Belief-Desire-Intention & Inter-Agent Communication Bus)
Autonomous Multi-Agent AI System for Disaster Prediction (Flood Focus)

Implements formal Multi-Agent AI specifications (Russell & Norvig, Wooldridge):
1. Autonomous Agency: Goal-directed behavior with explicit Desires and Intentions.
2. BDI Cognitive Engine: Maintains dynamic Beliefs (world state + peer messages).
3. Inter-Agent Communication Protocol (ACL): Agents exchange messages across a shared Blackboard bus.
4. Autonomous Policy Execution: Deliberates, negotiates, and takes actions independently.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import pandas as pd
import numpy as np
from pydantic import BaseModel, Field
import joblib

MODEL_DIR = Path(__file__).resolve().parent.parent / "models" / "saved_models"


class AgentMessage(BaseModel):
    """Standardized Agent Communication Language (ACL) message exchanged between AI agents."""
    message_id: str
    sender_agent: str
    recipient_agent: str  # specific agent id or "BROADCAST"
    performative: str     # INFORM, WARN, REQUEST, CONFIRM, EMERGENCY
    timestamp: str
    subject: str
    content: Dict[str, Any]


class AgentPredictionPacket(BaseModel):
    """Standardized autonomous packet passed from specialist agents to coordinator."""
    agent_id: str
    agent_type: str
    station_id: str
    station_name: str
    timestamp: str
    agent_goal: str
    operational_state: str
    risk_score: float = Field(..., ge=0.0, le=1.0)
    risk_level: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    critical_flags: List[str] = Field(default_factory=list)
    action_trigger: str
    active_intentions: List[str] = Field(default_factory=list)
    dispatched_messages_count: int = 0
    key_indicators: Dict[str, Any] = Field(default_factory=dict)
    ready_for_fusion: bool = True


class InterAgentMessageBus:
    """Blackboard communication bus enabling autonomous peer-to-peer agent messaging."""
    
    def __init__(self):
        self.message_history: List[AgentMessage] = []

    def broadcast(self, message: AgentMessage):
        self.message_history.append(message)

    def get_messages_for_agent(self, agent_type: str, timestamp: str) -> List[AgentMessage]:
        return [
            msg for msg in self.message_history
            if (msg.recipient_agent in [agent_type, "BROADCAST"])
            and msg.timestamp == timestamp
            and msg.sender_agent != agent_type
        ]

    def clear(self):
        self.message_history.clear()


# Global message bus singleton for inter-agent communication
MESSAGE_BUS = InterAgentMessageBus()


class BaseAutonomousAIAgent(ABC):
    """Abstract base class for Goal-Directed BDI Autonomous AI Agents."""

    def __init__(self, agent_id: str, agent_type: str, primary_goal: str):
        self.agent_id = agent_id
        self.agent_type = agent_type.upper()
        self.primary_goal = primary_goal
        
        # BDI Agent Cognitive State
        self.beliefs: Dict[str, Any] = {}
        self.desires: List[str] = []
        self.intentions: List[str] = []
        
        # Predictive Model
        self.ml_model = None
        self.ml_features = []
        self.ml_classes = []
        self._load_ml_model()

    def _load_ml_model(self):
        """Loads domain predictive model."""
        model_file = MODEL_DIR / f"{self.agent_type.lower()}_model.joblib"
        if model_file.exists():
            try:
                payload = joblib.load(model_file)
                self.ml_model = payload["model"]
                self.ml_features = payload["features"]
                self.ml_classes = payload["classes"]
            except Exception as e:
                self.ml_model = None
        else:
            self.ml_model = None

    def perceive(self, observation: Dict[str, Any], bus: InterAgentMessageBus) -> Dict[str, Any]:
        """Perception: Ingests environment telemetry AND listens to incoming peer messages."""
        sanitized = observation.copy()
        ts = str(sanitized.get("timestamp", ""))
        
        # Listen for peer agent alerts on the message bus
        incoming_messages = bus.get_messages_for_agent(self.agent_type, ts)
        
        # Update Beliefs with incoming messages
        self.beliefs["peer_alerts"] = [
            f"[{msg.sender_agent} -> {msg.performative}]: {msg.subject}"
            for msg in incoming_messages
        ]
        self.beliefs["incoming_messages"] = incoming_messages
        return sanitized

    def evaluate_predictive_model(self, obs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Cognitive reasoning component for evaluating statistical patterns."""
        if not self.ml_model or not self.ml_features:
            return None

        row = {}
        for feat in self.ml_features:
            val = obs.get(feat, 0.0)
            if isinstance(val, bool):
                val = int(val)
            row[feat] = float(val) if val is not None else 0.0

        X = pd.DataFrame([row])
        pred_label = self.ml_model.predict(X)[0]
        pred_proba = self.ml_model.predict_proba(X)[0]

        class_weights = {"LOW": 0.05, "MODERATE": 0.35, "HIGH": 0.65, "CRITICAL": 0.95}
        expected_score = sum(
            prob * class_weights.get(cls, 0.1)
            for cls, prob in zip(self.ml_classes, pred_proba)
        )

        return {
            "ml_predicted_level": pred_label,
            "ml_risk_score": float(expected_score),
            "ml_class_probabilities": dict(zip(self.ml_classes, [round(p, 4) for p in pred_proba]))
        }

    @abstractmethod
    def deliberate_bdi_cycle(
        self,
        obs: Dict[str, Any],
        ml_prediction: Optional[Dict[str, Any]],
        bus: InterAgentMessageBus
    ) -> Dict[str, Any]:
        """Goal-Directed BDI Deliberation: updates desires, commits to intentions, and sends messages."""
        pass

    def run_agent_cycle(self, raw_observation: Dict[str, Any], bus: InterAgentMessageBus = MESSAGE_BUS) -> AgentPredictionPacket:
        """Executes the complete Autonomous AI Agent cycle."""
        # 1. Perception (Sensors + Peer Communications)
        obs = self.perceive(raw_observation, bus)
        station_id = obs.get("station_id", "UNKNOWN")
        station_name = obs.get("station_name", "UNKNOWN")
        timestamp = str(obs.get("timestamp", ""))

        # 2. Cognitive Modeling
        ml_pred = self.evaluate_predictive_model(obs)

        # 3. Deliberation, Intention Formulation, and Action
        decision = self.deliberate_bdi_cycle(obs, ml_pred, bus)

        # 4. Return Output Packet
        return AgentPredictionPacket(
            agent_id=self.agent_id,
            agent_type=self.agent_type,
            station_id=station_id,
            station_name=station_name,
            timestamp=timestamp,
            agent_goal=self.primary_goal,
            operational_state=decision.get("operational_state", "ROUTINE_MONITORING"),
            risk_score=round(float(decision["risk_score"]), 3),
            risk_level=decision["risk_level"],
            confidence=round(float(decision.get("confidence", 0.95)), 2),
            critical_flags=decision.get("critical_flags", []),
            action_trigger=decision.get("action_trigger", "MAINTAIN_ROUTINE_MONITORING"),
            active_intentions=self.intentions,
            dispatched_messages_count=decision.get("dispatched_messages_count", 0),
            key_indicators=decision.get("key_indicators", {}),
            ready_for_fusion=True
        )
