import firebase_admin
from firebase_admin import credentials
import json
import os

def init_firebase(cert_input, database_url):
    if not firebase_admin._apps:
        # Render puts secret files in /etc/secrets/
        render_secret_path = os.path.join("/etc/secrets", cert_input)
        
        # 1. Check if it's in Render's secret folder
        if os.path.exists(render_secret_path):
            print(f"Loading Firebase key from Render secrets: {render_secret_path}")
            cred = credentials.Certificate(render_secret_path)
        
        # 2. Check if it's in the local project folder
        elif os.path.exists(cert_input):
            print(f"Loading Firebase key from local path: {cert_input}")
            cred = credentials.Certificate(cert_input)
            
        # 3. Last resort: Try to treat the input string itself as JSON data
        else:
            try:
                cert_dict = json.loads(cert_input)
                cred = credentials.Certificate(cert_dict)
            except (json.JSONDecodeError, ValueError, TypeError) as e:
                raise RuntimeError(
                    f"Firebase failed. Looked in /etc/secrets/{cert_input}, "
                    f"local folder, and raw JSON string. None worked. Error: {e}"
                )

        firebase_admin.initialize_app(cred, {
            "databaseURL": database_url
        })
