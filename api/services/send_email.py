#!/usr/bin/env python3
"""
Module to send one time code for 2FA
"""
import email
import os
import smtplib
import random
from dotenv import load_dotenv
from email.mime.text import MIMEText

load_dotenv()

def generate_otp():
    """
    Generates a random 6-digit OTP.
    """
    return str(random.randint(100000, 999999))

def send_otp_email(to_email, password:int):
    """
    Sends a one-time password (OTP) to the specified email address.
    """
    sender_email = os.getenv("SENDER_EMAIL")
    sender_app_password = os.getenv("SENDER_APP_PASSWORD")
    if not sender_email or not sender_app_password:
        raise ValueError("Email credentials are not set in the environment variables.")
    msg = MIMEText(f"Dear Customer,\n\nYou have registered successfully to MedPulse. Your registration password is: {password}\nPlease use this code to complete your login.\nThank you for using MedPulse.")
    msg["Subject"] = "Your Registration Password"
    msg["From"] = sender_email
    msg["To"] = to_email

    # connect to the SMTP server and send the email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_app_password)
        server.sendmail(sender_email, to_email, msg.as_string())

if __name__ == "__main__":
    send_otp_email(to_email = email, password = otp)