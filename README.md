# 🌍 Image Fetcher API - Geoguessr-style Location Image Retriever

## 📌 Project Overview

This Image Fetcher API is a powerful tool for generating random geographical locations and retrieving corresponding Street View images. Perfect for geolocation games, geographic research, or random location exploration.

## 🚀 Features

- 🎲 Random Location Generation
- 🗺️ Google Street View Image Retrieval
- 🔥 Firebase Cloud Firestore Integration
- 🛡️ API Key Validation
- 🩺 Health Check Endpoint

## 🛠️ Prerequisites

Before you begin, ensure you have the following:

- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [Google Cloud Platform Account](https://cloud.google.com/)
- [Firebase Account](https://firebase.google.com/)

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Augmented-Reality-Geoguessr/ImageFetchAPI.git
cd ImageFetchAPI
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root with the following contents:

```
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
FIREBASE_CREDENTIALS_PATH=/path/to/firebase-credentials.json
```

### 3. Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv myvenv

# Activate virtual environment
# On Windows
myvenv\Scripts\Activate
# On macOS/Linux
source myvenv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🌐 Google Cloud Setup

### API Activation

Ensure the following Google Cloud APIs are activated:
- [Street View Static API](https://console.cloud.google.com/apis/library/street-view-image-backend.googleapis.com)
- [Places API](https://console.cloud.google.com/apis/library/places.googleapis.com)
- [Maps JavaScript API](https://console.cloud.google.com/apis/library/maps-backend.googleapis.com)

## 🚀 Running the Application

```bash
python app.py
```

## 🔍 Endpoints

- `GET /`: API Key and path validation
- `GET /api/random-location`: Generate location and retrieve Street View image
- `GET /health`: Application health check

## 🖼️ Image Retrieval

To decode the base64 encoded image:
1. Retrieve the encoded text from Cloud Firestore
2. Use base64 decoding to convert back to an image

## 📦 Dependencies

- Flask
- Google Maps API
- Firebase Admin SDK
- Python-dotenv


## 🐛 Issues

Report issues on the [GitHub Issues page](https://github.com/Augmented-Reality-Geoguessr/ImageFetchAPI/issues)

## 📞 Contact

Daya Lokesh Duddupudi - [LinkedIn](https://www.linkedin.com/in/dayaduddupudi)

Project Link: [https://github.com/Augmented-Reality-Geoguessr/ImageFetchAPI](https://github.com/Augmented-Reality-Geoguessr/ImageFetchAPI)

---

**Disclaimer**: Ensure you comply with Google Maps API and Firebase terms of service when using this application.
