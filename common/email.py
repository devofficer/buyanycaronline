import smtplib, ssl
from email.mime.text import MIMEText

from common.utils import ConfigFile

conf = ConfigFile.getInstance()["GMAIL"]


class EmailClient:
    __instance = None

    @staticmethod
    def getInstance():
        if EmailClient.__instance is None:
            EmailClient()
        return EmailClient.__instance

    def __init__(self, ):
        if EmailClient.__instance is not None:
            raise Exception("This class is a DataBase!")
        else:
            smtp_server = conf["SERVER"]
            port = conf["PORT"]
            sender_email = conf["EMAIL"]
            password = conf["PASSWORD"]
            try:
                smtpserver = smtplib.SMTP(smtp_server, port)
                smtpserver.ehlo()
                smtpserver.starttls()
                smtpserver.ehlo()
                smtpserver.login(sender_email, password)
                EmailClient.__instance = smtpserver
            except Exception as e:
                print(e)

    @staticmethod
    def send_reset_password(link: str, username: str):
        smtpserver = EmailClient.getInstance()
        body = "Hello customer\n" \
               "Please click on the link below to reset your password\n" + link
        msg = MIMEText(body, 'html')
        msg['Subject'] = 'RESET PASSWORD'
        msg['From'] = conf["EMAIL"]
        msg['To'] = username
        msg = msg.as_string()
        smtpserver.sendmail(msg=msg, from_addr=conf["EMAIL"], to_addrs=username)
