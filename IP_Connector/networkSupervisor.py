"""
Auto connector class
"""

import time
import os
from datetime import datetime
from IP_Connector.print_record import print_record


class NetworkSupervisor(object):
    def __init__(self, ip_connector, retry_sleep=1, recheck_sleep=1):
        self._ip_connector = ip_connector
        self._retry_sleep = retry_sleep
        self._recheck_sleep = recheck_sleep

    def start_surveillance(self):
        internet_access = False
        while True:

            if self.internet_available():
                if not internet_access:
                    print_record('Network back at: ' + str(datetime.now()) + '\n')
                    internet_access = True
                time.sleep(self._recheck_sleep)

            else:
                time.sleep(1)
                internet_access = False
                print_record('Network lost at: ' + str(datetime.now()) + '\n')
                print_record('Reason: ')
                if not self.wifi_connected():
                    print_record('Wifi disconnected\n')

                    while not self.wifi_connected():
                        # print('no wifi')
                        time.sleep(self._retry_sleep)
                    time.sleep(1)

                    if self.internet_available():
                        print_record(reason + '\n')
                        continue
                    else:
                        # print('no internet')
                        self._ip_connector.login()
                elif self.wifi_connected():
                    print_record('ISP down\n')
                    # print('no internet')
                    self._ip_connector.login()

    @staticmethod
    def wifi_connected():
        a = os.popen("ping -c 1 192.168.0.102 | grep -E -o '[^[:space:]]+ packet loss'").read()
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
