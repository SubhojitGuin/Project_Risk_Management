import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
load_dotenv()
# Create an EmailMessage object
message = EmailMessage()
message.set_content("Hello, this is a basic email sent using Python!")

email = os.getenv("MAIL_USERNAME")
password = os.getenv("MAIL_PASSWORD")
# Set the sender and recipient
message["From"] = "subhojitgdsc7@gmail.com"
message["To"] = "subhojitguin2004@gmail.com"
# Set the subject
message["Subject"] = "Hello from Python!"
# Connect to the SMTP server and send the email
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()  # Enable TLS
    server.login(email, password)  # Log in to your email account
    server.send_message(message)