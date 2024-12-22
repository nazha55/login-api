from firebase_admin import credentials, firestore
from config import CONFIG
import firebase_admin
from firebase_admin import credentials, firestore
import json

# Initialize Firebase App

# Load the credentials
cred = credentials.Certificate(CONFIG)
firebase_app = firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()