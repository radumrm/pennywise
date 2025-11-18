import firebase_admin
from firebase_admin import credentials, firestore

def get_database():

    if not firebase_admin._apps:
        cred = credentials.Certificate("/home/ia4/pennywise-9367d-firebase-adminsdk-fbsvc-dccb030fe4.json")
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    return db

