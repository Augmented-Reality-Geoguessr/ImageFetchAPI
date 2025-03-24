import os
import requests
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# API Keys and configurations
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
FIREBASE_CREDENTIALS_PATH = os.getenv('FIREBASE_CREDENTIALS_PATH', 'firebase-credentials.json')

# Street View API configuration
STREETVIEW_API_URL = "https://maps.googleapis.com/maps/api/streetview"
STREETVIEW_METADATA_URL = "https://maps.googleapis.com/maps/api/streetview/metadata"
STREETVIEW_IMAGE_SIZE = "600x400"  # Image resolution


# Validate Google Maps API key on startup
def validate_api_key():
    """Validate the Google Maps API key by making a test request"""
    if not GOOGLE_MAPS_API_KEY:
        logger.warning("Google Maps API key is not set in environment variables!")
        return False

    # Log partial API key for debugging (safely)
    key_prefix = GOOGLE_MAPS_API_KEY[:4] if len(GOOGLE_MAPS_API_KEY) > 8 else "****"
    key_suffix = GOOGLE_MAPS_API_KEY[-4:] if len(GOOGLE_MAPS_API_KEY) > 8 else "****"
    logger.info(f"Using API key: {key_prefix}...{key_suffix}")

    # Test with a known location that has Street View coverage (NYC)
    test_params = {
        "location": "40.714728,-73.998672",
        "key": GOOGLE_MAPS_API_KEY
    }

    try:
        logger.info(f"Making test request to: {STREETVIEW_METADATA_URL}")
        response = requests.get(STREETVIEW_METADATA_URL, params=test_params)

        logger.info(f"API Response status code: {response.status_code}")

        try:
            data = response.json()

            if data.get("status") == "OK":
                logger.info("✅ Google Maps API key validation successful!")
                return True
            else:
                logger.error(f"❌ API key validation failed. Status: {data.get('status')}")
                logger.error(f"Error message: {data.get('error_message', 'No detailed error message')}")
                return False

        except ValueError as e:
            logger.error(f"Failed to parse API response as JSON: {str(e)}")
            logger.error(f"Response content: {response.content[:200]}...")
            return False

    except Exception as e:
        logger.error(f"Could not validate Google Maps API key: {str(e)}")
        return False


# Run validation on import
api_key_valid = validate_api_key()