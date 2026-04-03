import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path


class Mailer:

    def __init__(self, sender, password, smtp_port=587, mail_service='gmail'):
        self.sender = sender
        self.password = password
        self.smtp_port = smtp_port
        self.smtp_service = self.get_smtp_service(mail_service)
    def send_mail(self, recepients, raw_message, file_attachment_uri=None):
        msg =  self.prep_msg(recepients, raw_message, file_attachment_uri)
        with smtplib.SMTP(self.smtp_service, self.smtp_port) as smtp_server:
            smtp_server.ehlo()
            smtp_server.starttls()
            smtp_server.ehlo()
            smtp_server.login(self.sender, self.password)
            smtp_server.sendmail(self.sender, recepients, msg.as_string())

    def prep_msg(self, recepients,raw_message, file_attachment_uri):
        # msg = MIMEText(raw_message['body'])
        msg = MIMEMultipart()
        msg['Subject'] = raw_message['subject']
        msg['From'] = self.sender
        msg['To'] = ', '.join(recepients)
        msg.attach(MIMEText(raw_message['body'], 'plain'))
        if file_attachment_uri is not None:
            attachment = open(file_attachment_uri,"rb")
            p = MIMEBase('application', 'octet-stream')
            p.set_payload((attachment).read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition','attachment; filename= %s' % Path(file_attachment_uri).name)
            msg.attach(p)
        return msg

    def get_smtp_service(self, mail_service):
        if 'gmail' in mail_service.lower():
            return 'smtp.gmail.com'
        else:
            # implement others here TODO
            return None






