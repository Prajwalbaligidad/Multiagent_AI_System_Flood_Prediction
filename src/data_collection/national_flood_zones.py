"""
National High-Risk Flood Zones & Safe Sanctuaries Catalog
Autonomous Multi-Agent AI System for Disaster Prediction

Comprehensive registry of India's most critical flood-prone districts,
river basins (Brahmaputra, Ganga, Kosi, Mahanadi, Netravati, Periyar, Krishna, Tapi, Jhelum),
and their verified ground-truth safe sports stadium refuges.
"""

from typing import Dict, Any, List, Optional


NATIONAL_FLOOD_ZONES: Dict[str, Dict[str, Any]] = {
    # -------------------------------------------------------------
    # 1. ASSAM & NORTH-EAST (Brahmaputra & Barak Basins)
    # -------------------------------------------------------------
    "guwahati": {
        "city": "Guwahati",
        "district": "Kamrup Metropolitan",
        "state": "Assam",
        "river": "Brahmaputra",
        "hazard_trigger": "Brahmaputra River Inundation & Severe Urban Drainage Waterlogging",
        "latitude": 26.1445,
        "longitude": 91.7362,
        "elevation_m": 55.0,
        "stadium_name": "Indira Gandhi Athletic Stadium & Sarusajai Complex",
        "stadium_lat": 26.1112,
        "stadium_lon": 91.7654,
        "stadium_elev_m": 68.0,
        "capacity": 35000,
        "tier": "Tier-1 Elevated Highland Sports Complex"
    },
    "barpeta": {
        "city": "Barpeta",
        "district": "Barpeta",
        "state": "Assam",
        "river": "Beki & Manas",
        "hazard_trigger": "River Beki Floodplain Breach & Embankment Collapse",
        "latitude": 26.3211,
        "longitude": 91.0064,
        "elevation_m": 35.0,
        "stadium_name": "Barpeta District Sports Association Stadium",
        "stadium_lat": 26.3195,
        "stadium_lon": 91.0082,
        "stadium_elev_m": 42.0,
        "capacity": 12000,
        "tier": "Tier-1 Elevated Community Stadium Refuge"
    },
    "silchar": {
        "city": "Silchar",
        "district": "Cachar",
        "state": "Assam",
        "river": "Barak",
        "hazard_trigger": "Barak River Sluice Gate Overtopping & Bethukandi Dyke Inundation",
        "latitude": 24.8333,
        "longitude": 92.7789,
        "elevation_m": 42.0,
        "stadium_name": "Satindra Mohan Dev Stadium & District Sports Complex",
        "stadium_lat": 24.8251,
        "stadium_lon": 92.7985,
        "stadium_elev_m": 49.0,
        "capacity": 15000,
        "tier": "Tier-1 Highland Relief Sanctuary"
    },
    "dhubri": {
        "city": "Dhubri",
        "district": "Dhubri",
        "state": "Assam",
        "river": "Brahmaputra",
        "hazard_trigger": "Downstream Brahmaputra Delta Floods & River Island (Char) Submergence",
        "latitude": 26.0207,
        "longitude": 89.9740,
        "elevation_m": 28.0,
        "stadium_name": "Raja P.C. Barua Stadium & High Grounds",
        "stadium_lat": 26.0245,
        "stadium_lon": 89.9810,
        "stadium_elev_m": 34.0,
        "capacity": 10000,
        "tier": "Tier-1 Reinforced Plinth Stadium Sanctuary"
    },
    "dibrugarh": {
        "city": "Dibrugarh",
        "district": "Dibrugarh",
        "state": "Assam",
        "river": "Brahmaputra",
        "hazard_trigger": "Upstream Brahmaputra Surge & Severe Riverbank Erosion",
        "latitude": 27.4728,
        "longitude": 94.9120,
        "elevation_m": 108.0,
        "stadium_name": "Chowkidinghee Sports Field & District Complex",
        "stadium_lat": 27.4810,
        "stadium_lon": 94.9215,
        "stadium_elev_m": 114.0,
        "capacity": 18000,
        "tier": "Tier-1 High-Elevation Sports Sanctuary"
    },
    "kaziranga": {
        "city": "Kaziranga",
        "district": "Golaghat",
        "state": "Assam",
        "river": "Brahmaputra & Dhansiri",
        "hazard_trigger": "National Park Wildlife Lowland Inundation & Highway Submergence",
        "latitude": 26.5775,
        "longitude": 93.1711,
        "elevation_m": 72.0,
        "stadium_name": "Bokakhat Higher Secondary Sports Ground & Karbi Foothills Refuge",
        "stadium_lat": 26.6210,
        "stadium_lon": 93.5912,
        "stadium_elev_m": 95.0,
        "capacity": 8000,
        "tier": "Tier-1 Highland Foothills Sanctuary"
    },

    # -------------------------------------------------------------
    # 2. BIHAR (Ganga, Kosi, Gandak & Bagmati Basins)
    # -------------------------------------------------------------
    "patna": {
        "city": "Patna",
        "district": "Patna",
        "state": "Bihar",
        "river": "Ganga & Son",
        "hazard_trigger": "Ganga River Backflow & Severe Lowland Urban Drainage Collapse",
        "latitude": 25.5941,
        "longitude": 85.1356,
        "elevation_m": 53.0,
        "stadium_name": "Moin-ul-Haq Stadium & Sports Complex",
        "stadium_lat": 25.5948,
        "stadium_lon": 85.1535,
        "stadium_elev_m": 55.0,
        "capacity": 25000,
        "tier": "Tier-1 Reinforced Concrete Grandstand Safe Refuge"
    },
    "muzaffarpur": {
        "city": "Muzaffarpur",
        "district": "Muzaffarpur",
        "state": "Bihar",
        "river": "Burhi Gandak & Bagmati",
        "hazard_trigger": "Burhi Gandak Embankment Breaches & Riverbank Inundation",
        "latitude": 26.1209,
        "longitude": 85.3647,
        "elevation_m": 60.0,
        "stadium_name": "Khudi Ram Bose Memorial Stadium",
        "stadium_lat": 26.1185,
        "stadium_lon": 85.3812,
        "stadium_elev_m": 66.0,
        "capacity": 15000,
        "tier": "Tier-1 Elevated Plinth Stadium Sanctuary"
    },
    "bhagalpur": {
        "city": "Bhagalpur",
        "district": "Bhagalpur",
        "state": "Bihar",
        "river": "Ganga",
        "hazard_trigger": "Ganga River Channel Overflow & Diara Land Inundation",
        "latitude": 25.2425,
        "longitude": 86.9842,
        "elevation_m": 52.0,
        "stadium_name": "Sandy's Compound Sports Stadium",
        "stadium_lat": 25.2480,
        "stadium_lon": 86.9910,
        "stadium_elev_m": 58.0,
        "capacity": 20000,
        "tier": "Tier-1 Central Elevated Civic Stadium"
    },
    "darbhanga": {
        "city": "Darbhanga",
        "district": "Darbhanga",
        "state": "Bihar",
        "river": "Bagmati & Kamla",
        "hazard_trigger": "Kamla-Balan & Bagmati Flash Runoff Deluges",
        "latitude": 26.1542,
        "longitude": 85.8918,
        "elevation_m": 54.0,
        "stadium_name": "Nehru Stadium Darbhanga (Raj Ground)",
        "stadium_lat": 26.1510,
        "stadium_lon": 85.9020,
        "stadium_elev_m": 60.0,
        "capacity": 16000,
        "tier": "Tier-1 Royal Plinth Elevated Arena"
    },

    # -------------------------------------------------------------
    # 3. UTTAR PRADESH (Ganga, Yamuna, Rapti & Ghaghara Basins)
    # -------------------------------------------------------------
    "varanasi": {
        "city": "Varanasi",
        "district": "Varanasi",
        "state": "Uttar Pradesh",
        "river": "Ganga & Varuna",
        "hazard_trigger": "Varuna River Backflow & Ganga Ghat Submergence",
        "latitude": 25.3176,
        "longitude": 82.9739,
        "elevation_m": 80.0,
        "stadium_name": "Dr. Sampurnanand Stadium (Sigra Stadium)",
        "stadium_lat": 25.3210,
        "stadium_lon": 82.9850,
        "stadium_elev_m": 86.0,
        "capacity": 20000,
        "tier": "Tier-1 Elevated Inland Sports Arena"
    },
    "gorakhpur": {
        "city": "Gorakhpur",
        "district": "Gorakhpur",
        "state": "Uttar Pradesh",
        "river": "Rapti & Rohini",
        "hazard_trigger": "Rapti River Breach & Ring Bund Collapse",
        "latitude": 26.7606,
        "longitude": 83.3732,
        "elevation_m": 84.0,
        "stadium_name": "Regional Sports Stadium (Civil Lines)",
        "stadium_lat": 26.7580,
        "stadium_lon": 83.3850,
        "stadium_elev_m": 90.0,
        "capacity": 22000,
        "tier": "Tier-1 High-Elevation Civil Lines Sanctuary"
    },
    "prayagraj": {
        "city": "Prayagraj",
        "district": "Prayagraj",
        "state": "Uttar Pradesh",
        "river": "Ganga & Yamuna (Sangam)",
        "hazard_trigger": "Ganga-Yamuna Confluence Flood Surge & Lowland Submergence",
        "latitude": 25.4358,
        "longitude": 81.8463,
        "elevation_m": 98.0,
        "stadium_name": "Madan Mohan Malaviya Stadium",
        "stadium_lat": 25.4480,
        "stadium_lon": 81.8590,
        "stadium_elev_m": 105.0,
        "capacity": 25000,
        "tier": "Tier-1 Central High-Ground Sports Complex"
    },

    # -------------------------------------------------------------
    # 4. WEST BENGAL (Ganga, Hooghly, Damodar & Teesta Basins)
    # -------------------------------------------------------------
    "kolkata": {
        "city": "Kolkata",
        "district": "Kolkata",
        "state": "West Bengal",
        "river": "Hooghly (Ganga)",
        "hazard_trigger": "Tidal Bore Surges & Tropical Cyclone Cloudburst Deluges",
        "latitude": 22.5726,
        "longitude": 88.3639,
        "elevation_m": 9.0,
        "stadium_name": "Salt Lake Stadium (Vivekananda Yuba Bharati Krirangan)",
        "stadium_lat": 22.5697,
        "stadium_lon": 88.4069,
        "stadium_elev_m": 18.0,
        "capacity": 85000,
        "tier": "Tier-1 Reinforced Super-Stadium High-Ground Citadel"
    },
    "siliguri": {
        "city": "Siliguri",
        "district": "Darjeeling & Jalpaiguri",
        "state": "West Bengal",
        "river": "Mahananda & Teesta",
        "hazard_trigger": "Teesta River Flash Floods & Sub-Himalayan Torrential Runoff",
        "latitude": 26.7271,
        "longitude": 88.3953,
        "elevation_m": 122.0,
        "stadium_name": "Kanchenjunga Stadium",
        "stadium_lat": 26.7190,
        "stadium_lon": 88.4280,
        "stadium_elev_m": 130.0,
        "capacity": 30000,
        "tier": "Tier-1 Sub-Himalayan Elevated Arena"
    },

    # -------------------------------------------------------------
    # 5. ODISHA (Mahanadi, Kathajodi & Baitarani Delta)
    # -------------------------------------------------------------
    "cuttack": {
        "city": "Cuttack",
        "district": "Cuttack",
        "state": "Odisha",
        "river": "Mahanadi & Kathajodi",
        "hazard_trigger": "Mahanadi Hirakud Reservoir Discharge & Kathajodi Ring Road Overtopping",
        "latitude": 20.4625,
        "longitude": 85.8828,
        "elevation_m": 36.0,
        "stadium_name": "Barabati Stadium & Sports Complex",
        "stadium_lat": 20.4815,
        "stadium_lon": 85.8685,
        "stadium_elev_m": 42.0,
        "capacity": 45000,
        "tier": "Tier-1 Historic High-Plinth Stadium Citadel"
    },
    "bhubaneswar": {
        "city": "Bhubaneswar",
        "district": "Khurda",
        "state": "Odisha",
        "river": "Kuakhai & Daya",
        "hazard_trigger": "Daya River Delta Breach & Urban Flash Drainage Collapse",
        "latitude": 20.2961,
        "longitude": 85.8245,
        "elevation_m": 45.0,
        "stadium_name": "Kalinga Stadium & Multi-Sport Complex",
        "stadium_lat": 20.3015,
        "stadium_lon": 85.8235,
        "stadium_elev_m": 52.0,
        "capacity": 25000,
        "tier": "Tier-1 Modern Concrete Sports Haven"
    },

    # -------------------------------------------------------------
    # 6. KERALA (Periyar, Pamba, Bharathappuzha & Chaliyar)
    # -------------------------------------------------------------
    "kochi": {
        "city": "Kochi",
        "district": "Ernakulam",
        "state": "Kerala",
        "river": "Periyar",
        "hazard_trigger": "Idamalayar/Idukki Dam Spills & Periyar River Estuarine Deluges",
        "latitude": 9.9312,
        "longitude": 76.2673,
        "elevation_m": 5.0,
        "stadium_name": "Jawaharlal Nehru International Stadium (Kaloor)",
        "stadium_lat": 9.9982,
        "stadium_lon": 76.3001,
        "stadium_elev_m": 16.0,
        "capacity": 40000,
        "tier": "Tier-1 Elevated Coastal Relief Super-Stadium"
    },
    "wayanad": {
        "city": "Wayanad",
        "district": "Wayanad",
        "state": "Kerala",
        "river": "Kabini",
        "hazard_trigger": "Western Ghats Torrential Cloudbursts & Hillside Debris Flows",
        "latitude": 11.6854,
        "longitude": 76.1320,
        "elevation_m": 780.0,
        "stadium_name": "Krishnagiri Cricket Stadium & Highland Sanctuary",
        "stadium_lat": 11.6510,
        "stadium_lon": 76.2110,
        "stadium_elev_m": 820.0,
        "capacity": 15000,
        "tier": "Tier-1 Highland Plateau Mountain Citadel"
    },

    # -------------------------------------------------------------
    # 7. KARNATAKA (Netravati, Gurupura, Krishna & Malaprabha)
    # -------------------------------------------------------------
    "mangaluru": {
        "city": "Mangaluru",
        "district": "Dakshina Kannada",
        "state": "Karnataka",
        "river": "Netravati & Gurupura",
        "hazard_trigger": "Netravati River Coastal Surges & Estuarine Flooding",
        "latitude": 12.8698,
        "longitude": 74.8430,
        "elevation_m": 22.0,
        "stadium_name": "Mangala Stadium & Sports Complex (Ladyhill)",
        "stadium_lat": 12.8863,
        "stadium_lon": 74.8355,
        "stadium_elev_m": 28.0,
        "capacity": 25000,
        "tier": "Tier-1 Elevated Coastal Municipal Sports Sanctuary"
    },
    "belagavi": {
        "city": "Belagavi",
        "district": "Belagavi",
        "state": "Karnataka",
        "river": "Krishna, Malaprabha & Ghataprabha",
        "hazard_trigger": "Maharashtra Koyna/Almatti Dam Inflows & Krishna Basin Overflows",
        "latitude": 15.8497,
        "longitude": 74.4977,
        "elevation_m": 751.0,
        "stadium_name": "Subhash Ground & District Sports Stadium",
        "stadium_lat": 15.8610,
        "stadium_lon": 74.5120,
        "stadium_elev_m": 765.0,
        "capacity": 20000,
        "tier": "Tier-1 Plateau Highland Stadium Sanctuary"
    },

    # -------------------------------------------------------------
    # 8. GOA (Mandovi, Zuari & Sal Basins)
    # -------------------------------------------------------------
    "goa": {
        "city": "Goa",
        "district": "South Goa",
        "state": "Goa",
        "river": "Mandovi, Zuari & Sal",
        "hazard_trigger": "High-Tide Coastal Storm Surges & Mandovi Riverbank Floods",
        "latitude": 15.2993,
        "longitude": 74.0000,
        "elevation_m": 24.0,
        "stadium_name": "Fatorda Stadium (Jawaharlal Nehru Stadium, Margao)",
        "stadium_lat": 15.2912,
        "stadium_lon": 73.9744,
        "stadium_elev_m": 26.0,
        "capacity": 19000,
        "tier": "Tier-1 FIFA-Standard Elevated Stadium Safe Haven"
    },
    "panaji": {
        "city": "Panaji",
        "district": "North Goa",
        "state": "Goa",
        "river": "Mandovi River Estuary",
        "hazard_trigger": "Mandovi Tidal Backflow & Campal Lowland Submergence",
        "latitude": 15.4909,
        "longitude": 73.8278,
        "elevation_m": 7.0,
        "stadium_name": "Bambolim Athletic Stadium & Sports Complex",
        "stadium_lat": 15.4526,
        "stadium_lon": 73.8643,
        "stadium_elev_m": 45.0,
        "capacity": 15000,
        "tier": "Tier-1 Highland Athletics Stadium Sanctuary"
    },

    # -------------------------------------------------------------
    # 9. MAHARASHTRA (Mithi, Panchganga & Krishna Basins)
    # -------------------------------------------------------------
    "mumbai": {
        "city": "Mumbai",
        "district": "Mumbai City & Suburban",
        "state": "Maharashtra",
        "river": "Mithi & Coastal Arabian Sea",
        "hazard_trigger": "Extreme Cloudburst Deluges & High-Tide Coastal Outfall Choking",
        "latitude": 19.0760,
        "longitude": 72.8777,
        "elevation_m": 14.0,
        "stadium_name": "Wankhede / Brabourne Stadium & High Ground Arenas",
        "stadium_lat": 18.9389,
        "stadium_lon": 72.8258,
        "stadium_elev_m": 19.0,
        "capacity": 33000,
        "tier": "Tier-1 Reinforced Concrete Coastal Stadium Haven"
    },
    "kolhapur": {
        "city": "Kolhapur",
        "district": "Kolhapur",
        "state": "Maharashtra",
        "river": "Panchganga",
        "hazard_trigger": "Panchganga River Flood Stage Breach & Lowland Highway Cutoff",
        "latitude": 16.7050,
        "longitude": 74.2433,
        "elevation_m": 569.0,
        "stadium_name": "Chhatrapati Shahu Stadium",
        "stadium_lat": 16.6980,
        "stadium_lon": 74.2310,
        "stadium_elev_m": 578.0,
        "capacity": 18000,
        "tier": "Tier-1 Royal Plinth Historic Stadium Refuge"
    },
    "sangli": {
        "city": "Sangli",
        "district": "Sangli",
        "state": "Maharashtra",
        "river": "Krishna",
        "hazard_trigger": "Krishna River Extreme Discharge & Western Ghats Catchment Spills",
        "latitude": 16.8524,
        "longitude": 74.5815,
        "elevation_m": 549.0,
        "stadium_name": "Tarun Bharat Sports Stadium",
        "stadium_lat": 16.8610,
        "stadium_lon": 74.5720,
        "stadium_elev_m": 558.0,
        "capacity": 16000,
        "tier": "Tier-1 Highland Plateau Sports Complex"
    },

    # -------------------------------------------------------------
    # 10. GUJARAT (Tapi & Vishwamitri Basins)
    # -------------------------------------------------------------
    "surat": {
        "city": "Surat",
        "district": "Surat",
        "state": "Gujarat",
        "river": "Tapi",
        "hazard_trigger": "Ukai Dam Emergency Spillway Release & Tapi River Flooding",
        "latitude": 21.1702,
        "longitude": 72.8311,
        "elevation_m": 13.0,
        "stadium_name": "Lalbhai Contractor Cricket Stadium",
        "stadium_lat": 21.1510,
        "stadium_lon": 72.7810,
        "stadium_elev_m": 18.0,
        "capacity": 22000,
        "tier": "Tier-1 Reinforced Sports Stadium Refuge"
    },
    "vadodara": {
        "city": "Vadodara",
        "district": "Vadodara",
        "state": "Gujarat",
        "river": "Vishwamitri",
        "hazard_trigger": "Ajwa Dam Overflow & Vishwamitri River Urban Basin Breach",
        "latitude": 22.3072,
        "longitude": 73.1812,
        "elevation_m": 39.0,
        "stadium_name": "Kotambi International Sports Stadium",
        "stadium_lat": 22.3410,
        "stadium_lon": 73.3120,
        "stadium_elev_m": 48.0,
        "capacity": 25000,
        "tier": "Tier-1 Elevated Inland Arena Sanctuary"
    },

    # -------------------------------------------------------------
    # 11. JAMMU & KASHMIR (Jhelum Basin)
    # -------------------------------------------------------------
    "srinagar": {
        "city": "Srinagar",
        "district": "Srinagar",
        "state": "Jammu & Kashmir",
        "river": "Jhelum",
        "hazard_trigger": "Jhelum River Embankment Breach & Dal Lake Catchment Spill",
        "latitude": 34.0837,
        "longitude": 74.7973,
        "elevation_m": 1585.0,
        "stadium_name": "Bakshi Stadium & Sher-i-Kashmir Complex",
        "stadium_lat": 34.0680,
        "stadium_lon": 74.8050,
        "stadium_elev_m": 1594.0,
        "capacity": 30000,
        "tier": "Tier-1 Valley Highland Stadium Fortress"
    },

    # -------------------------------------------------------------
    # 12. ANDHRA PRADESH & TELANGANA (Godavari, Krishna & Musi)
    # -------------------------------------------------------------
    "vijayawada": {
        "city": "Vijayawada",
        "district": "NTR",
        "state": "Andhra Pradesh",
        "river": "Krishna (Prakasam Barrage)",
        "hazard_trigger": "Prakasam Barrage Extreme Discharge & Budameru Rivulet Flooding",
        "latitude": 16.5062,
        "longitude": 80.6480,
        "elevation_m": 11.0,
        "stadium_name": "Indira Gandhi Municipal Sports Stadium",
        "stadium_lat": 16.5010,
        "stadium_lon": 80.6410,
        "stadium_elev_m": 18.0,
        "capacity": 25000,
        "tier": "Tier-1 Elevated City Stadium Refuge"
    },
    "hyderabad": {
        "city": "Hyderabad",
        "district": "Hyderabad",
        "state": "Telangana",
        "river": "Musi",
        "hazard_trigger": "Himayat Sagar/Osman Sagar Lake Overflow & Musi River Inundation",
        "latitude": 17.3850,
        "longitude": 78.4867,
        "elevation_m": 505.0,
        "stadium_name": "G.M.C. Balayogi Athletic Stadium (Gachibowli)",
        "stadium_lat": 17.4430,
        "stadium_lon": 78.3490,
        "stadium_elev_m": 542.0,
        "capacity": 30000,
        "tier": "Tier-1 Elevated Highland Sports Citadel"
    },

    # -------------------------------------------------------------
    # 13. TAMIL NADU (Adyar, Cooum & Kosasthalaiyar)
    # -------------------------------------------------------------
    "chennai": {
        "city": "Chennai",
        "district": "Chennai",
        "state": "Tamil Nadu",
        "river": "Adyar, Cooum & Chembarambakkam Spills",
        "hazard_trigger": "Northeast Monsoon Cyclone Cloudbursts & Reservoir Releases",
        "latitude": 13.0827,
        "longitude": 80.2707,
        "elevation_m": 6.0,
        "stadium_name": "Jawaharlal Nehru Multi-Purpose Stadium (Periamet)",
        "stadium_lat": 13.0835,
        "stadium_lon": 80.2770,
        "stadium_elev_m": 14.0,
        "capacity": 40000,
        "tier": "Tier-1 Elevated High-Plinth Stadium Citadel"
    }
}


def get_all_flood_zones() -> Dict[str, Dict[str, Any]]:
    """Returns the full catalog of verified Indian flood hotspot zones."""
    return NATIONAL_FLOOD_ZONES


def search_flood_zone(query: str) -> Optional[Dict[str, Any]]:
    """Searches for a flood hotspot by city, district, river, or state name."""
    q = query.lower().strip()
    
    # Direct match
    if q in NATIONAL_FLOOD_ZONES:
        return NATIONAL_FLOOD_ZONES[q]
        
    # Substring match
    for key, data in NATIONAL_FLOOD_ZONES.items():
        if (
            q in key
            or q in data["city"].lower()
            or q in data["district"].lower()
            or q in data["state"].lower()
            or q in data["river"].lower()
        ):
            return data
            
    return None
