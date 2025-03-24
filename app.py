from flask import Flask, jsonify, request
from firebase_service import FirebaseService
from location_service import LocationService
import os
import logging
from datetime import datetime
from config import api_key_valid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
firebase_service = FirebaseService()


def get_current_timestamp():
    """Get current timestamp in the required format"""
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


@app.route('/', methods=['GET'])
def home():
    """Root endpoint providing API information"""
    timestamp = get_current_timestamp()
    return jsonify({
        "api": "Random Location Panorama API",
        "status": "running",
        "api_key_status": "valid" if api_key_valid else "invalid",
        "endpoints": {
            "/api/random-location": "Get a random location with panorama",
            "/health": "Health check endpoint"
        },
        "timestamp": timestamp,
    })


@app.route('/api/random-location', methods=['GET'])
def get_random_location():
    timestamp = get_current_timestamp()

    # Check if API key is valid before proceeding
    if not api_key_valid:
        return jsonify({
            "status": "error",
            "message": "Google Maps API key validation failed. Please check your API key configuration.",
            "timestamp": timestamp,
        }), 500

    try:
        logger.info("Received request for random location")

        # Find a valid location with panorama
        latitude, longitude, image_data, pano_id = LocationService.find_valid_location()

        # Upload the image to Firebase (Base64 encoded in Firestore)
        logger.info(f"Storing panorama in Firestore for location {latitude}, {longitude}")
        resource_info = firebase_service.upload_image(image_data, latitude, longitude, pano_id)

        # Return minimal response with just success status and document reference
        return jsonify({
            "status": "success",
            "timestamp": timestamp,
            "reference": resource_info["location_data"]["firestore_ref"]["location_id"],
        })
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": timestamp,
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    timestamp = get_current_timestamp()
    api_status = "valid" if api_key_valid else "invalid"
    return jsonify({
        "status": "healthy",
        "api_key_status": api_status,
        "timestamp": timestamp,
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    if not api_key_valid:
        logger.warning(
            "⚠️ Starting app with invalid Google Maps API key. The /api/random-location endpoint may not work properly.")

    logger.info(f"Starting app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)