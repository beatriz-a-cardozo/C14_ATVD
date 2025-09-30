import os
import smtplib
import ssl
from email.message import EmailMessage

#Pega os secrets do actions
smtp_user = os.getenv("SMTP_USER")
smtp_pass = os.getenv("SMTP_PASS")
mail_to = os.getenv("MAIL_TO")

msg = EmailMessage()
msg["From"] = smtp_user
msg["To"] = mail_to
msg["Subject"] = "Mensagem do pipeline"
msg.set_content("O build foi executado com sucesso!")

context = ssl.create_default_context()
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls(context=context)
    server.login(smtp_user, smtp_pass)
    server.send_message(msg)

print("Email enviado com sucesso!")