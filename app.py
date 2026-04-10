"""
Flask web application for Render deployment.
Provides a simple web interface to the calc library functionality.
"""

from flask import Flask, jsonify, request
import sys
import os

# Add sources directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sources'))
from calc import add2

app = Flask(__name__)


@app.route('/')
def home():
    """Home endpoint with app information."""
    return jsonify({
        "app": "Python Calculator App",
        "status": "running",
        "description": "Simple addition calculator - supports integers, floats, and strings",
        "version": "1.0.0",
        "endpoints": {
            "home": "GET /",
            "health": "GET /health",
            "add": "GET /add/<a>/<b> or POST /add"
        }
    })


@app.route('/health')
def health():
    """Health check endpoint for Render."""
    return jsonify({"status": "healthy"}), 200


@app.route('/add/<a>/<b>', methods=['GET'])
def add_get(a, b):
    """Add two values via GET request."""
    try:
        result = add2(str(a), str(b))
        return jsonify({
            "a": a,
            "b": b,
            "result": result,
            "operation": "addition"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Failed to perform addition"
        }), 400


@app.route('/add', methods=['POST'])
def add_post():
    """Add two values via POST request."""
    try:
        data = request.get_json()
        if not data or 'a' not in data or 'b' not in data:
            return jsonify({
                "error": "Missing required fields: 'a' and 'b'",
                "example": {"a": "10", "b": "20"}
            }), 400
        
        result = add2(str(data['a']), str(data['b']))
        return jsonify({
            "a": data['a'],
            "b": data['b'],
            "result": result,
            "operation": "addition"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Failed to perform addition"
        }), 400


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
