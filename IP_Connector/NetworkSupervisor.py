"""
Auto connector class
"""

import time
import os
from datetime import datetime
from IP_Connector.PrintRecord import print_record
from IP_Connector.automatic_email_sender.Sender import Sender
from IP_Connector.automatic_email_sender.Sender import valid_email


class NetworkSupervisor(object):
    def __init__(self, ip_connector):
        self._ip_connector = ip_connector
        self._retry_wait = 3
        self._recheck_wait = 10
        self._user_email = None
        self._user_name = 'Boss'
        self._reason = None
        self._down_time = None
        self._email = None
        self._email_password = None
        self._sender = Sender(email=self._email,
                              password=self._email_password,
                              message='email_message.txt')

    @property
    def user_email(self):
        return self._user_email

    @user_email.setter
    def user_email(self, email):
        if not valid_email(email):
            print('Not a valid email')
            return
        self._user_email = email

    @property
    def recheck_wait(self):
        return self._recheck_wait

    @recheck_wait.setter
    def recheck_wait(self, value):
        if value <= 0:
            print('Invalid wait time')
            return
        self._recheck_wait = value

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, name):
        self._user_name = name

    @property
    def retry_wait(self):
        return self._retry_wait

    @retry_wait.setter
    def retry_wait(self, value):
        if value <= 0:
            print('Invalid wait time')
            return
        self._retry_wait = value

    def start_surveillance(self):
        print_record('==============================================================\n')
        print_record('Starting network surveillance at ' + str(datetime.now()) + '\n')
        internet_access = True
        first_time_loss = None
        while True:

            if self.internet_available():
                if not internet_access:
                    self._sender.send_mail(recipient=self._user_email,
                                           subject='You network is back now',
                                           message_details={'name': self._user_name,
                                                            'reason': self._reason,
                                                            'down_time': str(self._down_time)[:-7]})
                    print_record('Network back at: ' + str(datetime.now()) + '\n')
                    internet_access = True
                first_time_loss = True
                time.sleep(self._recheck_wait)

            else:
                internet_access = False
                self._down_time = datetime.now()
                print_record('Network lost at: ' + str(self._down_time) + '\n')
                print_record('Reason: ')
                if first_time_loss:
                    time.sleep(10)
                first_time_loss = False

                if not self.wifi_connected():
                    self._reason = 'disconnected wifi'
                    print_record('Wifi disconnected\n')

                    while not self.wifi_connected():
                        time.sleep(self._retry_wait)

                    time.sleep(2)
                    if self.internet_available():
                        continue
                    else:
                        self._ip_connector.login()

                elif self.wifi_connected():
                    self._reason = 'down ISP'
                    print_record('ISP down\n')
                    self._ip_connector.login()
                    time.sleep(self._retry_wait)

    @staticmethod
    def wifi_connected():
        a = os.popen("ping -c 1 192.168.0.102 | grep -E -o '[^[:space:]]+ packet loss'").read()
        if a is '':
            return False
        else:
            return True

    @staticmethod
    def internet_available():
        a = os.popen("ping -w 5 'google.com' | grep -E -o '[^[:space:]]+ packet loss'").read()
        if a is '':
            return False
        a = int(a[:a.find('%')])
        if a == 100:
            return False
        else:
            return True
