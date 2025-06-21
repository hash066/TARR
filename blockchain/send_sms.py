import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

# Fetch credentials from .env
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_PHONE")
COMPANY_PHONE = os.getenv("COMPANY_PHONE")  # Destination

client = Client(TWILIO_SID, TWILIO_AUTH)

def send_alert(reason, delta_t):
    try:
        msg = f"[TAR Alert] Failure detected: {reason}. ΔT = {delta_t}°C. Please check the system."
        message = client.messages.create(
            body=msg,
            from_=TWILIO_NUMBER,
            to=COMPANY_PHONE
        )
        print("✅ SMS sent:", message.sid)
    except Exception as e:
        print("❌ SMS error:", e)
