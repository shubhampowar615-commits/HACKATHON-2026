import numpy as np
import random

# Added new required metrics: walking_distance, transfers, waiting_time
HARDCODED_ROUTES = {
    "Kalyan_BKC": {
        "Fastest": {"mode_sequence": ["Central Line Local", "Metro Line 3", "Shared Auto"], "time": 65, "cost": 120, "crowd": "High", "walking_distance": "300m", "transfers": 2, "waiting_time": 8},
        "Cheapest": {"mode_sequence": ["Central Line Local", "BEST Bus", "Walking"], "time": 105, "cost": 45, "crowd": "High", "walking_distance": "600m", "transfers": 2, "waiting_time": 15},
        "Reliable": {"mode_sequence": ["Central Line Local", "Metro Line 3", "Shared Auto"], "time": 75, "cost": 250, "crowd": "Medium", "walking_distance": "200m", "transfers": 1, "waiting_time": 6}
    },
    "Thane_BKC": {
        "Fastest": {"mode_sequence": ["Central Line Local", "Metro Line 3", "Shared Auto"], "time": 45, "cost": 80, "crowd": "High", "walking_distance": "250m", "transfers": 1, "waiting_time": 6},
        "Cheapest": {"mode_sequence": ["Central Line Local", "BEST Bus", "Walking"], "time": 75, "cost": 30, "crowd": "High", "walking_distance": "500m", "transfers": 2, "waiting_time": 12},
        "Reliable": {"mode_sequence": ["Central Line Local", "Metro Line 3", "Shared Auto"], "time": 50, "cost": 210, "crowd": "Low", "walking_distance": "150m", "transfers": 1, "waiting_time": 5}
    },
    "Borivali_CSMT": {
        "Fastest": {"mode_sequence": ["Central Line Local", "Uber/Ola"], "time": 55, "cost": 150, "crowd": "High", "walking_distance": "200m", "transfers": 1, "waiting_time": 7},
        "Cheapest": {"mode_sequence": ["Central Line Local", "BEST Bus", "Walking"], "time": 85, "cost": 15, "crowd": "High", "walking_distance": "450m", "transfers": 1, "waiting_time": 14},
        "Reliable": {"mode_sequence": ["Central Line Local", "Uber/Ola"], "time": 60, "cost": 220, "crowd": "Low", "walking_distance": "150m", "transfers": 1, "waiting_time": 5}
    },
    "Kalyan_CSMT": {
        "Fastest": {"mode_sequence": ["Central Line Local", "Uber/Ola"], "time": 70, "cost": 60, "crowd": "High", "walking_distance": "300m", "transfers": 1, "waiting_time": 9},
        "Cheapest": {"mode_sequence": ["Central Line Local", "Walking"], "time": 95, "cost": 20, "crowd": "High", "walking_distance": "700m", "transfers": 0, "waiting_time": 14},
        "Reliable": {"mode_sequence": ["Central Line Local", "Uber/Ola"], "time": 75, "cost": 250, "crowd": "Low", "walking_distance": "100m", "transfers": 1, "waiting_time": 7}
    },
    "Thane_CSMT": {
        "Fastest": {"mode_sequence": ["Central Line Local", "Uber/Ola"], "time": 55, "cost": 50, "crowd": "High", "walking_distance": "200m", "transfers": 1, "waiting_time": 6},
        "Cheapest": {"mode_sequence": ["Central Line Local", "Walking"], "time": 70, "cost": 15, "crowd": "High", "walking_distance": "500m", "transfers": 0, "waiting_time": 10},
        "Reliable": {"mode_sequence": ["Central Line Local", "Uber/Ola"], "time": 60, "cost": 150, "crowd": "Low", "walking_distance": "100m", "transfers": 1, "waiting_time": 6}
    },
    "Borivali_BKC": {
        "Fastest": {"mode_sequence": ["Central Line Local", "Metro Line 3", "Shared Auto"], "time": 60, "cost": 110, "crowd": "High", "walking_distance": "300m", "transfers": 2, "waiting_time": 8},
        "Cheapest": {"mode_sequence": ["Central Line Local", "BEST Bus", "Walking"], "time": 95, "cost": 40, "crowd": "High", "walking_distance": "600m", "transfers": 2, "waiting_time": 15},
        "Reliable": {"mode_sequence": ["Central Line Local", "Metro Line 3", "Shared Auto"], "time": 65, "cost": 230, "crowd": "Medium", "walking_distance": "200m", "transfers": 1, "waiting_time": 7}
    },
    "Dadar_BKC": {
        "Fastest": {"mode_sequence": ["Central Line Local", "Shared Auto"], "time": 25, "cost": 60, "crowd": "High", "walking_distance": "150m", "transfers": 1, "waiting_time": 4},
        "Cheapest": {"mode_sequence": ["BEST Bus", "Walking"], "time": 45, "cost": 15, "crowd": "Medium", "walking_distance": "400m", "transfers": 0, "waiting_time": 8},
        "Reliable": {"mode_sequence": ["Uber/Ola"], "time": 30, "cost": 150, "crowd": "Low", "walking_distance": "50m", "transfers": 0, "waiting_time": 3}
    },
    "Dadar_CSMT": {
        "Fastest": {"mode_sequence": ["Central Line Local", "Uber/Ola"], "time": 20, "cost": 40, "crowd": "High", "walking_distance": "100m", "transfers": 1, "waiting_time": 3},
        "Cheapest": {"mode_sequence": ["Central Line Local", "Walking"], "time": 25, "cost": 10, "crowd": "High", "walking_distance": "500m", "transfers": 0, "waiting_time": 4},
        "Reliable": {"mode_sequence": ["Uber/Ola"], "time": 25, "cost": 100, "crowd": "Low", "walking_distance": "50m", "transfers": 0, "waiting_time": 2}
    }
}

