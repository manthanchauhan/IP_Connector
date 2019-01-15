"""
Auto connector class
"""

import time
import os
from datetime import datetime
import sys


class NetworkSupervisor(object):
    def __init__(self, ip_connector, retry_sleep=1, recheck_sleep=1):
        self.ip_connector = ip_connector
        self.retry_sleep = retry_sleep
        self.recheck_sleep = recheck_sleep

    def start_surveillance(self):
        internet_access = False
        while True:

            if self.internet_available():
                if not internet_access:
                    f = open('logout_details.txt', 'a')
                    sys.stdout = f
                    print('Network back at: ' + str(datetime.now()))
                    f.close()
                    internet_access = True
                # print('connected')
                time.sleep(self.recheck_sleep)

            else:
                internet_access = False
                f = open('logout_details.txt', 'a')
                sys.stdout = f
                print('Network lost at: ' + str(datetime.now()))
                print('Reason: ', end='')
                f.close()
                if not self.wifi_connected():
                    reason = 'Wifi disconnected'

                    while not self.wifi_connected():
                        # print('no wifi')
                        time.sleep(self.retry_sleep)
                    time.sleep(1)

                    if self.internet_available():
                        f = open('logout_details.txt')
                        sys.stdout = f
                        f.close()
                        continue
                    else:
                        # print('no internet')
                        self.ip_connector.login()
                else:
                    reason = 'ISP down'
                    # print('no internet')
                    self.ip_connector.login()
                f = open('logout_details.txt', 'a')
                sys.stdout = f
                print(reason)
                f.close()

    @staticmethod
    def wifi_connected():
        a = os.popen("ping -c 1 0 | grep -E -o '[^[:space:]]+ packet loss'").read()
        # print(a)
        # print(self.connector.gateway)
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
