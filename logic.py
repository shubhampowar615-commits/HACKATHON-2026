import numpy as np
import random
from datetime import datetime, timedelta

# =====================================================================
# MUMBAI RAILWAY, METRO & MULTIMODAL NETWORK KNOWLEDGE BASE
# =====================================================================

CENTRAL_LINE = [
    "Kalyan", "Thakurli", "Dombivli", "Kopar", "Diva", "Mumbra", "Kalwa", "Thane", 
    "Mulund", "Nahur", "Bhandup", "Kanjurmarg", "Vikhroli", "Ghatkopar", "Vidyavihar", 
    "Kurla", "Sion", "Matunga (Central)", "Dadar (Central)", "Parel", "Currey Road", 
    "Chinchpokli", "Byculla", "Sandhurst Road", "Masjid Bunder", "CSMT"
]

WESTERN_LINE = [
    "Virar", "Vasai Road", "Bhayandar", "Mira Road", "Dahisar", "Borivali", "Kandivali", 
    "Malad", "Goregaon", "Ram Mandir", "Jogeshwari", "Andheri", "Vile Parle", "Santacruz", 
    "Khar Road", "Bandra", "Mahim", "Matunga Road", "Dadar (Western)", "Prabhadevi", 
    "Lower Parel", "Mahalaxmi", "Mumbai Central", "Grant Road", "Charni Road", "Marine Lines", "Churchgate"
]

HARBOUR_LINE = [
    "Panvel", "Kharghar", "Belapur CBD", "Seawoods Grand Central", "Nerul", "Juinagar", 
    "Sanpada", "Vashi", "Mankhurd", "Govandi", "Chembur", "Tilak Nagar", "Kurla", 
    "Chunabhatti", "GTB Nagar", "Vadala Road", "Sandhurst Road", "Masjid Bunder", "CSMT"
]

METRO_LINE_1 = [
    "Versova", "D.N. Nagar", "Azad Nagar", "Andheri", "Western Express Highway", 
    "Chakala", "Airport Road", "Marol Naka", "Saki Naka", "Asalpha", "Jagruti Nagar", "Ghatkopar"
]

CENTRAL_FAST_STOPS = {
    "Kalyan", "Dombivli", "Diva", "Thane", "Mulund", "Bhandup", "Ghatkopar", 
    "Kurla", "Dadar (Central)", "Byculla", "CSMT"
}

WESTERN_FAST_STOPS = {
    "Virar", "Vasai Road", "Bhayandar", "Borivali", "Andheri", "Bandra", 
    "Dadar (Western)", "Mumbai Central", "Grant Road", "Charni Road", "Marine Lines", "Churchgate"
}

CENTRAL_KM = {
    "kalyan": 54.0, "thakurli": 50.0, "dombivli": 48.0, "kopar": 46.5, "diva": 43.0, 
    "mumbra": 40.0, "kalwa": 36.0, "thane": 34.0, "mulund": 31.0, "nahur": 28.5, 
    "bhandup": 27.0, "kanjurmarg": 25.5, "vikhroli": 23.0, "ghatkopar": 21.0, 
    "vidyavihar": 18.0, "kurla": 15.0, "sion": 13.0, "matunga (central)": 11.0, "matunga": 11.0, 
    "dadar (central)": 9.0, "dadar": 9.0, "parel": 8.0, "currey road": 6.5, "chinchpokli": 5.5, 
    "byculla": 4.5, "sandhurst road": 3.0, "masjid bunder": 1.5, "csmt": 0.0, "csmt (cst)": 0.0, "cst": 0.0
}

WESTERN_KM = {
    "virar": 60.0, "vasai road": 52.0, "vasai": 52.0, "bhayandar": 44.0, "mira road": 40.0, 
    "dahisar": 37.0, "borivali": 34.0, "kandivali": 31.0, "malad": 29.0, "goregaon": 27.0, 
    "ram mandir": 25.0, "jogeshwari": 23.5, "andheri": 22.0, "vile parle": 19.5, "santacruz": 17.5, 
    "khar road": 16.0, "khar": 16.0, "bandra": 14.5, "mahim": 12.0, "matunga road": 10.5, 
    "dadar (western)": 9.0, "dadar": 9.0, "prabhadevi": 8.0, "lower parel": 7.0, "mahalaxmi": 5.5, 
    "mumbai central": 4.5, "grant road": 3.5, "charni road": 2.2, "marine lines": 1.4, 
    "marine drive": 1.4, "churchgate": 0.0
}

HARBOUR_KM = {
    "panvel": 49.0, "kharghar": 41.0, "belapur cbd": 38.0, "belapur": 38.0, 
    "seawoods grand central": 36.0, "seawoods": 36.0, "nerul": 34.0, "juinagar": 31.5, 
    "sanpada": 30.0, "vashi": 28.5, "mankhurd": 22.0, "govandi": 19.5, "chembur": 17.5, 
    "tilak nagar": 16.0, "kurla": 15.0, "chunabhatti": 13.5, "gtb nagar": 11.5, "vadala road": 9.0, 
    "sandhurst road": 3.0, "masjid bunder": 1.5, "masjid": 1.5, "csmt": 0.0, "csmt (cst)": 0.0
}

# ---------------------------------------------------------------------
# LOCATION RESOLVER & CLASSIFICATION
# ---------------------------------------------------------------------

def clean_station_name(name):
    return name.lower().replace(" (current location)", "").replace(" (central)", "").replace(" (western)", "").replace(" (cst)", "").strip()

def find_station(name, station_list):
    c = clean_station_name(name)
    for idx, s in enumerate(station_list):
        s_c = clean_station_name(s)
        if s_c == c or s.lower() == name.lower():
            return idx, s
    for idx, s in enumerate(station_list):
        s_c = clean_station_name(s)
        if s_c in c or c in s_c:
            return idx, s
    return -1, None

def check_hub(query):
    q = query.lower().strip()
    if "bkc" in q or "bandra kurla" in q:
        return {"type": "hub", "hub": "bkc", "name": "Bandra Kurla Complex (BKC)"}
    if "powai" in q or "hiranandani" in q:
        return {"type": "hub", "hub": "powai", "name": "Powai (Hiranandani)"}
    if "nariman" in q:
        return {"type": "hub", "hub": "nariman", "name": "Nariman Point"}
    if "colaba" in q or "gateway of india" in q:
        return {"type": "hub", "hub": "colaba", "name": "Colaba"}
    if "fort" in q or "flora fountain" in q:
        return {"type": "hub", "hub": "fort", "name": "Fort"}
    if "worli" in q:
        return {"type": "hub", "hub": "worli", "name": "Worli"}
    if "airport (t2)" in q or "t2" in q:
        return {"type": "hub", "hub": "airport_t2", "name": "CSMI Airport (T2)"}
    if "airport (t1)" in q or "t1" in q:
        return {"type": "hub", "hub": "airport_t1", "name": "Domestic Airport (T1)"}
    return None

def get_station_lines(name):
    results = []
    w_idx, w_s = find_station(name, WESTERN_LINE)
    if w_idx != -1: results.append({"type": "station", "line": "Western", "index": w_idx, "name": w_s})
    c_idx, c_s = find_station(name, CENTRAL_LINE)
    if c_idx != -1: results.append({"type": "station", "line": "Central", "index": c_idx, "name": c_s})
    h_idx, h_s = find_station(name, HARBOUR_LINE)
    if h_idx != -1: results.append({"type": "station", "line": "Harbour", "index": h_idx, "name": h_s})
    m_idx, m_s = find_station(name, METRO_LINE_1)
    if m_idx != -1: results.append({"type": "station", "line": "Metro1", "index": m_idx, "name": m_s})
    return results

def resolve_pair(origin, destination):
    h_orig = check_hub(origin)
    h_dest = check_hub(destination)
    
    if h_orig and h_dest:
        return h_orig, h_dest
    if h_orig:
        dest_lines = get_station_lines(destination)
        dest_choice = dest_lines[0] if dest_lines else {"type": "station", "line": "Western", "index": 0, "name": destination.title()}
        return h_orig, dest_choice
    if h_dest:
        orig_lines = get_station_lines(origin)
        orig_choice = orig_lines[0] if orig_lines else {"type": "station", "line": "Central", "index": 0, "name": origin.title()}
        return orig_choice, h_dest
        
    orig_lines = get_station_lines(origin)
    dest_lines = get_station_lines(destination)
    
    if not orig_lines:
        orig_lines = [{"type": "station", "line": "Central" if "kalyan" in origin.lower() or "thane" in origin.lower() else "Western", "index": 0, "name": origin.title()}]
    if not dest_lines:
        dest_lines = [{"type": "station", "line": "Western" if "marine" in destination.lower() or "churchgate" in destination.lower() else "Central", "index": 0, "name": destination.title()}]
        
    # Check for shared corridor (e.g. Panvel to CSMT on Harbour, or Kalyan to CSMT on Central)
    for o in orig_lines:
        for d in dest_lines:
            if o["line"] == d["line"]:
                return o, d
                
    return orig_lines[0], dest_lines[0]

