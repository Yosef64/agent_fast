import os
import json
import base64
import firebase_admin
from firebase_admin import credentials,firestore

firebase_key_base64 = os.getenv("FIREBASE_KEY_BASE64")
if firebase_key_base64:
    firebase_key_json = json.loads(base64.b64decode(firebase_key_base64).decode('utf-8'))
    cred = credentials.Certificate(firebase_key_json)
else:
    raise ValueError("FIREBASE_KEY_BASE64 environment variable not set")
firebase_admin.initialize_app(cred,{"storageBucket": "testing-518f3.firebasestorage.app",})
db = firestore.client()