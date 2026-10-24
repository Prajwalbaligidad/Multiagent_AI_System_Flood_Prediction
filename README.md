# Autonomous Multi-Agent AI System for Flood Disaster Prediction (100% Local ML Engine)

A completely local, machine learning-driven multi-agent architecture for **Flood Disaster Prediction and Emergency Response**, operating with **zero LLM dependencies, zero external APIs, and zero internet connection required**.

```
                  ┌────────────────────────────────────────┐
                  │      Multi-Source Data Collection      │
                  │   Weather · Satellite · Rainfall ·     │
                  │   River Sensors · Terrain · History    │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │         Data Processing Agent          │
                  │   Cleans · Validates · Aligns ·        │
                  │             Combines                   │
                  └───────────────────┬────────────────────┘
                                      │
         ┌───────────────────┬────────┴──────────┬───────────────────┐
         ▼                   ▼                   ▼                   ▼
┌──────────────────┐ ┌───────────────┐ ┌───────────────────┐ ┌──────────────────┐
│  Weather Agent   │ │  Flood Agent  │ │   Terrain Agent   │ │ Satellite Agent  │
│  Random Forest   │ │ Random Forest │ │   Random Forest   │ │  Random Forest   │
│  Rainfall, Wind, │ │ River Levels, │ │ Slope, Soil, Land │ │ Clouds, NDWI,    │
│   Atm Pressure   │ │ Drainage, Log │ │       Cover       │ │  SAR Water Ext   │
└────────┬─────────┘ └───────┬───────┘ └─────────┬─────────┘ └────────┬─────────┘
         │                   │                   │                    │
         └───────────────────┴─────────┬─────────┴────────────────────┘
                                       ▼
                  ┌────────────────────────────────────────┐
                  │ Standardized Packets Ready for Fusion  │
                  │  (Risk Assessment & Fusion Agent Input)│
                  └────────────────────────────────────────┘
```

---

## 1. Project Directory Structure

```
flood_disaster_multiagent_system/
├── dataset/
│   ├── raw/
│   │   ├── weather_stations.csv            # Atmospheric parameters (pressure, temp, wind, gusts)
│   │   ├── rainfall_sensors.csv            # Hourly rainfall, cumulative 6h/24h, intensity category
│   │   ├── river_discharge_sensors.csv     # River levels, warning/danger levels, discharge, waterlogging
│   │   ├── satellite_imagery.csv           # Optical cloud cover, NDWI index, SAR backscatter, water extent
│   │   ├── terrain_parameters.csv          # Elevation, slope, soil permeability, land cover, runoff coeff
│   │   └── historical_flood_events.csv     # Historical peak flood levels, return periods, damages
│   └── processed/
│       ├── aligned_flood_multimodal.csv    # 3,600 spatiotemporally aligned multimodal records
│       └── preprocessing_report.json       # Data quality audit and validation report
├── src/
│   ├── models/
│   │   ├── train_ml_models.py              # Scikit-learn Random Forest training script
│   │   └── saved_models/                   # Exported specialist ML models (.joblib)
│   │       ├── weather_model.joblib
│   │       ├── flood_model.joblib
│   │       ├── terrain_model.joblib
│   │       └── satellite_model.joblib
│   ├── data_collection/
│   │   └── generate_multisource_data.py    # Multi-source data generator
│   ├── preprocessing/
│   │   └── data_processing_agent.py        # Cleans, validates, aligns, and fuses incoming streams
│   ├── agents/
│   │   ├── base_agent.py                   # Pydantic schema + ML inference engine
│   │   ├── weather_agent.py                # Meteorological hazard specialist
│   │   ├── flood_agent.py                  # Hydrological & river stage specialist
│   │   ├── terrain_agent.py                # Geomorphological & runoff susceptibility specialist
│   │   └── satellite_agent.py              # Remote sensing & SAR spaceborne verification specialist
│   └── run_system.py                       # Pipeline runner
└── analysis_output/
    ├── specialist_agents_output.json       # Standardized packets ready for Risk Assessment / Fusion
    └── specialist_agents_summary.csv       # Tabular summary of agent predictions and critical flags
```

---

## 2. Core Machine Learning Architecture

Each specialist agent is powered by a dedicated **Random Forest Classifier** (`scikit-learn`), trained on 3,600 aligned spatiotemporal multimodal observations:

1. **Weather ML Agent**: Evaluates rainfall intensity, 6h/24h cumulative rainfall, atmospheric pressure drops, and wind squalls.
2. **Flood ML Agent**: Evaluates river water levels relative to warning/danger marks, 1h/3h rise rates, discharge rate, street waterlogging depth, and drainage choke ratio.
3. **Terrain ML Agent**: Evaluates slope gradient, elevation, soil infiltration capacity, land cover imperviousness, Topographic Wetness Index (TWI), and effective runoff surge index.
4. **Satellite ML Agent**: Evaluates optical NDWI, cloud occlusion handling, surface water extent expansion %, and Sentinel-1 SAR C-band radar backscatter (dB).

---

## 3. Standardized Output Schema

Each specialist agent outputs a structured quantitative result packet:
```json
{
  "agent_id": "FLOOD_AGENT_01",
  "agent_type": "FLOOD",
  "station_id": "STN_001_GUW",
  "station_name": "Guwahati_AWRMI",
  "timestamp": "2024-07-03 08:00:00",
  "risk_score": 0.95,
  "risk_level": "CRITICAL",
  "confidence": 0.95,
  "critical_flags": [
    "RIVER_BREACHED_DANGER_LEVEL",
    "SEVERE_URBAN_WATERLOGGING",
    "DRAINAGE_NETWORK_COLLAPSE"
  ],
  "action_trigger": "TRIGGER_EMERGENCY_EVACUATION_BRAHMAPUTRA_BASIN",
  "key_indicators": {
    "river_name": "Brahmaputra",
    "water_level_m": 52.076,
    "warning_level_m": 49.68,
    "danger_level_m": 50.5,
    "danger_buffer_m": 1.576,
    "discharge_rate_cumecs": 37430.0,
    "waterlogging_depth_cm": 118.2,
    "drainage_choke_ratio": 1.0
  },
  "ready_for_fusion": true
}
```

---

## 4. How to Run

### Retrain ML Models (Optional)
```bash
python src/models/train_ml_models.py
```

### Run the Specialist Multi-Agent Pipeline
```bash
python src/run_system.py
```
This executes all 4 specialist agents locally and outputs:
- `analysis_output/specialist_agents_output.json`
- `analysis_output/specialist_agents_summary.csv`
