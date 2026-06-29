import smtplib
from email.message import EmailMessage

EMAIL_ADDRESS = "xxxxx@gmail.com"
EMAIL_PASSWORD = "xxxxxxxxx"

RECIPIENTS = [
    "xxx@nise.my",         # To
    "xxx@gmail.com", # cc 
    
]

def send_alert(subject, body):

    msg = EmailMessage()

    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = ", ".join(RECIPIENTS)

    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    print("Alert email sent successfully!")