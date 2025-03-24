import random
import requests
import logging
from io import BytesIO
from config import GOOGLE_MAPS_API_KEY, STREETVIEW_API_URL, STREETVIEW_METADATA_URL, STREETVIEW_IMAGE_SIZE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LocationService:
    @staticmethod
    def generate_random_location():
        """
        Generate a random location that is likely to have street view available.
        Prioritizes urban areas and regions with high Street View coverage.
        """
        # Major regions with high probability of street view coverage
        regions = [
            # Urban US - higher priority
            {"lat_min": 32.0, "lat_max": 42.0, "lng_min": -118.0, "lng_max": -71.0, "weight": 3},
            # Urban Europe - higher priority
            {"lat_min": 45.0, "lat_max": 55.0, "lng_min": -5.0, "lng_max": 20.0, "weight": 3},
            # Japan - high coverage
            {"lat_min": 34.0, "lat_max": 38.0, "lng_min": 130.0, "lng_max": 141.0, "weight": 2},
            # Rest of North America
            {"lat_min": 25.0, "lat_max": 49.0, "lng_min": -125.0, "lng_max": -66.0, "weight": 1},
            # South America - urban centers
            {"lat_min": -34.0, "lat_max": -15.0, "lng_min": -70.0, "lng_max": -40.0, "weight": 1},
            # Australia - urban areas
            {"lat_min": -38.0, "lat_max": -25.0, "lng_min": 144.0, "lng_max": 153.0, "weight": 1},
            # South Africa
            {"lat_min": -34.0, "lat_max": -25.0, "lng_min": 18.0, "lng_max": 31.0, "weight": 1},
        ]

        # Create weighted list based on priority
        weighted_regions = []
        for region in regions:
            weight = region.pop("weight", 1)  # Extract weight and default to 1 if not specified
            weighted_regions.extend([region] * weight)

        # Select a random region from the weighted list
        region = random.choice(weighted_regions)

        # Generate random coordinates within selected region
        latitude = random.uniform(region["lat_min"], region["lat_max"])
        longitude = random.uniform(region["lng_min"], region["lng_max"])

        return round(latitude, 6), round(longitude, 6)

    @staticmethod
    def check_panorama_availability(latitude, longitude):
        """
        Check if a panorama is available at the given coordinates
        Returns the panorama ID if available, None otherwise
        """
        params = {
            "location": f"{latitude},{longitude}",
            "key": GOOGLE_MAPS_API_KEY
        }

        try:
            response = requests.get(STREETVIEW_METADATA_URL, params=params, timeout=5)
            response.raise_for_status()  # Raise exception for HTTP errors
            data = response.json()

            if data.get("status") == "OK":
                logger.info(f"Found panorama at {latitude}, {longitude}: {data.get('pano_id')}")
                return data.get("pano_id")
            else:
                logger.info(f"No panorama at {latitude}, {longitude}. Status: {data.get('status')}")

        except Exception as e:
            logger.error(f"Error checking panorama at {latitude}, {longitude}: {str(e)}")

        return None

    @staticmethod
    def get_panorama_image(pano_id):
        """
        Fetch a 360 panorama image for the given panorama ID
        Returns the image data if successful, None otherwise
        """
        params = {
            "size": STREETVIEW_IMAGE_SIZE,
            "pano": pano_id,
            "key": GOOGLE_MAPS_API_KEY,
            "fov": 90,  # Field of view
            "heading": 0  # Initial heading (0 = North)
        }

        try:
            response = requests.get(STREETVIEW_API_URL, params=params, timeout=10)
            response.raise_for_status()

            if response.headers.get('content-type').startswith('image/'):
                logger.info(f"Successfully fetched image for panorama ID: {pano_id}")
                return BytesIO(response.content)
            else:
                logger.warning(f"Received non-image response for panorama ID: {pano_id}")

        except Exception as e:
            logger.error(f"Error fetching panorama image for ID {pano_id}: {str(e)}")

        return None

    @staticmethod
    def find_valid_location():
        """
        Generate locations until we find one with a 360 panorama available
        Returns (latitude, longitude, image_data, pano_id)
        """
        max_attempts = 40  # Increased attempts to find a valid location
        attempts = 0

        logger.info(f"Starting search for valid panorama location. Max attempts: {max_attempts}")

        while attempts < max_attempts:
            latitude, longitude = LocationService.generate_random_location()
            logger.info(f"Attempt {attempts + 1}/{max_attempts}: Checking location {latitude}, {longitude}")

            pano_id = LocationService.check_panorama_availability(latitude, longitude)

            if pano_id:
                image_data = LocationService.get_panorama_image(pano_id)
                if image_data:
                    logger.info(f"Found valid location with panorama at {latitude}, {longitude}")
                    return latitude, longitude, image_data, pano_id

            attempts += 1

        logger.error(f"Failed to find valid location after {max_attempts} attempts")
        raise Exception("Could not find a valid location with panorama available")