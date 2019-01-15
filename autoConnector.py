"""
Auto connector class
"""

import time
import os
from datetime import datetime


class autoConnect(object):
    def __init__(self, connector, retry=1, recheck=1):
        self.connector = connector
        self.retry_sleep = retry
        self.recheck_sleep = recheck

    def surveillance(self):
        connection = None
        while True:
            if self.is_internet():
                if not connection:
                    print('Network back at: ' + str(datetime.now()))
                    connection = True
                # print('connected')
                time.sleep(self.recheck_sleep)
            else:
                connection = False
                print('Network lost at: ' + str(datetime.now()))
                print('Reason: ', end='')
                if self.is_wifi_connected() is False:
                    print('No wifi connected')
                    while self.is_wifi_connected() is False:
                        # print('no wifi')
                        time.sleep(self.retry_sleep)
                    time.sleep(self.retry_sleep)
                    if self.is_internet() is True:
                        pass
                    else:
                        # print('no internet')
                        self.connector.login()
                        self.connector.quit()
                else:
                    print('ISP down')
                    # print('no internet')
                    self.connector.login()
                    self.connector.quit()

    @staticmethod
    def is_wifi_connected():
        a = os.popen("ping -c 1 0 | grep -E -o '[^[:space:]]+ packet loss'").read()
        # print(a)
        # print(self.connector.gateway)
        if a is '':
            return False
        else:
            return True

    @staticmethod
    def is_internet():
        a = os.popen("ping -w 5 'google.com' | grep -E -o '[^[:space:]]+ packet loss'").read()
        if a is '':
            return False
        a = int(a[:a.find('%')])
        if a == 100:
            return False
        else:
            return True