def calculate_realistic_metrics(dist, modes, route_type):
    """Simulates real M-Indicator and Ola/Uber rates based on distance"""
    cost = 0
    time = 0
    
    # Split the total distance equally among transit modes (excluding walking)
    active_modes = [m for m in modes if m != "Walking"]
    dist_per_mode = dist / max(1, len(active_modes))
    
    for mode in modes:
        if mode == "Walking":
            time += 10 # reduced average walk time
            continue
            
        # 1. Ola/Uber & Taxi Logic (Realistic Fares)
        if mode in ["Taxi", "Uber/Ola"]:
            base_fare = 50 if mode == "Uber/Ola" else 28
            per_km = 18 if mode == "Uber/Ola" else 18.66
            cost += base_fare + max(0, (dist_per_mode - 1.5)) * per_km
            time += (dist_per_mode / 25) * 60 # 25 km/h avg speed
            
        elif "Auto" in mode:
            cost += 23 + max(0, (dist_per_mode - 1.5)) * 15.33
            time += (dist_per_mode / 25) * 60
            
        # 2. M-Indicator Logic (Realistic Train/Metro/Bus Fares)
        elif "Local" in mode:
            if "AC" in mode:
                cost += min(210, max(65, dist_per_mode * 5))
            else:
                cost += 5 if dist_per_mode <= 10 else (10 if dist_per_mode <= 25 else 15)
            time += (dist_per_mode / 45) * 60 # 45 km/h train speed
            
        elif "Metro" in mode:
            cost += 10 if dist_per_mode <= 3 else (20 if dist_per_mode <= 12 else 30)
            time += (dist_per_mode / 35) * 60 # 35 km/h metro speed
            
        elif "Bus" in mode:
            cost += 5 if dist_per_mode <= 5 else (10 if dist_per_mode <= 15 else 20)
            time += (dist_per_mode / 15) * 60 # 15 km/h bus speed
            
    # Apply minor strategic adjustments
    if route_type == "Fastest":
        time *= 0.85
        cost *= 1.2 # Surge pricing
    elif route_type == "Cheapest":
        time *= 1.2
    
    return int(time), int(cost)

