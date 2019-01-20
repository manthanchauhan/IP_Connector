"""
email sender class

sends only text emails
"""

import smtplib
from email.mime.text import MIMEText
from string import Template
from datetime import datetime


class Sender(object):
    def __init__(self, message=None, email=None, password=None):
        self.__email = email
        self.__password = password
        self.__message = message

    def __create_email(self, subject, recipient, message_details):
        with open(self.__message, 'r') as message_txt:
            time = int(str(datetime.now())[11:13])
            if 5 <= time <= 12:
                message_details['greeting'] = 'Good morning'
            elif 12 <= time <= 15:
                message_details['greeting'] = 'Good noon'
            elif 15 <= time <= 17:
                message_details['greeting'] = 'Good afternoon'
            elif 17 <= time <= 20:
                message_details['greeting'] = 'Good evening'
            else:
                message_details['greeting'] = 'Good night'
            message = Template(message_txt.read())
            message = message.substitute(**message_details)
            message = MIMEText(message)
            message['Subject'] = subject
            message['From'] = ''
            message['To'] = recipient
            return message

    def send_mail(self, recipient, subject, message_details):
        email_message = self.__create_email(subject, recipient, message_details)
        server = smtplib.SMTP('smtp.gmail.com', '587')
        server.starttls()
        server.login(self.__email, self.__password)
        server.sendmail(self.__email, recipient, email_message.as_string())
        server.quit()


def valid_email(email):
    raise NotImplementedError