def get_station_slice(line_stations, idx_from, idx_to, is_fast=False, fast_set=None):
    step = 1 if idx_from <= idx_to else -1
    all_stops = [line_stations[i] for i in range(idx_from, idx_to + step, step)]
    if not is_fast or not fast_set:
        return all_stops
    return [s for s in all_stops if s in fast_set or s == line_stations[idx_from] or s == line_stations[idx_to]]

# ---------------------------------------------------------------------
# UNIVERSAL MUMBAI ROUTE & TIMELINE GENERATOR
# ---------------------------------------------------------------------

def generate_mumbai_routes(origin, destination, distance_km=None):
    orig_loc, dest_loc = resolve_pair(origin, destination)
    now = datetime.now()
    dep_time = now + timedelta(minutes=4)
    
    norm_origin = orig_loc["name"]
    norm_dest = dest_loc["name"]

    # 1. SAME WESTERN LINE (e.g. Borivali to Churchgate / Marine Lines)
    if orig_loc["type"] == "station" and orig_loc["line"] == "Western" and dest_loc["type"] == "station" and dest_loc["line"] == "Western":
        idx1, idx2 = orig_loc["index"], dest_loc["index"]
        d1 = WESTERN_KM.get(clean_station_name(orig_loc["name"]), 20.0)
        d2 = WESTERN_KM.get(clean_station_name(dest_loc["name"]), 0.0)
        dist = round(float(distance_km), 1) if (distance_km and float(distance_km) > 0) else max(3.0, round(abs(d1 - d2), 1))
        
        is_south = idx1 < idx2
        headsign = "Churchgate" if is_south else ("Borivali" if idx2 <= 5 else "Virar")
        badge = f"🔵 {headsign} (F)" if dist > 18 else f"🔵 {headsign} (S)"
        fast_stops = get_station_slice(WESTERN_LINE, idx1, idx2, is_fast=(dist > 18), fast_set=WESTERN_FAST_STOPS)
        slow_stops = get_station_slice(WESTERN_LINE, idx1, idx2, is_fast=False)
        t_fast = max(12, int(dist * 1.35 + 4))
        t_slow = max(15, int(dist * 1.9 + 3))
        cost_2nd = 10 if dist <= 25 else 15
        cost_ac = 75 if dist <= 25 else 105
        
        return {
            "Fastest": {
                "mode_sequence": ["Western Line Fast Local" if dist > 18 else "Western Line Local", "Walking"],
                "time": t_fast, "cost": cost_2nd, "crowd": "High", "walking_distance": "180m", "transfers": 0, "waiting_time": 4, "dist": dist,
                "timeline": [
                    {
                        "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_origin} Station", "type": "board", "color": "blue", "badge": badge,
                        "train_info": f"90{random.randint(200, 800)}: Local towards {headsign}",
                        "meta": f"{t_fast - 3} min ({len(fast_stops)-1} stops) · Platform 2/3 · Stop ID: {norm_origin[:3].upper()}",
                        "stops": fast_stops[1:]
                    },
                    {
                        "time": (dep_time + timedelta(minutes=t_fast)).strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_dest} Station", "type": "arrive", "color": "emerald", "meta": "Arrive at destination (walk 180m)"
                    }
                ]
            },
            "Cheapest": {
                "mode_sequence": ["Western Line Local", "Walking"],
                "time": t_slow, "cost": cost_2nd, "crowd": "High", "walking_distance": "180m", "transfers": 0, "waiting_time": 5, "dist": dist,
                "timeline": [
                    {
                        "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_origin} Station", "type": "board", "color": "blue", "badge": f"🔵 {headsign} (S)",
                        "train_info": f"90{random.randint(100, 500)}: All Stops Local towards {headsign}",
                        "meta": f"{t_slow - 3} min ({len(slow_stops)-1} stops) · Platform 1/2 · Stop ID: {norm_origin[:3].upper()}",
                        "stops": slow_stops[1:]
                    },
                    {
                        "time": (dep_time + timedelta(minutes=t_slow)).strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_dest} Station", "type": "arrive", "color": "emerald", "meta": "Arrive at destination (walk 180m)"
                    }
                ]
            },
            "Reliable": {
                "mode_sequence": ["Western Line AC Fast Local", "Walking"],
                "time": t_fast, "cost": cost_ac, "crowd": "Low", "walking_distance": "180m", "transfers": 0, "waiting_time": 4, "dist": dist,
                "timeline": [
                    {
                        "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_origin} Station", "type": "board", "color": "blue", "badge": f"🔵 {headsign} (AC)",
                        "train_info": f"90{random.randint(600, 999)}: AC Fast Local towards {headsign}",
                        "meta": f"{t_fast - 3} min ({len(fast_stops)-1} stops) · AC Guaranteed Seating · Platform 3",
                        "stops": fast_stops[1:]
                    },
                    {
                        "time": (dep_time + timedelta(minutes=t_fast)).strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_dest} Station", "type": "arrive", "color": "emerald", "meta": "Arrive at destination (walk 180m)"
                    }
                ]
            }
        }

    # 2. SAME CENTRAL LINE (e.g. Kalyan to CSMT, or Thane to Dadar)
    if orig_loc["type"] == "station" and orig_loc["line"] == "Central" and dest_loc["type"] == "station" and dest_loc["line"] == "Central":
        idx1, idx2 = orig_loc["index"], dest_loc["index"]
        d1 = CENTRAL_KM.get(clean_station_name(orig_loc["name"]), 30.0)
        d2 = CENTRAL_KM.get(clean_station_name(dest_loc["name"]), 0.0)
        dist = round(float(distance_km), 1) if (distance_km and float(distance_km) > 0) else max(3.0, round(abs(d1 - d2), 1))
        
        is_south = idx1 < idx2
        headsign = "CSMT" if is_south else ("Thane" if idx2 <= 7 else "Kalyan")
        badge = f"🔴 {headsign} (F)" if dist > 18 else f"🔴 {headsign} (S)"
        fast_stops = get_station_slice(CENTRAL_LINE, idx1, idx2, is_fast=(dist > 18), fast_set=CENTRAL_FAST_STOPS)
        slow_stops = get_station_slice(CENTRAL_LINE, idx1, idx2, is_fast=False)
        t_fast = max(12, int(dist * 1.25 + 4))
        t_slow = max(15, int(dist * 1.8 + 3))
        cost_2nd = 10 if dist <= 25 else 15
        cost_ac = 85 if dist <= 25 else 125
        
        return {
            "Fastest": {
                "mode_sequence": ["Central Line Fast Local" if dist > 18 else "Central Line Local", "Walking"],
                "time": t_fast, "cost": cost_2nd, "crowd": "High", "walking_distance": "160m", "transfers": 0, "waiting_time": 4, "dist": dist,
                "timeline": [
                    {
                        "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_origin} Jn", "type": "board", "color": "red", "badge": badge,
                        "train_info": f"95{random.randint(200, 800)}: Fast Local towards {headsign}",
                        "meta": f"{t_fast - 3} min ({len(fast_stops)-1} stops) · Platform 4/5 · Stop ID: {norm_origin[:3].upper()}",
                        "stops": fast_stops[1:]
                    },
                    {
                        "time": (dep_time + timedelta(minutes=t_fast)).strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_dest} Terminus" if "csmt" in norm_dest.lower() else f"{norm_dest} Station", "type": "arrive", "color": "emerald", "meta": "Arrive at destination (walk 160m)"
                    }
                ]
            },
            "Cheapest": {
                "mode_sequence": ["Central Line Local", "Walking"],
                "time": t_slow, "cost": cost_2nd, "crowd": "High", "walking_distance": "160m", "transfers": 0, "waiting_time": 5, "dist": dist,
                "timeline": [
                    {
                        "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_origin} Station", "type": "board", "color": "red", "badge": f"🔴 {headsign} (S)",
                        "train_info": f"97{random.randint(100, 500)}: All Stops Slow towards {headsign}",
                        "meta": f"{t_slow - 3} min ({len(slow_stops)-1} stops) · Platform 1/2 · Stop ID: {norm_origin[:3].upper()}",
                        "stops": slow_stops[1:]
                    },
                    {
                        "time": (dep_time + timedelta(minutes=t_slow)).strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_dest} Station", "type": "arrive", "color": "emerald", "meta": "Arrive at destination (walk 160m)"
                    }
                ]
            },
            "Reliable": {
                "mode_sequence": ["Central Line AC Fast Local", "Walking"],
                "time": t_fast, "cost": cost_ac, "crowd": "Low", "walking_distance": "160m", "transfers": 0, "waiting_time": 4, "dist": dist,
                "timeline": [
                    {
                        "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_origin} Jn", "type": "board", "color": "red", "badge": f"🔴 {headsign} (AC)",
                        "train_info": f"95{random.randint(600, 999)}: AC Fast Local towards {headsign}",
                        "meta": f"{t_fast - 3} min ({len(fast_stops)-1} stops) · AC Guaranteed Seating · Platform 4",
                        "stops": fast_stops[1:]
                    },
                    {
                        "time": (dep_time + timedelta(minutes=t_fast)).strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_dest} Station", "type": "arrive", "color": "emerald", "meta": "Arrive at destination (walk 160m)"
                    }
                ]
            }
        }

    # 3. SAME HARBOUR LINE (e.g. Panvel to CSMT / Vashi)
    if orig_loc["type"] == "station" and orig_loc["line"] == "Harbour" and dest_loc["type"] == "station" and dest_loc["line"] == "Harbour":
        idx1, idx2 = orig_loc["index"], dest_loc["index"]
        d1 = HARBOUR_KM.get(clean_station_name(orig_loc["name"]), 30.0)
        d2 = HARBOUR_KM.get(clean_station_name(dest_loc["name"]), 0.0)
        dist = round(float(distance_km), 1) if (distance_km and float(distance_km) > 0) else max(3.0, round(abs(d1 - d2), 1))
        
        is_inbound = idx1 < idx2
        headsign = "CSMT" if is_inbound else ("Vashi" if idx2 <= 7 else "Panvel")
        all_stops = get_station_slice(HARBOUR_LINE, idx1, idx2, is_fast=False)
        t_harbour = max(15, int(dist * 1.8 + 4))
        cost_2nd = 10 if dist <= 25 else 15
        
        return {
            "Fastest": {
                "mode_sequence": ["Harbour Line Local", "Walking"],
                "time": t_harbour, "cost": cost_2nd, "crowd": "High", "walking_distance": "180m", "transfers": 0, "waiting_time": 4, "dist": dist,
                "timeline": [
                    {
                        "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_origin} Station", "type": "board", "color": "orange", "badge": f"🟠 {headsign} (H)",
                        "train_info": f"98{random.randint(100, 600)}: Harbour Local towards {headsign}",
                        "meta": f"{t_harbour - 3} min ({len(all_stops)-1} stops) · Platform 1/2",
                        "stops": all_stops[1:]
                    },
                    {
                        "time": (dep_time + timedelta(minutes=t_harbour)).strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_dest} Terminus" if "csmt" in norm_dest.lower() else f"{norm_dest} Station", "type": "arrive", "color": "emerald", "meta": "Arrive at destination (walk 180m)"
                    }
                ]
            },
            "Cheapest": {
                "mode_sequence": ["Harbour Line Local", "Walking"],
                "time": t_harbour, "cost": cost_2nd, "crowd": "High", "walking_distance": "180m", "transfers": 0, "waiting_time": 5, "dist": dist,
                "timeline": [
                    {
                        "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_origin} Station", "type": "board", "color": "orange", "badge": f"🟠 {headsign} (H)",
                        "train_info": f"98{random.randint(100, 600)}: Harbour Local towards {headsign}",
                        "meta": f"{t_harbour - 3} min ({len(all_stops)-1} stops) · Platform 1/2",
                        "stops": all_stops[1:]
                    },
                    {
                        "time": (dep_time + timedelta(minutes=t_harbour)).strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_dest} Station", "type": "arrive", "color": "emerald", "meta": "Arrive at destination (walk 180m)"
                    }
                ]
            },
            "Reliable": {
                "mode_sequence": ["Harbour Line Local", "Taxi"],
                "time": t_harbour - 2, "cost": cost_2nd + 35, "crowd": "Medium", "walking_distance": "100m", "transfers": 1, "waiting_time": 4, "dist": dist,
                "timeline": [
                    {
                        "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_origin} Station", "type": "board", "color": "orange", "badge": f"🟠 {headsign} (H)",
                        "train_info": f"98{random.randint(100, 600)}: Harbour Local towards {headsign}",
                        "meta": f"{t_harbour - 5} min ({len(all_stops)-1} stops) · Platform 1/2",
                        "stops": all_stops[1:]
                    },
                    {
                        "time": (dep_time + timedelta(minutes=t_harbour - 2)).strftime('%I:%M %p').lstrip('0'),
                        "station": norm_dest, "type": "arrive", "color": "emerald", "meta": "Arrive at destination"
                    }
                ]
            }
        }

    # 4. CENTRAL LINE to WESTERN LINE (e.g. Kalyan to Marine Lines or Borivali)
    if (orig_loc["type"] == "station" and orig_loc["line"] == "Central") and (dest_loc["type"] == "station" and dest_loc["line"] == "Western"):
        idx_c = orig_loc["index"]
        idx_w = dest_loc["index"]
        d1 = CENTRAL_KM.get(clean_station_name(orig_loc["name"]), 40.0)
        d2 = WESTERN_KM.get(clean_station_name(dest_loc["name"]), 15.0)
        dist = round(float(distance_km), 1) if (distance_km and float(distance_km) > 0) else round((d1 + d2) * 0.75, 1)
        
        dadar_c_idx = CENTRAL_LINE.index("Dadar (Central)")
        dadar_w_idx = WESTERN_LINE.index("Dadar (Western)")
        
        c_stops = get_station_slice(CENTRAL_LINE, idx_c, dadar_c_idx, is_fast=True, fast_set=CENTRAL_FAST_STOPS)
        w_stops = get_station_slice(WESTERN_LINE, dadar_w_idx, idx_w, is_fast=(abs(dadar_w_idx - idx_w) > 6), fast_set=WESTERN_FAST_STOPS)
        
        t1 = max(15, int(abs(d1 - 9.0) * 1.25 + 3))
        t2 = max(8, int(abs(d2 - 9.0) * 1.35 + 3))
        tot_time = t1 + 4 + t2
        
        w_dest_is_south = idx_w > dadar_w_idx
        w_headsign = "Churchgate" if w_dest_is_south else "Borivali"
        
        is_andheri = "andheri" in dest_loc["name"].lower()
        if is_andheri:
            ghat_idx = CENTRAL_LINE.index("Ghatkopar")
            c_to_ghat = get_station_slice(CENTRAL_LINE, idx_c, ghat_idx, is_fast=True, fast_set=CENTRAL_FAST_STOPS)
            t_ghat = max(10, int(abs(d1 - 21.0) * 1.25 + 3))
            tot_metro_time = t_ghat + 3 + 21
            return {
                "Fastest": {
                    "mode_sequence": ["Central Line Fast Local", "Metro Line 1", "Walking"],
                    "time": tot_metro_time, "cost": 45, "crowd": "High", "walking_distance": "150m", "transfers": 1, "waiting_time": 4, "dist": dist,
                    "timeline": [
                        {
                            "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                            "station": f"{norm_origin} Jn", "type": "board", "color": "red", "badge": "🔴 CSMT (F)",
                            "train_info": "95230: Fast Local towards CSMT",
                            "meta": f"{t_ghat} min ({len(c_to_ghat)-1} stops) · Platform 4/5 · Stop ID: {norm_origin[:3].upper()}",
                            "stops": c_to_ghat[1:]
                        },
                        {
                            "time": (dep_time + timedelta(minutes=t_ghat)).strftime('%I:%M %p').lstrip('0'),
                            "station": "Ghatkopar Interchange", "type": "transfer", "color": "slate",
                            "transfer_text": "Walk ~2 min across FOB directly into Metro Line 1 Concourse",
                            "meta": "Central Line to Metro 1 Interchange"
                        },
                        {
                            "time": (dep_time + timedelta(minutes=t_ghat + 3)).strftime('%I:%M %p').lstrip('0'),
                            "station": "Ghatkopar Metro Station", "type": "board", "color": "cyan", "badge": "🚇 Versova",
                            "train_info": "Metro Line 1 towards Versova (AC)",
                            "meta": "21 min (11 stops) · Platform 1 · High Frequency every 3 min",
                            "stops": ["Jagruti Nagar", "Asalpha", "Saki Naka", "Marol Naka", "Airport Road", "Chakala", "WEH", "Andheri Metro"]
                        },
                        {
                            "time": (dep_time + timedelta(minutes=tot_metro_time)).strftime('%I:%M %p').lstrip('0'),
                            "station": f"{norm_dest} Station", "type": "arrive", "color": "emerald", "meta": "Arrive at destination (walk 150m)"
                        }
                    ]
                },
                "Cheapest": {
                    "mode_sequence": ["Central Line Fast Local", "Western Line Local", "Walking"],
                    "time": tot_time, "cost": 20, "crowd": "High", "walking_distance": "350m", "transfers": 1, "waiting_time": 6, "dist": dist,
                    "timeline": [
                        {
                            "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                            "station": f"{norm_origin} Jn", "type": "board", "color": "red", "badge": "🔴 CSMT (F)",
                            "train_info": "95230: Fast Local towards CSMT",
                            "meta": f"{t1} min ({len(c_stops)-1} stops) · Platform 4/5",
                            "stops": c_stops[1:]
                        },
                        {
                            "time": (dep_time + timedelta(minutes=t1)).strftime('%I:%M %p').lstrip('0'),
                            "station": "Dadar Junction", "type": "transfer", "color": "slate",
                            "transfer_text": "Walk ~4 min across Foot Overbridge (Platform 4 ➔ Platform 1)",
                            "meta": "Central Line to Western Line Interchange"
                        },
                        {
                            "time": (dep_time + timedelta(minutes=t1 + 4)).strftime('%I:%M %p').lstrip('0'),
                            "station": "Dadar (Western)", "type": "board", "color": "blue", "badge": "🔵 Borivali (S)",
                            "train_info": "90412: Slow Local towards Borivali",
                            "meta": f"{t2} min ({len(w_stops)-1} stops) · Platform 1",
                            "stops": w_stops[1:]
                        },
                        {
                            "time": (dep_time + timedelta(minutes=tot_time)).strftime('%I:%M %p').lstrip('0'),
                            "station": f"{norm_dest} Station", "type": "arrive", "color": "emerald", "meta": "Arrive at destination (walk 150m)"
                        }
                    ]
                },
                "Reliable": {
                    "mode_sequence": ["Central Line AC Fast Local", "Metro Line 1", "Shared Auto"],
                    "time": tot_metro_time, "cost": 135, "crowd": "Low", "walking_distance": "100m", "transfers": 1, "waiting_time": 4, "dist": dist,
                    "timeline": [
                        {
                            "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                            "station": f"{norm_origin} Jn", "type": "board", "color": "red", "badge": "🔴 CSMT (AC)",
                            "train_info": "95230: AC Fast Local towards CSMT",
                            "meta": f"{t_ghat} min ({len(c_to_ghat)-1} stops) · AC Guaranteed Seating · Platform 4",
                            "stops": c_to_ghat[1:]
                        },
                        {
                            "time": (dep_time + timedelta(minutes=t_ghat)).strftime('%I:%M %p').lstrip('0'),
                            "station": "Ghatkopar Interchange", "type": "transfer", "color": "slate",
                            "transfer_text": "Walk ~2 min across FOB directly into Metro Line 1 Concourse",
                            "meta": "Central Line to Metro 1 Interchange"
                        },
                        {
                            "time": (dep_time + timedelta(minutes=t_ghat + 3)).strftime('%I:%M %p').lstrip('0'),
                            "station": "Ghatkopar Metro Station", "type": "board", "color": "cyan", "badge": "🚇 Versova",
                            "train_info": "Metro Line 1 towards Versova (AC)",
                            "meta": "21 min (11 stops) · Platform 1 · AC Metro Train",
                            "stops": ["Jagruti Nagar", "Asalpha", "Saki Naka", "Marol Naka", "Airport Road", "Chakala", "WEH", "Andheri Metro"]
                        },
                        {
                            "time": (dep_time + timedelta(minutes=tot_metro_time)).strftime('%I:%M %p').lstrip('0'),
                            "station": f"{norm_dest} Station", "type": "arrive", "color": "emerald", "meta": "Arrive at destination"
                        }
                    ]
                }
            }
        
        # General Central to Western via Dadar
        return {
            "Fastest": {
                "mode_sequence": ["Central Line Fast Local", "Western Line Local", "Walking"],
                "time": tot_time, "cost": 20, "crowd": "High", "walking_distance": "200m", "transfers": 1, "waiting_time": 5, "dist": dist,
                "timeline": [
                    {
                        "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_origin} Jn", "type": "board", "color": "red", "badge": "🔴 CSMT (F)",
                        "train_info": "95230: Fast Local towards CSMT",
                        "meta": f"{t1} min ({len(c_stops)-1} stops) · Platform 4/5 · Stop ID: {norm_origin[:3].upper()}",
                        "stops": c_stops[1:]
                    },
                    {
                        "time": (dep_time + timedelta(minutes=t1)).strftime('%I:%M %p').lstrip('0'),
                        "station": "Dadar Junction", "type": "transfer", "color": "slate",
                        "transfer_text": f"Walk ~4 min across Foot Overbridge (Platform 4 ➔ Platform {2 if w_dest_is_south else 1})",
                        "meta": "Central Line to Western Line Interchange"
                    },
                    {
                        "time": (dep_time + timedelta(minutes=t1 + 4)).strftime('%I:%M %p').lstrip('0'),
                        "station": "Dadar (Western)", "type": "board", "color": "blue", "badge": f"🔵 {w_headsign} (S)",
                        "train_info": f"90686: Local towards {w_headsign}",
                        "meta": f"{t2} min ({len(w_stops)-1} stops) · Platform {2 if w_dest_is_south else 1} · Stop ID: DDR",
                        "stops": w_stops[1:]
                    },
                    {
                        "time": (dep_time + timedelta(minutes=tot_time)).strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_dest} Station", "type": "arrive", "color": "emerald", "meta": "Arrive at destination (walk 200m)"
                    }
                ]
            },
            "Cheapest": {
                "mode_sequence": ["Central Line Fast Local", "Western Line Local", "Walking"],
                "time": tot_time + 8, "cost": 15, "crowd": "High", "walking_distance": "350m", "transfers": 1, "waiting_time": 7, "dist": dist,
                "timeline": [
                    {
                        "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_origin} Jn", "type": "board", "color": "red", "badge": "🔴 CSMT (F)",
                        "train_info": "95230: Fast Local towards CSMT",
                        "meta": f"{t1} min ({len(c_stops)-1} stops) · Platform 4/5",
                        "stops": c_stops[1:]
                    },
                    {
                        "time": (dep_time + timedelta(minutes=t1)).strftime('%I:%M %p').lstrip('0'),
                        "station": "Dadar Junction", "type": "transfer", "color": "slate",
                        "transfer_text": "Walk ~4 min across Foot Overbridge",
                        "meta": "Central Line to Western Line Interchange"
                    },
                    {
                        "time": (dep_time + timedelta(minutes=t1 + 4)).strftime('%I:%M %p').lstrip('0'),
                        "station": "Dadar (Western)", "type": "board", "color": "blue", "badge": f"🔵 {w_headsign} (S)",
                        "train_info": f"90412: Slow Local towards {w_headsign}",
                        "meta": f"{t2} min ({len(w_stops)-1} stops) · Platform 2",
                        "stops": w_stops[1:]
                    },
                    {
                        "time": (dep_time + timedelta(minutes=tot_time + 8)).strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_dest} Station", "type": "arrive", "color": "emerald", "meta": "Arrive at destination (walk 350m)"
                    }
                ]
            },
            "Reliable": {
                "mode_sequence": ["Central Line AC Fast Local", "Western Line Local", "Taxi"],
                "time": tot_time, "cost": 140, "crowd": "Low", "walking_distance": "120m", "transfers": 1, "waiting_time": 4, "dist": dist,
                "timeline": [
                    {
                        "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_origin} Jn", "type": "board", "color": "red", "badge": "🔴 CSMT (AC)",
                        "train_info": "95230: AC Fast Local towards CSMT",
                        "meta": f"{t1} min ({len(c_stops)-1} stops) · AC Guaranteed Seating · Platform 4",
                        "stops": c_stops[1:]
                    },
                    {
                        "time": (dep_time + timedelta(minutes=t1)).strftime('%I:%M %p').lstrip('0'),
                        "station": "Dadar Junction", "type": "transfer", "color": "slate",
                        "transfer_text": "Walk ~4 min across Foot Overbridge to Western Platform",
                        "meta": "Central Line to Western Line Interchange"
                    },
                    {
                        "time": (dep_time + timedelta(minutes=t1 + 4)).strftime('%I:%M %p').lstrip('0'),
                        "station": "Dadar (Western)", "type": "board", "color": "blue", "badge": f"🔵 {w_headsign} (S)",
                        "train_info": f"90686: Local towards {w_headsign}",
                        "meta": f"{t2} min ({len(w_stops)-1} stops) · Platform 2",
                        "stops": w_stops[1:]
                    },
                    {
                        "time": (dep_time + timedelta(minutes=tot_time)).strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_dest} Station", "type": "arrive", "color": "emerald", "meta": "Arrive at destination"
                    }
                ]
            }
        }

    # 5. WESTERN LINE to CENTRAL LINE (e.g. Borivali to Thane or CSMT)
    if (orig_loc["type"] == "station" and orig_loc["line"] == "Western") and (dest_loc["type"] == "station" and dest_loc["line"] == "Central"):
        idx_w = orig_loc["index"]
        idx_c = dest_loc["index"]
        d1 = WESTERN_KM.get(clean_station_name(orig_loc["name"]), 30.0)
        d2 = CENTRAL_KM.get(clean_station_name(dest_loc["name"]), 20.0)
        dist = round(float(distance_km), 1) if (distance_km and float(distance_km) > 0) else round((d1 + d2) * 0.75, 1)
        
        dadar_w_idx = WESTERN_LINE.index("Dadar (Western)")
        dadar_c_idx = CENTRAL_LINE.index("Dadar (Central)")
        
        w_stops = get_station_slice(WESTERN_LINE, idx_w, dadar_w_idx, is_fast=True, fast_set=WESTERN_FAST_STOPS)
        c_dest_is_north = idx_c < dadar_c_idx
        c_headsign = "Kalyan" if c_dest_is_north else "CSMT"
        c_stops = get_station_slice(CENTRAL_LINE, dadar_c_idx, idx_c, is_fast=True, fast_set=CENTRAL_FAST_STOPS)
        
        t1 = max(15, int(abs(d1 - 9.0) * 1.35 + 3))
        t2 = max(8, int(abs(d2 - 9.0) * 1.25 + 3))
        tot_time = t1 + 4 + t2
        
        return {
            "Fastest": {
                "mode_sequence": ["Western Line Fast Local", "Central Line Fast Local", "Walking"],
                "time": tot_time, "cost": 20, "crowd": "High", "walking_distance": "200m", "transfers": 1, "waiting_time": 5, "dist": dist,
                "timeline": [
                    {
                        "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_origin} Station", "type": "board", "color": "blue", "badge": "🔵 Churchgate (F)",
                        "train_info": "90686: Fast Local towards Churchgate",
                        "meta": f"{t1} min ({len(w_stops)-1} stops) · Platform 3 · Stop ID: {norm_origin[:3].upper()}",
                        "stops": w_stops[1:]
                    },
                    {
                        "time": (dep_time + timedelta(minutes=t1)).strftime('%I:%M %p').lstrip('0'),
                        "station": "Dadar Junction", "type": "transfer", "color": "slate",
                        "transfer_text": f"Walk ~4 min across Foot Overbridge (Platform 2 ➔ Platform {4 if c_dest_is_north else 5})",
                        "meta": "Western Line to Central Line Interchange"
                    },
                    {
                        "time": (dep_time + timedelta(minutes=t1 + 4)).strftime('%I:%M %p').lstrip('0'),
                        "station": "Dadar (Central)", "type": "board", "color": "red", "badge": f"🔴 {c_headsign} (F)",
                        "train_info": f"95230: Fast Local towards {c_headsign}",
                        "meta": f"{t2} min ({len(c_stops)-1} stops) · Platform {4 if c_dest_is_north else 5} · Stop ID: DDR",
                        "stops": c_stops[1:]
                    },
                    {
                        "time": (dep_time + timedelta(minutes=tot_time)).strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_dest} Station", "type": "arrive", "color": "emerald", "meta": "Arrive at destination (walk 200m)"
                    }
                ]
            },
            "Cheapest": {
                "mode_sequence": ["Western Line Local", "Central Line Local", "Walking"],
                "time": tot_time + 12, "cost": 15, "crowd": "High", "walking_distance": "350m", "transfers": 1, "waiting_time": 7, "dist": dist,
                "timeline": [
                    {
                        "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_origin} Station", "type": "board", "color": "blue", "badge": "🔵 Churchgate (S)",
                        "train_info": "90412: Slow Local towards Churchgate",
                        "meta": f"{t1 + 6} min · Platform 1", "stops": w_stops[1:]
                    },
                    {
                        "time": (dep_time + timedelta(minutes=t1 + 6)).strftime('%I:%M %p').lstrip('0'),
                        "station": "Dadar Junction", "type": "transfer", "color": "slate",
                        "transfer_text": "Walk ~4 min across Foot Overbridge",
                        "meta": "Western Line to Central Line Interchange"
                    },
                    {
                        "time": (dep_time + timedelta(minutes=t1 + 10)).strftime('%I:%M %p').lstrip('0'),
                        "station": "Dadar (Central)", "type": "board", "color": "red", "badge": f"🔴 {c_headsign} (S)",
                        "train_info": f"97042: All Stops Slow towards {c_headsign}",
                        "meta": f"{t2 + 6} min · Platform 1", "stops": c_stops[1:]
                    },
                    {
                        "time": (dep_time + timedelta(minutes=tot_time + 12)).strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_dest} Station", "type": "arrive", "color": "emerald", "meta": "Arrive at destination (walk 350m)"
                    }
                ]
            },
            "Reliable": {
                "mode_sequence": ["Western Line AC Fast Local", "Central Line Fast Local", "Shared Auto"],
                "time": tot_time, "cost": 145, "crowd": "Low", "walking_distance": "120m", "transfers": 1, "waiting_time": 4, "dist": dist,
                "timeline": [
                    {
                        "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_origin} Station", "type": "board", "color": "blue", "badge": "🔵 Churchgate (AC)",
                        "train_info": "90686: AC Fast Local towards Churchgate",
                        "meta": f"{t1} min ({len(w_stops)-1} stops) · AC Guaranteed Seating · Platform 3",
                        "stops": w_stops[1:]
                    },
                    {
                        "time": (dep_time + timedelta(minutes=t1)).strftime('%I:%M %p').lstrip('0'),
                        "station": "Dadar Junction", "type": "transfer", "color": "slate",
                        "transfer_text": "Walk ~4 min across Foot Overbridge",
                        "meta": "Western Line to Central Line Interchange"
                    },
                    {
                        "time": (dep_time + timedelta(minutes=t1 + 4)).strftime('%I:%M %p').lstrip('0'),
                        "station": "Dadar (Central)", "type": "board", "color": "red", "badge": f"🔴 {c_headsign} (F)",
                        "train_info": f"95230: Fast Local towards {c_headsign}",
                        "meta": f"{t2} min ({len(c_stops)-1} stops) · Platform 4",
                        "stops": c_stops[1:]
                    },
                    {
                        "time": (dep_time + timedelta(minutes=tot_time)).strftime('%I:%M %p').lstrip('0'),
                        "station": f"{norm_dest} Station", "type": "arrive", "color": "emerald", "meta": "Arrive at destination"
                    }
                ]
            }
        }

    # 6. TO NON-RAIL HUBS (BKC, Powai, Colaba, Nariman Point, Airport)
    if dest_loc["type"] == "hub":
        hub_key = dest_loc["hub"]
        
        # 6A. TO BKC (Bandra Kurla Complex)
        if hub_key == "bkc":
            is_from_western = orig_loc["line"] == "Western" if orig_loc["type"] == "station" else False
            gateway = "Bandra" if is_from_western else "Kurla"
            gateway_idx = (WESTERN_LINE if is_from_western else CENTRAL_LINE).index(gateway)
            orig_idx = orig_loc["index"] if orig_loc["type"] == "station" else 0
            
            stops = get_station_slice(WESTERN_LINE if is_from_western else CENTRAL_LINE, orig_idx, gateway_idx, is_fast=True, fast_set=(WESTERN_FAST_STOPS if is_from_western else CENTRAL_FAST_STOPS))
            t_train = max(12, int(len(stops) * 3.5 + 4))
            tot_time = t_train + 4 + 8
            dist = round(float(distance_km), 1) if (distance_km and float(distance_km) > 0) else 25.0
            
            return {
                "Fastest": {
                    "mode_sequence": [(f"Western Line Fast Local" if is_from_western else "Central Line Fast Local"), "Shared Auto"],
                    "time": tot_time, "cost": 45, "crowd": "High", "walking_distance": "120m", "transfers": 1, "waiting_time": 4, "dist": dist,
                    "timeline": [
                        {
                            "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                            "station": f"{norm_origin} Station", "type": "board", "color": "blue" if is_from_western else "red",
                            "badge": f"{'🔵 Churchgate (F)' if is_from_western else '🔴 CSMT (F)'}",
                            "train_info": f"{'Western' if is_from_western else 'Central'} Fast Local towards {gateway}",
                            "meta": f"{t_train} min ({len(stops)-1} stops) · Platform 3/4 · Stop ID: {norm_origin[:3].upper()}",
                            "stops": stops[1:]
                        },
                        {
                            "time": (dep_time + timedelta(minutes=t_train)).strftime('%I:%M %p').lstrip('0'),
                            "station": f"{gateway} Junction", "type": "transfer", "color": "amber",
                            "transfer_text": f"Exit {gateway} {'East' if is_from_western else 'West'} to BKC Shared Auto Stand",
                            "meta": "Local Train to Road Transit Interchange"
                        },
                        {
                            "time": (dep_time + timedelta(minutes=t_train + 4)).strftime('%I:%M %p').lstrip('0'),
                            "station": f"{gateway} Auto Stand", "type": "board", "color": "amber", "badge": "🛺 Shared Auto",
                            "train_info": "BKC Connector (via BKC Connector Flyover)",
                            "meta": "8 min (2.5 km) · ₹30 fixed per seat · Direct drop-off"
                        },
                        {
                            "time": (dep_time + timedelta(minutes=tot_time)).strftime('%I:%M %p').lstrip('0'),
                            "station": "Bandra Kurla Complex (BKC)", "type": "arrive", "color": "emerald", "meta": "Arrive at destination"
                        }
                    ]
                },
                "Cheapest": {
                    "mode_sequence": [(f"Western Line Local" if is_from_western else "Central Line Local"), "BEST Bus", "Walking"],
                    "time": tot_time + 15, "cost": 22, "crowd": "High", "walking_distance": "350m", "transfers": 1, "waiting_time": 8, "dist": dist,
                    "timeline": [
                        {
                            "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                            "station": f"{norm_origin} Station", "type": "board", "color": "blue" if is_from_western else "red",
                            "badge": f"{'🔵 Churchgate (S)' if is_from_western else '🔴 CSMT (S)'}",
                            "train_info": f"Local Train to {gateway}",
                            "meta": f"{t_train + 5} min · Platform 1", "stops": stops[1:]
                        },
                        {
                            "time": (dep_time + timedelta(minutes=t_train + 5)).strftime('%I:%M %p').lstrip('0'),
                            "station": f"{gateway} Bus Depot", "type": "transfer", "color": "amber",
                            "transfer_text": "Walk to BEST Bus Stop", "meta": "Transfer to BEST Bus"
                        },
                        {
                            "time": (dep_time + timedelta(minutes=t_train + 10)).strftime('%I:%M %p').lstrip('0'),
                            "station": f"{gateway} Station Bus Stop", "type": "board", "color": "amber", "badge": "🚌 Bus 310",
                            "train_info": "BEST Bus Route 310 towards BKC", "meta": "15 min · ₹6 fare"
                        },
                        {
                            "time": (dep_time + timedelta(minutes=tot_time + 15)).strftime('%I:%M %p').lstrip('0'),
                            "station": "Bandra Kurla Complex (BKC)", "type": "arrive", "color": "emerald", "meta": "Arrive at destination"
                        }
                    ]
                },
                "Reliable": {
                    "mode_sequence": [(f"Western Line AC Fast Local" if is_from_western else "Central Line AC Fast Local"), "Uber/Ola"],
                    "time": tot_time, "cost": 140, "crowd": "Low", "walking_distance": "80m", "transfers": 1, "waiting_time": 4, "dist": dist,
                    "timeline": [
                        {
                            "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                            "station": f"{norm_origin} Station", "type": "board", "color": "blue" if is_from_western else "red",
                            "badge": f"{'🔵 Churchgate (AC)' if is_from_western else '🔴 CSMT (AC)'}",
                            "train_info": f"AC Fast Local to {gateway}",
                            "meta": f"{t_train} min · AC Guaranteed Seating", "stops": stops[1:]
                        },
                        {
                            "time": (dep_time + timedelta(minutes=t_train)).strftime('%I:%M %p').lstrip('0'),
                            "station": f"{gateway} Station", "type": "transfer", "color": "amber",
                            "transfer_text": "Exit to App Cab Pickup Point", "meta": "Transfer to Uber/Ola"
                        },
                        {
                            "time": (dep_time + timedelta(minutes=t_train + 4)).strftime('%I:%M %p').lstrip('0'),
                            "station": f"{gateway} Cab Stand", "type": "board", "color": "amber", "badge": "🚖 Uber Go",
                            "train_info": f"App Cab to BKC", "meta": "8 min · ₹110"
                        },
                        {
                            "time": (dep_time + timedelta(minutes=tot_time)).strftime('%I:%M %p').lstrip('0'),
                            "station": "Bandra Kurla Complex (BKC)", "type": "arrive", "color": "emerald", "meta": "Arrive at destination"
                        }
                    ]
                }
            }

        # 6B. TO POWAI (Hiranandani)
        if hub_key == "powai":
            is_from_western = orig_loc["line"] == "Western" if orig_loc["type"] == "station" else False
            gateway = "Andheri" if is_from_western else "Kanjurmarg"
            gateway_idx = (WESTERN_LINE if is_from_western else CENTRAL_LINE).index(gateway)
            orig_idx = orig_loc["index"] if orig_loc["type"] == "station" else 0
            
            stops = get_station_slice(WESTERN_LINE if is_from_western else CENTRAL_LINE, orig_idx, gateway_idx, is_fast=True, fast_set=(WESTERN_FAST_STOPS if is_from_western else CENTRAL_FAST_STOPS))
            t_train = max(10, int(len(stops) * 3.2 + 3))
            t_last = 16 if is_from_western else 10
            tot_time = t_train + 3 + t_last
            dist = round(float(distance_km), 1) if (distance_km and float(distance_km) > 0) else 22.0
            
            return {
                "Fastest": {
                    "mode_sequence": [(f"Western Line Fast Local" if is_from_western else "Central Line Local"), "Shared Auto"],
                    "time": tot_time, "cost": 50, "crowd": "High", "walking_distance": "120m", "transfers": 1, "waiting_time": 4, "dist": dist,
                    "timeline": [
                        {
                            "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                            "station": f"{norm_origin} Station", "type": "board", "color": "blue" if is_from_western else "red",
                            "badge": f"{'🔵 Andheri (F)' if is_from_western else '🔴 CSMT (S)'}",
                            "train_info": f"Local Train to {gateway}",
                            "meta": f"{t_train} min ({len(stops)-1} stops) · Platform 2/3", "stops": stops[1:]
                        },
                        {
                            "time": (dep_time + timedelta(minutes=t_train)).strftime('%I:%M %p').lstrip('0'),
                            "station": f"{gateway} Station", "type": "transfer", "color": "amber",
                            "transfer_text": f"Exit {gateway} East to Auto Stand", "meta": "Local Train to Auto Interchange"
                        },
                        {
                            "time": (dep_time + timedelta(minutes=t_train + 3)).strftime('%I:%M %p').lstrip('0'),
                            "station": f"{gateway} Auto Stand", "type": "board", "color": "amber", "badge": "🛺 Auto Rickshaw",
                            "train_info": "Metered Auto to Powai (Hiranandani)",
                            "meta": f"{t_last} min · via JVLR / Central Ave"
                        },
                        {
                            "time": (dep_time + timedelta(minutes=tot_time)).strftime('%I:%M %p').lstrip('0'),
                            "station": "Powai (Hiranandani)", "type": "arrive", "color": "emerald", "meta": "Arrive at destination"
                        }
                    ]
                },
                "Cheapest": {
                    "mode_sequence": [(f"Western Line Local" if is_from_western else "Central Line Local"), "BEST Bus", "Walking"],
                    "time": tot_time + 14, "cost": 20, "crowd": "High", "walking_distance": "350m", "transfers": 1, "waiting_time": 7, "dist": dist,
                    "timeline": [
                        {
                            "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                            "station": f"{norm_origin} Station", "type": "board", "color": "blue" if is_from_western else "red",
                            "badge": "Local Train", "train_info": f"Local Train to {gateway}",
                            "meta": f"{t_train + 4} min · Platform 1", "stops": stops[1:]
                        },
                        {
                            "time": (dep_time + timedelta(minutes=t_train + 4)).strftime('%I:%M %p').lstrip('0'),
                            "station": f"{gateway} Bus Stop", "type": "transfer", "color": "amber",
                            "transfer_text": "Board BEST Bus to Powai", "meta": "Transfer to Bus"
                        },
                        {
                            "time": (dep_time + timedelta(minutes=t_train + 8)).strftime('%I:%M %p').lstrip('0'),
                            "station": f"{gateway} Bus Stop", "type": "board", "color": "amber", "badge": "🚌 Bus 392",
                            "train_info": "BEST Bus towards Powai", "meta": "18 min · ₹6 fare"
                        },
                        {
                            "time": (dep_time + timedelta(minutes=tot_time + 14)).strftime('%I:%M %p').lstrip('0'),
                            "station": "Powai (Hiranandani)", "type": "arrive", "color": "emerald", "meta": "Arrive at destination"
                        }
                    ]
                },
                "Reliable": {
                    "mode_sequence": [(f"Western Line AC Fast Local" if is_from_western else "Central Line AC Fast Local"), "Uber/Ola"],
                    "time": tot_time, "cost": 160, "crowd": "Low", "walking_distance": "80m", "transfers": 1, "waiting_time": 4, "dist": dist,
                    "timeline": [
                        {
                            "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                            "station": f"{norm_origin} Station", "type": "board", "color": "blue" if is_from_western else "red",
                            "badge": "AC Local", "train_info": f"AC Local to {gateway}",
                            "meta": f"{t_train} min · AC Seating", "stops": stops[1:]
                        },
                        {
                            "time": (dep_time + timedelta(minutes=t_train)).strftime('%I:%M %p').lstrip('0'),
                            "station": f"{gateway} Station", "type": "transfer", "color": "amber",
                            "transfer_text": "Exit to Cab Pickup", "meta": "Transfer to Cab"
                        },
                        {
                            "time": (dep_time + timedelta(minutes=t_train + 3)).strftime('%I:%M %p').lstrip('0'),
                            "station": f"{gateway} Cab Stand", "type": "board", "color": "amber", "badge": "🚖 Uber Go",
                            "train_info": "App Cab to Powai", "meta": f"{t_last} min · ₹130"
                        },
                        {
                            "time": (dep_time + timedelta(minutes=tot_time)).strftime('%I:%M %p').lstrip('0'),
                            "station": "Powai (Hiranandani)", "type": "arrive", "color": "emerald", "meta": "Arrive at destination"
                        }
                    ]
                }
            }

        # 6C. TO SOUTH MUMBAI HUBS (Colaba, Nariman Point, Fort)
        if hub_key in ("colaba", "nariman", "fort"):
            is_from_western = orig_loc["line"] == "Western" if orig_loc["type"] == "station" else False
            gateway = "Churchgate" if is_from_western else "CSMT"
            gateway_idx = (WESTERN_LINE if is_from_western else CENTRAL_LINE).index(gateway)
            orig_idx = orig_loc["index"] if orig_loc["type"] == "station" else 0
            
            stops = get_station_slice(WESTERN_LINE if is_from_western else CENTRAL_LINE, orig_idx, gateway_idx, is_fast=True, fast_set=(WESTERN_FAST_STOPS if is_from_western else CENTRAL_FAST_STOPS))
            t_train = max(15, int(len(stops) * 3.5 + 4))
            tot_time = t_train + 3 + 8
            dist = round(float(distance_km), 1) if (distance_km and float(distance_km) > 0) else 32.0
            
            return {
                "Fastest": {
                    "mode_sequence": [(f"Western Line Fast Local" if is_from_western else "Central Line Fast Local"), "Taxi"],
                    "time": tot_time, "cost": 45, "crowd": "High", "walking_distance": "120m", "transfers": 1, "waiting_time": 4, "dist": dist,
                    "timeline": [
                        {
                            "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                            "station": f"{norm_origin} Station", "type": "board", "color": "blue" if is_from_western else "red",
                            "badge": f"{'🔵 Churchgate (F)' if is_from_western else '🔴 CSMT (F)'}",
                            "train_info": f"Fast Local towards {gateway} Terminus",
                            "meta": f"{t_train} min ({len(stops)-1} stops) · Platform 3/4 · Stop ID: {norm_origin[:3].upper()}",
                            "stops": stops[1:]
                        },
                        {
                            "time": (dep_time + timedelta(minutes=t_train)).strftime('%I:%M %p').lstrip('0'),
                            "station": f"{gateway} Terminus", "type": "transfer", "color": "amber",
                            "transfer_text": f"Exit Platform 1 to {gateway} Kaali Peeli Taxi Stand",
                            "meta": "Local Train to Road Transit Interchange"
                        },
                        {
                            "time": (dep_time + timedelta(minutes=t_train + 3)).strftime('%I:%M %p').lstrip('0'),
                            "station": f"{gateway} Taxi Stand", "type": "board", "color": "amber", "badge": "🚖 Road Cab",
                            "train_info": f"Kaali Peeli Taxi to {norm_dest}",
                            "meta": "8 min (2.2 km) · Metered Taxi"
                        },
                        {
                            "time": (dep_time + timedelta(minutes=tot_time)).strftime('%I:%M %p').lstrip('0'),
                            "station": norm_dest, "type": "arrive", "color": "emerald", "meta": "Arrive at destination"
                        }
                    ]
                },
                "Cheapest": {
                    "mode_sequence": [(f"Western Line Local" if is_from_western else "Central Line Local"), "Walking"],
                    "time": tot_time + 10, "cost": 15, "crowd": "High", "walking_distance": "1.2 km", "transfers": 0, "waiting_time": 5, "dist": dist,
                    "timeline": [
                        {
                            "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                            "station": f"{norm_origin} Station", "type": "board", "color": "blue" if is_from_western else "red",
                            "badge": f"{'🔵 Churchgate (S)' if is_from_western else '🔴 CSMT (S)'}",
                            "train_info": f"Slow Local towards {gateway}",
                            "meta": f"{t_train + 6} min · Platform 1/2", "stops": stops[1:]
                        },
                        {
                            "time": (dep_time + timedelta(minutes=tot_time + 10)).strftime('%I:%M %p').lstrip('0'),
                            "station": norm_dest, "type": "arrive", "color": "emerald", "meta": f"Arrive at {norm_dest} (walk from {gateway})"
                        }
                    ]
                },
                "Reliable": {
                    "mode_sequence": [(f"Western Line AC Fast Local" if is_from_western else "Central Line AC Fast Local"), "Taxi"],
                    "time": tot_time, "cost": 125, "crowd": "Low", "walking_distance": "100m", "transfers": 1, "waiting_time": 4, "dist": dist,
                    "timeline": [
                        {
                            "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                            "station": f"{norm_origin} Station", "type": "board", "color": "blue" if is_from_western else "red",
                            "badge": "AC Local", "train_info": f"AC Local to {gateway}",
                            "meta": f"{t_train} min · AC Guaranteed Seating", "stops": stops[1:]
                        },
                        {
                            "time": (dep_time + timedelta(minutes=t_train)).strftime('%I:%M %p').lstrip('0'),
                            "station": f"{gateway} Terminus", "type": "transfer", "color": "amber",
                            "transfer_text": "Exit to Taxi Stand", "meta": "Transfer to Taxi"
                        },
                        {
                            "time": (dep_time + timedelta(minutes=t_train + 3)).strftime('%I:%M %p').lstrip('0'),
                            "station": f"{gateway} Taxi Stand", "type": "board", "color": "amber", "badge": "🚖 Road Cab",
                            "train_info": f"Taxi to {norm_dest}", "meta": "8 min · Metered Taxi"
                        },
                        {
                            "time": (dep_time + timedelta(minutes=tot_time)).strftime('%I:%M %p').lstrip('0'),
                            "station": norm_dest, "type": "arrive", "color": "emerald", "meta": "Arrive at destination"
                        }
                    ]
                }
            }

    # 7. DEFAULT GENERAL TRANSIT FALLBACK
    dist = round(float(distance_km), 1) if (distance_km and float(distance_km) > 0) else 24.0
    est_time = max(20, int(dist * 1.5 + 8))
    train_mode = "Central Line Fast Local" if "Central" in orig_loc.get("line", "") else "Western Line Fast Local"
    
    return {
        "Fastest": {
            "mode_sequence": [train_mode, "Shared Auto"],
            "time": est_time, "cost": 35, "crowd": "High", "walking_distance": "200m", "transfers": 1, "waiting_time": 4, "dist": dist,
            "timeline": [
                {
                    "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                    "station": f"{norm_origin} Station", "type": "board", "color": "red" if "Central" in train_mode else "blue",
                    "badge": "Transit Boarding", "train_info": f"{train_mode} Corridor",
                    "meta": f"{est_time - 8} min · Platform 2/3", "stops": ["En-route Suburban Stations"]
                },
                {
                    "time": (dep_time + timedelta(minutes=est_time - 8)).strftime('%I:%M %p').lstrip('0'),
                    "station": "Nearest Junction", "type": "transfer", "color": "amber",
                    "transfer_text": "Exit to Last-Mile Auto / Taxi Stand", "meta": "Transit Interchange"
                },
                {
                    "time": (dep_time + timedelta(minutes=est_time)).strftime('%I:%M %p').lstrip('0'),
                    "station": norm_dest, "type": "arrive", "color": "emerald", "meta": "Arrive at destination"
                }
            ]
        },
        "Cheapest": {
            "mode_sequence": [train_mode, "Walking"],
            "time": est_time + 10, "cost": 15, "crowd": "High", "walking_distance": "450m", "transfers": 0, "waiting_time": 6, "dist": dist,
            "timeline": [
                {
                    "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                    "station": f"{norm_origin} Station", "type": "board", "color": "red" if "Central" in train_mode else "blue",
                    "badge": "Local Train", "train_info": f"{train_mode} Corridor",
                    "meta": f"{est_time} min · Platform 1", "stops": ["En-route Suburban Stations"]
                },
                {
                    "time": (dep_time + timedelta(minutes=est_time + 10)).strftime('%I:%M %p').lstrip('0'),
                    "station": norm_dest, "type": "arrive", "color": "emerald", "meta": "Arrive at destination (walk 450m)"
                }
            ]
        },
        "Reliable": {
            "mode_sequence": [f"{train_mode} (AC)", "Taxi"],
            "time": est_time, "cost": 120, "crowd": "Low", "walking_distance": "120m", "transfers": 1, "waiting_time": 4, "dist": dist,
            "timeline": [
                {
                    "time": dep_time.strftime('%I:%M %p').lstrip('0'),
                    "station": f"{norm_origin} Station", "type": "board", "color": "red" if "Central" in train_mode else "blue",
                    "badge": "AC Local", "train_info": f"AC {train_mode}",
                    "meta": f"{est_time - 8} min · AC Guaranteed Seating", "stops": ["En-route Suburban Stations"]
                },
                {
                    "time": (dep_time + timedelta(minutes=est_time)).strftime('%I:%M %p').lstrip('0'),
                    "station": norm_dest, "type": "arrive", "color": "emerald", "meta": "Arrive at destination"
                }
            ]
        }
    }

