from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from twilio.rest import Client
from dotenv import load_dotenv
import os

TWILIO_ACCOUNT_SID="AC3d8a69533dd58e755f45f5c5aa3e5bf7"
TWILIO_AUTH_TOKEN="70eae166ea01b15d2bbaa83877fd2552"




def send_email_otp(contact: str, otp: str):
    sender_email = "lifo55078@gmail.com"
    sender_password = "xeuv zfbz pgma omzj "  
    receiver_email = contact

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Your OTP Code"
    body = f"Your OTP code is: {otp}"
    message.attach(MIMEText(body, "plain"))

    try:
        print("Connecting to the SMTP server...")
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)  
        print("Logging in...")
        server.login(sender_email, sender_password)
        print(f"Sending OTP to {contact}...")
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("OTP sent successfully!")
        server.quit()
    except Exception as e:
        print(f"Failed to send OTP: {e}")

    
# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = "+17163404884"

def send_otp_via_sms(mobile_number: str,otp) -> int:
    """
    send an OTP to the given mobile number via Twilio.
    """
    try:
        # account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        # auth_token = os.getenv('TWILIO_AUTH_TOKEN')

        # Check if the environment variables are set correctly
        if TWILIO_ACCOUNT_SID is None or TWILIO_AUTH_TOKEN is None:
            raise ValueError("Twilio credentials are not set in the environment variables.")

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        # Create Twilio client
        # client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        # Send the OTP
        message = client.messages.create(
            body=f"Your OTP is {otp}",
            from_=TWILIO_PHONE_NUMBER,
            to=mobile_number
        )

        return {f"Message sent to {mobile_number}, SID: {message.sid}"}

       
    except Exception as e:
        print(f"Failed to send OTP to {mobile_number}: {e}")
        raise