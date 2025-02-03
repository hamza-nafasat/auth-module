import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from configs.envConf import getEnv


SMTP_SERVER = getEnv("SMTP_SERVER")
SMTP_PORT = getEnv("SMTP_PORT")
SMTP_USERNAME = getEnv("SMTP_USERNAME")
SMTP_PASSWORD = getEnv("SMTP_PASSWORD")
SENDER_EMAIL = getEnv("SENDER_EMAIL")


async def sendMail(to: str, subject: str, body: str):
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        server = smtplib.SMTP_SSL("smtp.gmail.com", SMTP_PORT)
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SENDER_EMAIL, to, msg.as_string())
        server.quit()
        print("mail sent successfully")
        return True
    except Exception as e:
        print("error in send_mail controller", str(e))
        return False
