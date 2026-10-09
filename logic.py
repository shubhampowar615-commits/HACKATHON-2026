import numpy as np

ROUTING_DATABASE = {
    "Kalyan_BKC": {
        "Fastest": {"mode_sequence": ["Fast Local", "Metro", "Auto"], "time": 65, "cost": 120, "crowd": "High"},
        "Cheapest": {"mode_sequence": ["Slow Local", "BEST Bus", "Walking"], "time": 105, "cost": 45, "crowd": "High"},
        "Reliable": {"mode_sequence": ["AC Local", "Metro"], "time": 75, "cost": 250, "crowd": "Medium"}
    },
    "Thane_BKC": {
        "Fastest": {"mode_sequence": ["Fast Local", "Metro", "Walking"], "time": 45, "cost": 80, "crowd": "High"},
        "Cheapest": {"mode_sequence": ["Slow Local", "BEST Bus", "Walking"], "time": 75, "cost": 30, "crowd": "High"},
        "Reliable": {"mode_sequence": ["AC Local", "Metro", "Walking"], "time": 50, "cost": 210, "crowd": "Low"}
    },
    "Borivali_CSMT": {
        "Fastest": {"mode_sequence": ["Fast Local", "Taxi"], "time": 55, "cost": 150, "crowd": "High"},
        "Cheapest": {"mode_sequence": ["Slow Local", "Walking"], "time": 85, "cost": 15, "crowd": "High"},
        "Reliable": {"mode_sequence": ["AC Local", "Taxi"], "time": 60, "cost": 220, "crowd": "Low"}
    }
}

def calculate_optimal_routes(origin, destination, preferences):
    corridor = f"{origin}_{destination}"
    
    if corridor not in ROUTING_DATABASE:
        return []
    
    routes = ROUTING_DATABASE[corridor]
    scored_routes = []
    
    # Preference multipliers
    w_fastest = 1.0 if preferences.get('fastest') else 0.1
    w_cheapest = 1.0 if preferences.get('cheapest') else 0.1
    w_reliable = 1.0 if preferences.get('reliable') else 0.1
    
    # Normalize weights using numpy
    weights = np.array([w_fastest, w_cheapest, w_reliable])
    if weights.sum() > 0:
        weights = weights / weights.sum()
    else:
        weights = np.array([0.33, 0.33, 0.34])
        
    for strategy, details in routes.items():
        score = 0
        if strategy == "Fastest":
            score += weights[0] * 100
        elif strategy == "Cheapest":
            score += weights[1] * 100
        elif strategy == "Reliable":
            score += weights[2] * 100
            
        scored_routes.append({
            "strategy": strategy,
            "mode_sequence": details["mode_sequence"],
            "time": details["time"],
            "cost": details["cost"],
            "crowd": details["crowd"],
            "score": float(score)
        })
        
    # Sort by score descending
    scored_routes.sort(key=lambda x: x['score'], reverse=True)
    return scored_routes

