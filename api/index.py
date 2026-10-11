import sys
import os

# Add root directory to sys.path so logic.py can be imported seamlessly
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from flask import Flask, request, jsonify
from flask_cors import CORS
from logic import calculate_optimal_routes

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index_path = os.path.join(root_dir, 'index.html')
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'text/html; charset=utf-8'}
    return "Mumbai Commute Optimizer API is running", 200

@app.route('/api/route-optimize', methods=['POST', 'OPTIONS'])
def optimize_route():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "No JSON payload provided"}), 400
            
        origin = data.get('origin')
        destination = data.get('destination')
        preferences = data.get('preferences', {})
        distance_km = data.get('distance_km')
        
        if not origin or not destination:
            return jsonify({"error": "Missing origin or destination"}), 400
            
        routes = calculate_optimal_routes(origin, destination, preferences, distance_km)
        
        if not routes:
            return jsonify([]), 200
            
        return jsonify(routes), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/route-optimize', methods=['POST', 'OPTIONS'])
def optimize_route_sub():
    return optimize_route()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

