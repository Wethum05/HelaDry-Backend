import firebase_admin
from firebase_admin import credentials
import json

def init_firebase(cert_json_string, database_url):
    """
    Initializes Firebase using a raw JSON string from environment variables.
    """
    if not firebase_admin._apps:
        if not cert_json_string:
            raise RuntimeError("FIREBASE_CREDENTIALS environment variable is empty or missing.")

        try:
            # Convert the string into a Python dictionary
            cert_dict = json.loads(cert_json_string)
            cred = credentials.Certificate(cert_dict)
            
            firebase_admin.initialize_app(cred, {
                "databaseURL": database_url
            })
            print("Firebase initialized successfully using environment variables.")
            
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON format in FIREBASE_CREDENTIALS: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Firebase: {e}")
