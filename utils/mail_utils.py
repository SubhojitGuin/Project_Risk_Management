import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
load_dotenv()

# Create an EmailMessage object
message = EmailMessage()

email = os.getenv("MAIL_USERNAME")
password = os.getenv("MAIL_PASSWORD")
message["From"] = email

receiver_addresses = [
    "subhojitgdsc7@gmail.com",
    "sudeshnagdsc@gmail.com",
]

def send_mail(content, project_key):
    
    message.set_content(content)
    message["Subject"] = f"Critical Alert! for project : {project_key}"   
    message["To"] = ", ".join(receiver_addresses)
    
    # Connect to the SMTP server and send the email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(email, password)  
        server.send_message(message)
    del message["To"]

if __name__ == "__main__":
    content = "This is a test email."
    project_key = "test_project"
    send_mail(content, project_key)
    print("Email sent successfully!")