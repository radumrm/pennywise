# firestore.py
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("/home/ia4/pennywise-9367d-firebase-adminsdk-fbsvc-dccb030fe4.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()