def generate_dynamic_route(origin, destination, real_dist=None):
    """Generates realistic-looking fallback route data for ANY text location input"""
    if origin.lower().strip() == destination.lower().strip():
        return {}
        
    seed_val = hash(origin.lower().strip() + destination.lower().strip())
    random.seed(seed_val)
    
    if real_dist is not None:
        dist = float(real_dist)
    else:
        dist = random.randint(10, 60)
    
    # Dramatically reduced walking in the mode sequences
    fast_modes = ["Central Line Local", "Metro Line 3", "Uber/Ola"] if dist > 20 else ["Uber/Ola"]
    cheap_modes = ["Central Line Local", "BEST Bus", "Walking"] if dist > 20 else ["BEST Bus", "Walking"]
    reliable_modes = ["Central Line Local", "Metro Line 3", "Shared Auto"] if dist > 20 else ["Uber/Ola"]

    fast_time, fast_cost = calculate_realistic_metrics(dist, fast_modes, "Fastest")
    cheap_time, cheap_cost = calculate_realistic_metrics(dist, cheap_modes, "Cheapest")
    rel_time, rel_cost = calculate_realistic_metrics(dist, reliable_modes, "Reliable")

    def get_walk_dist(time_mins, pct):
        # Calculate walking duration based on total time, minimum 1 min
        walk_mins = max(1, int(time_mins * pct))
        # Convert duration to distance assuming ~80m per minute
        return f"{walk_mins * 80}m"

    return {
        "Fastest": {
            "mode_sequence": fast_modes,
            "time": fast_time,
            "cost": fast_cost,
            "crowd": "High",
            "walking_distance": get_walk_dist(fast_time, 0.05),
            "transfers": len(fast_modes) - 1,
            "waiting_time": max(2, int(fast_time * 0.10))
        },
        "Cheapest": {
            "mode_sequence": cheap_modes,
            "time": cheap_time,
            "cost": cheap_cost,
            "crowd": "High",
            "walking_distance": get_walk_dist(cheap_time, 0.15),
            "transfers": len(cheap_modes) - 1,
            "waiting_time": max(3, int(cheap_time * 0.20))
        },
        "Reliable": {
            "mode_sequence": reliable_modes,
            "time": rel_time,
            "cost": rel_cost,
            "crowd": random.choice(["Low", "Medium"]),
            "walking_distance": get_walk_dist(rel_time, 0.08),
            "transfers": len(reliable_modes) - 1,
            "waiting_time": max(2, int(rel_time * 0.10))
        }
    }

def calculate_optimal_routes(origin, destination, preferences, distance_km=None):
    # Normalize keys for looking up the hardcoded database
    norm_origin = origin.strip().title()
    norm_dest = destination.strip().title()
    
    # Check both normal and reversed directions for hardcoded stuff, else generate
    if norm_origin.lower() == norm_dest.lower():
        return []
        
    corridor_direct = f"{norm_origin}_{norm_dest}"
    
    if corridor_direct in HARDCODED_ROUTES:
        routes = HARDCODED_ROUTES[corridor_direct]
    else:
        routes = generate_dynamic_route(origin, destination, distance_km)
    
    if not routes:
        return []
        
    scored_routes = []
    
    for strategy, details in routes.items():
        # Strictly filter out strategies the user unchecked
        if strategy == "Fastest" and not preferences.get('fastest'):
            continue
        if strategy == "Cheapest" and not preferences.get('cheapest'):
            continue
        if strategy == "Reliable" and not preferences.get('reliable'):
            continue
            
        # Simple scoring to ensure consistent display order (Fastest > Cheapest > Reliable)
        score = 0
        if strategy == "Fastest":
            score = 300
        elif strategy == "Cheapest":
            score = 200
        elif strategy == "Reliable":
            score = 100
            
        scored_routes.append({
            "strategy": strategy,
            "mode_sequence": details["mode_sequence"],
            "time": details["time"],
            "cost": details["cost"],
            "crowd": details["crowd"],
            "walking_distance": details["walking_distance"],
            "transfers": details["transfers"],
            "waiting_time": details["waiting_time"],
            "total_km": round(float(distance_km), 1) if distance_km else random.randint(15, 45),
            "score": float(score)
        })
        
    scored_routes.sort(key=lambda x: x['score'], reverse=True)
    
    # Generate Google-like live insights for the origin and destination
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
        "insights": insights
    }
