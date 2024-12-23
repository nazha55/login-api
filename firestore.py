from firebase_admin import credentials, firestore
# from config import CONFIG
import firebase_admin
from firebase_admin import credentials, firestore
import os, json


# Initialize Firebase App
cred = credentials.Certificate('config.json')
firebase_app = firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()