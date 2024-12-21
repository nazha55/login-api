import firebase_admin
import os
from firebase_admin import credentials
from firebase_admin import firestore
# key_path = os.getenv('FIREBASE_KEY_PATH')
# if not key_path:
#     raise ValueError("FIREBASE_KEY_PATH environment variable is not set.")
# cred = credentials.Certificate(key_path)

cred = credentials.Certificate("private_key.json")
firebase_admin.initialize_app(cred)

db=firestore.client()
 
COLLECTION = 'users'

doc_ref = db.collection(COLLECTION).document()


def set_contact(user_id,data):
    db.collection(COLLECTION).document(user_id).set(data)

def update_contact(user_id,data):
    db.collection(COLLECTION).document(user_id).update(data)

def fetch_contact(user_id):
    data = db.collection(COLLECTION).document(user_id).get().to_dict()
    return data

def delete_otp(user_id):
    try:
        db.collection(COLLECTION).document(user_id).update({'otp': firestore.DELETE_FIELD})
    except Exception as e:
        print(f"Error deleting OTP for user {user_id}: {e}")
        raise   

def delete_verified(user_id):
    try:
        db.collection(COLLECTION).document(user_id).update({'is_verified': firestore.DELETE_FIELD})
    except Exception as e:
        print(f"Error deleting 'is_verified' for user {user_id}: {e}")
        raise 