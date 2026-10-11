from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from logic import calculate_optimal_routes

import os

app = Flask(__name__)
# Enable CORS for the local frontend integration
CORS(app)

@app.route('/')
def home():
    # Serve the frontend dashboard directly from the server
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'index.html')

@app.route('/api/route-optimize', methods=['POST'])
def optimize_route():
    try:
        data = request.get_json()
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

