import os

class Config:
    # Render puts secret files in /etc/secrets/
    # We check if that path exists; if not, we use the local filename
    RENDER_SECRET_PATH = "/etc/secrets/firebase_key.json"
    
    FIREBASE_CREDENTIALS = os.getenv(
        "FIREBASE_CREDENTIALS",
        RENDER_SECRET_PATH if os.path.exists(RENDER_SECRET_PATH) else "firebase_key.json"
    )
    
    FIREBASE_DATABASE_URL = os.getenv(
        "FIREBASE_DATABASE_URL",
        "https://solar-dryer-iot-default-rtdb.asia-southeast1.firebasedatabase.app/"
    )
