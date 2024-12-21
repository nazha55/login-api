from fastapi import HTTPException
import random,re
from utils import send_email_otp,send_otp_via_sms

def validate_contact(contact: str):
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    phone_regex = r"^\+?[1-9]\d{1,14}$"  

    if re.match(email_regex, contact):
        return "email"
    elif re.match(phone_regex, contact):
        return "phone"
    else:
        raise HTTPException(status_code=400, detail="Invalid contact format")
    
def generate_otp():
    otp = random.randint(1000, 9999)  
    print("the otp generated is ",otp)
    return otp

def send_otp(contact: str, otp: str, contact_type):
    if contact_type == "email":
        send_email_otp(contact, otp)
    elif contact_type == "phone":
        send_otp_via_sms(contact,otp)
    else:
        raise ValueError(f"Invalid contact type: {contact_type}. Must be 'email' or 'phone'.")