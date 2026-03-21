import os

class Config:
    # On Render, set FLASK_DEBUG to "False" in Environment Variables
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"

    # This pulls the JSON string from Render OR defaults to the local filename
    # In Render, paste the ENTIRE content of your JSON file into a variable named FIREBASE_CREDENTIALS
    FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS", "firebase_key.json")

    FIREBASE_DATABASE_URL = os.getenv(
        "FIREBASE_DATABASE_URL",
        "https://solar-dryer-iot-default-rtdb.asia-southeast1.firebasedatabase.app/"
    )