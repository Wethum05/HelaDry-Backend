import os

class Config:
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"

    # This MUST be the raw JSON string from your Firebase Admin SDK
    # In Render: Create an Environment Variable 'FIREBASE_CREDENTIALS' 
    # and paste the entire { ... } JSON content into it.
    FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")

    FIREBASE_DATABASE_URL = os.getenv(
        "FIREBASE_DATABASE_URL",
        "https://solar-dryer-iot-default-rtdb.asia-southeast1.firebasedatabase.app/"
    )
