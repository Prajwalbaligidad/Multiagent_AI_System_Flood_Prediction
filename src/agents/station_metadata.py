"""
Standardized Hydrological & Geomorphic Profiles for Assam Monitoring Stations
"""

STATION_PROFILES = {
    "Guwahati_AWRMI": {
        "station_id": "STN_001_GUW",
        "station_name": "Guwahati_AWRMI",
        "district": "Kamrup Metropolitan",
        "river_name": "Brahmaputra",
        "latitude": 26.1445,
        "longitude": 91.7362,
        "warning_level_m": 49.68,
        "danger_level_m": 50.50,
        "hfl_m": 51.46,
        "elevation_m": 55.0,
        "slope_deg": 2.5,
        "soil_type": "Silty Clay Loam",
        "infiltration_capacity_mmh": 8.5,
        "land_cover_class": "Urban / Built-up",
        "runoff_coefficient": 0.78,
        "topographic_wetness_index": 12.25
    },
    "Dhubri_Ghat": {
        "station_id": "STN_002_DHU",
        "station_name": "Dhubri_Ghat",
        "district": "Dhubri",
        "river_name": "Brahmaputra",
        "latitude": 26.0207,
        "longitude": 89.9740,
        "warning_level_m": 28.62,
        "danger_level_m": 29.84,
        "hfl_m": 30.52,
        "elevation_m": 28.0,
        "slope_deg": 0.6,
        "soil_type": "Alluvial Clay",
        "infiltration_capacity_mmh": 4.2,
        "land_cover_class": "Riverine Floodplain",
        "runoff_coefficient": 0.38,
        "topographic_wetness_index": 13.58
    },
    "Silchar_Barak": {
        "station_id": "STN_003_SIL",
        "station_name": "Silchar_Barak",
        "district": "Cachar",
        "river_name": "Barak",
        "latitude": 24.8333,
        "longitude": 92.7789,
        "warning_level_m": 19.83,
        "danger_level_m": 20.85,
        "hfl_m": 21.98,
        "elevation_m": 42.0,
        "slope_deg": 1.8,
        "soil_type": "Clayey Silt",
        "infiltration_capacity_mmh": 6.0,
        "land_cover_class": "Semi-Urban / Lowland",
        "runoff_coefficient": 0.60,
        "topographic_wetness_index": 12.74
    },
    "Udalguri_Dhansiri": {
        "station_id": "STN_004_UDA",
        "station_name": "Udalguri_Dhansiri",
        "district": "Udalguri",
        "river_name": "Dhansiri (North)",
        "latitude": 26.7452,
        "longitude": 92.0962,
        "warning_level_m": 68.50,
        "danger_level_m": 69.80,
        "hfl_m": 70.45,
        "elevation_m": 165.0,
        "slope_deg": 11.5,
        "soil_type": "Gravelly Sandy Loam",
        "infiltration_capacity_mmh": 22.0,
        "land_cover_class": "Foothills / Forest",
        "runoff_coefficient": 0.42,
        "topographic_wetness_index": 5.95
    },
    "Barpeta_Beki": {
        "station_id": "STN_005_BAR",
        "station_name": "Barpeta_Beki",
        "district": "Barpeta",
        "river_name": "Beki",
        "latitude": 26.3211,
        "longitude": 91.0064,
        "warning_level_m": 44.10,
        "danger_level_m": 45.10,
        "hfl_m": 45.89,
        "elevation_m": 35.0,
        "slope_deg": 0.8,
        "soil_type": "Alluvial Loam",
        "infiltration_capacity_mmh": 7.0,
        "land_cover_class": "Wetlands / Cropland",
        "runoff_coefficient": 0.32,
        "topographic_wetness_index": 13.44
    }
}

def get_station_profile(station_name: str) -> dict:
    if station_name in STATION_PROFILES:
        return STATION_PROFILES[station_name]
    for k, v in STATION_PROFILES.items():
        if v["station_id"] == station_name or k.lower() in station_name.lower():
            return v
    return STATION_PROFILES["Guwahati_AWRMI"]
