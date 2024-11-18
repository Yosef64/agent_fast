import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred,{"storageBucket": "testing-518f3.firebasestorage.app",})

db = firestore.client()