# ---------------------------------------------------------------------
# MAIN EXPORT FOR SERVER.PY: CALCULATE_OPTIMAL_ROUTES
# ---------------------------------------------------------------------

def calculate_optimal_routes(origin, destination, preferences, distance_km=None):
    norm_origin = origin.strip().title()
    norm_dest = destination.strip().title()
    
    if norm_origin.lower() == norm_dest.lower():
        return []
        
    routes = generate_mumbai_routes(origin, destination, distance_km)
    if not routes:
        return []
        
    scored_routes = []
    
    active_prefs = dict(preferences) if preferences else {}
    if not any(active_prefs.get(k) for k in ['fastest', 'cheapest', 'reliable']):
        active_prefs['fastest'] = True

    now = datetime.now()
    final_km = 0.0

    for strategy, details in routes.items():
        if strategy == "Fastest" and not active_prefs.get('fastest'):
            continue
        if strategy == "Cheapest" and not active_prefs.get('cheapest'):
            continue
        if strategy == "Reliable" and not active_prefs.get('reliable'):
            continue
            
        score = 0
        if strategy == "Fastest":
            score = 300
        elif strategy == "Cheapest":
            score = 200
        elif strategy == "Reliable":
            score = 100
            
        final_km = round(float(distance_km), 1) if (distance_km and float(distance_km) > 0) else details.get("dist", 25.0)
        route_time = details["time"]
        
        # Real-time Google Maps style departure and arrival window
        dep_time = now + timedelta(minutes=4)
        arr_time = dep_time + timedelta(minutes=route_time)
        dep_window = f"{dep_time.strftime('%I:%M %p').lstrip('0')} — {arr_time.strftime('%I:%M %p').lstrip('0')}"
        
        # Next 3 departures
        next_trains = [
            f"{dep_time.strftime('%I:%M %p').lstrip('0')}",
            f"{(dep_time + timedelta(minutes=7)).strftime('%I:%M %p').lstrip('0')}",
            f"{(dep_time + timedelta(minutes=14)).strftime('%I:%M %p').lstrip('0')}"
        ]
        
        # Environmental and financial savings vs taking a personal cab
        co2_saved = round(max(0.5, final_km * 0.13), 1)
        cost_saved = int(max(50, (final_km * 14 + 120) - details["cost"]))
        
        # Construct turn-by-turn itinerary steps for fallback
        steps = []
        for idx, m in enumerate(details["mode_sequence"]):
            if "Local" in m:
                steps.append({
                    "mode": m,
                    "action": f"Board {m}",
                    "stop": f"From {norm_origin} (Platform 4/5)" if idx == 0 else "Platform Interchange",
                    "badge": "🔴 Central" if "Central" in m else ("🔵 Western" if "Western" in m else "🟠 Harbour")
                })
            elif "Metro" in m:
                steps.append({
                    "mode": m,
                    "action": f"Transfer to {m}",
                    "stop": "Metro Line concourse",
                    "badge": "🚇 Metro"
                })
            elif "Taxi" in m or "Auto" in m or "Uber" in m:
                steps.append({
                    "mode": m,
                    "action": f"Take {m} for connection",
                    "stop": f"Drop-off at {norm_dest}",
                    "badge": "🚖 Road Transit"
                })
            elif "Walking" in m or "Bus" in m:
                steps.append({
                    "mode": m,
                    "action": f"Walk {details['walking_distance']} to destination" if "Walking" in m else f"Take {m}",
                    "stop": f"Arrive at {norm_dest}",
                    "badge": "🚶 Walk" if "Walking" in m else "🚌 BEST"
                })

        scored_routes.append({
            "strategy": strategy,
            "mode_sequence": details["mode_sequence"],
            "time": route_time,
            "cost": details["cost"],
            "crowd": details["crowd"],
            "walking_distance": details["walking_distance"],
            "transfers": details["transfers"],
            "waiting_time": details["waiting_time"],
            "total_km": final_km,
            "departure_window": dep_window,
            "frequency": "every 4–6 mins",
            "next_trains": next_trains,
            "co2_saved_kg": co2_saved,
            "cost_saved_inr": cost_saved,
            "steps": steps,
            "timeline": details.get("timeline", []),
            "score": float(score)
        })
        
    scored_routes.sort(key=lambda x: x['score'], reverse=True)
    
    # Road comparison data (Cab, Two-Wheeler)
    ref_km = final_km if final_km > 0 else 32.0
    cab_mins = int(ref_km * 2.1)
    bike_mins = int(ref_km * 1.85)
    
    road_comparisons = {
        "cab": {
            "title": "via Highway / Major Arterial Road",
            "duration": f"{cab_mins // 60} hr {cab_mins % 60} min",
            "distance": f"{round(ref_km * 1.15, 1)} km",
            "cost": f"₹{int(ref_km * 14 + 110)}",
            "traffic": "🔴 Heavy Congestion (Peak Rush)"
        },
        "bike": {
            "title": "via Two-Wheeler / Bike Taxi",
            "duration": f"{bike_mins // 60} hr {bike_mins % 60} min",
            "distance": f"{round(ref_km * 1.05, 1)} km",
            "cost": f"₹{int(ref_km * 3.5 + 45)}",
            "traffic": "🟠 Slow Moving Traffic"
        }
    }
    
    seed_val = hash(norm_origin + norm_dest)
    random.seed(seed_val)
    
    crowd_levels = ["🔴 Heavy Crush Load", "🟠 Moderate Crowd", "🟢 Normal / Empty"]
    traffic_levels = ["🔴 Severe Traffic Jam", "🟠 Slow Moving Traffic", "🟢 Clear Roads", "🔴 Surge Pricing Active"]
    
    insights = {
        "origin_station": random.choice(crowd_levels),
        "dest_area": random.choice(traffic_levels),
        "weather": random.choice(["Clear", "Light Rain", "Heavy Rain (Trains Delayed)"])
    }
    
    return {
        "routes": scored_routes,
        "insights": insights,
        "road_comparisons": road_comparisons
    }
