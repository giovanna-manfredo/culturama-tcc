import random
import smtplib
from email.mime.text import MIMEText
from django.template.loader import render_to_string
from dotenv import load_dotenv
import environ

load_dotenv()
env = environ.Env()

class EmailClient:
   
    @staticmethod
    def send_email(subject, body, sender, recipients, password):
                
        msg = MIMEText(body,'html')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
                smtp_server.login(sender, password)
                smtp_server.sendmail(sender, recipients, msg.as_string())
                return True
        except Exception as e:
            return e
       
    
    @staticmethod
    def create_email_validation_code(email:str):
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        subject = "Validate your code email"
        body = render_to_string('validate_layout.html', {
        'codigo_validacao': code,
    })

        sender = env("SYSTEM_EMAIL")
        recipients = [email]
        password = env("SYSTEM_PASSWORD_EMAIL")

        if EmailClient.send_email(subject, body, sender, recipients, password):
            return code