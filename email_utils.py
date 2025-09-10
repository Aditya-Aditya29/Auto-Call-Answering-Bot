import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()




def send_email(transcript):
    # Company email (where the complaint/issue is delivered)
    sender_email = os.getenv("SENDER_EMAIL")  # The email you're sending from
    sender_password = os.getenv("SENDER_PASSWORD")  # App password or real password
    company_email = os.getenv("COMPANY_EMAIL")         # ✅ Replace with your actual email


    subject = "New Customer Call Transcript"
    body = f"A new customer message was recorded:\n\n{transcript}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = company_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, company_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print("Failed to send email:", str(e))
