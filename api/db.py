import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred,{'storageBucket': 'victorybot-bc6db.appspot.com'})

db = firestore.client()