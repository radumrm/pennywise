import firebase_admin
from firebase_admin import credentials, firestore
import os

def get_database():

    if not firebase_admin._apps:
        key_path = os.getenv('FIREBASE_KEY_PATH', 'pennywise_key.json')
        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    return db

