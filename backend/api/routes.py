"""REST API routes for BLE Beacon Tracker."""

from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from app import db

api_bp = Blueprint('api', __name__)

# Health check
@api_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200

# Beacon endpoints
@api_bp.route('/beacons', methods=['GET'])
def get_beacons():
    """Get all beacons."""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 50, type=int)
        
        # Placeholder - would fetch from database
        beacons = []
        
        return jsonify({
            'success': True,
            'data': beacons,
            'page': page,
            'limit': limit
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/beacons/<beacon_id>', methods=['GET'])
def get_beacon(beacon_id):
    """Get specific beacon details."""
    try:
        # Placeholder - would fetch from database
        beacon_data = {
            'id': beacon_id,
            'name': f'Beacon {beacon_id}',
            'rssi': -75,
            'distance': 5.2,
            'last_seen': datetime.utcnow().isoformat()
        }
        
        return jsonify({
            'success': True,
            'data': beacon_data
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Location endpoints
@api_bp.route('/locations', methods=['POST'])
def update_location():
    """Update beacon location."""
    try:
        data = request.get_json()
        
        # Validate data
        required_fields = ['beacon_id', 'x', 'y']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {required_fields}'
            }), 400
        
        # Process location update
        beacon_id = data['beacon_id']
        x, y = data['x'], data['y']
        
        return jsonify({
            'success': True,
            'message': f'Location updated for beacon {beacon_id}',
            'data': {'beacon_id': beacon_id, 'x': x, 'y': y}
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Heatmap endpoints
@api_bp.route('/heatmap', methods=['GET'])
def get_heatmap():
    """Get location heatmap data."""
    try:
        zone_id = request.args.get('zone_id')
        time_range = request.args.get('time_range', '1h')
        
        # Placeholder heatmap data
        heatmap_data = {
            'zone_id': zone_id,
            'time_range': time_range,
            'grid': [],  # Would contain grid points with intensity values
            'max_intensity': 0,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return jsonify({
            'success': True,
            'data': heatmap_data
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Geofence endpoints
@api_bp.route('/geofences', methods=['POST'])
def create_geofence():
    """Create new geofence."""
    try:
        data = request.get_json()
        
        required_fields = ['zone_id', 'center_x', 'center_y', 'radius']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {required_fields}'
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Geofence created',
            'data': data
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Error handlers
@api_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'success': False, 'error': 'Not found'}), 404

@api_bp.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return jsonify({'success': False, 'error': 'Internal server error'}), 500
