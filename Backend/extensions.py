import firebase_admin
from firebase_admin import credentials
import json
import os

def init_firebase(cert_input, database_url):
    """
    Initializes Firebase by checking if cert_input is a path to a file 
    or a raw JSON string from an environment variable.
    """
    if not firebase_admin._apps:
        # 1. Try to treat cert_input as a file path (Local Dev)
        if os.path.exists(cert_input):
            cred = credentials.Certificate(cert_input)
        else:
            # 2. If no file exists, treat it as raw JSON text (Render Production)
            try:
                cert_dict = json.loads(cert_input)
                cred = credentials.Certificate(cert_dict)
            except (json.JSONDecodeError, ValueError) as e:
                raise RuntimeError(
                    f"Firebase initialization failed. 'cert_input' is neither a valid "
                    f"file path nor valid JSON string. Error: {e}"
                )

        firebase_admin.initialize_app(cred, {
            "databaseURL": database_url
        })