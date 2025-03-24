import firebase_admin
from firebase_admin import credentials, firestore
import uuid
from datetime import datetime
import base64
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FirebaseService:
    def __init__(self):
        """Initialize Firebase connection"""
        self.initialize_firebase()
        self.db = firestore.client()

    def initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            # Check if already initialized
            firebase_admin.get_app()
            logger.info("Firebase already initialized")
        except ValueError:
            # Get the credentials file path from environment
            credentials_path = os.getenv('FIREBASE_CREDENTIALS_PATH', 'firebase-credentials.json')
            logger.info(f"Initializing Firebase with credentials file: {credentials_path}")

            try:
                # Initialize with just Firestore (no Storage)
                cred = credentials.Certificate(credentials_path)
                firebase_admin.initialize_app(cred)
                logger.info("Firebase initialized (Firestore only)")
            except Exception as e:
                logger.error(f"Error initializing Firebase: {str(e)}")
                raise

    def store_panorama_data(self, latitude, longitude, image_data, pano_id):
        """
        Store location and image data in Firestore
        Returns the document reference
        """
        # Create a unique ID for this location entry
        location_id = uuid.uuid4().hex

        # Convert image data to base64
        image_data.seek(0)
        image_bytes = image_data.read()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')

        # Create a document with location and image data
        panorama_data = {
            "latitude": latitude,
            "longitude": longitude,
            "image_base64": image_base64,
            "panorama_id": pano_id,
            "timestamp": firestore.SERVER_TIMESTAMP
        }

        # Add document to panoramas collection
        doc_ref = self.db.collection('panoramas').document(location_id)
        doc_ref.set(panorama_data)
        logger.info(f"Stored panorama data in Firestore with ID: {location_id}")

        return {
            "location_id": location_id,
            "firestore_path": f"panoramas/{location_id}"
        }

    def upload_image(self, image_data, latitude, longitude, pano_id):
        """
        Store panoramic image and location data in Firestore
        Returns information about the stored data
        """
        try:
            logger.info(f"Storing panorama data for location {latitude}, {longitude}")

            # Store everything in Firestore
            location_ref = self.store_panorama_data(latitude, longitude, image_data, pano_id)

            return {
                "location_data": {
                    "firestore_ref": location_ref,
                    "latitude": latitude,
                    "longitude": longitude,
                    "panorama_id": pano_id
                }
            }
        except Exception as e:
            logger.error(f"Error storing panorama: {str(e)}")
            raise