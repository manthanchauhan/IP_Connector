"""
Ip connector class
"""
import json
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time
import sys


class IpConnector(object):

    def __init__(self):
        self.ssid = self.get_ssid()
        self._isp_wait = 10
        self._login_id = None
        self._password = None
        self._driver = None

        try:
            self._load_details('details.json')
        except FileNotFoundError:
            pass
        self._open_record('logout_details.txt')

    def _load_details(self, file_name):
        try:
            with open(file_name, 'r') as details:
                data = json.load(details)
                self._login_id = data[self.ssid]['id']
                self._password = data[self.ssid]['password']
        except FileNotFoundError:
            raise FileNotFoundError

    @staticmethod
    def _open_record(file_name):
        try:
            if os.stat(file_name).st_size >= 1000000000:
                os.remove(file_name)
                record = open(file_name, 'w')
                record.close()
        except FileNotFoundError:
            record = open(file_name, 'w')
            record.close()

    @property
    def isp_wait(self):
        return self._isp_wait

    @isp_wait.setter
    def isp_wait(self, value):
        if value < 0:
            raise Exception('invalid time')
        self._isp_wait = value

    @property
    def login_id(self):
        raise Exception('cannot show login id (confidential)')

    @login_id.setter
    def login_id(self, value):
        self._login_id = value

    @property
    def password(self):
        raise Exception('cannot show password (confidential)')

    @password.setter
    def password(self, value):
        self._password = value

    def login(self):
        try:
            if requests.get(self.url, verify=False, timeout=3).status_code is not requests.codes.ok:
                raise Exception('error: ' + str(requests.get(self.url).raise_for_status()))
        except requests.exceptions.ConnectTimeout:
            # with open('logout_details.txt', 'a') as record:
            #     sys.stdout = record
            #     print('Already logged in')
            return
        except requests.exceptions.ConnectionError:
            # with open('logout_details.txt', 'a') as record:
            #     sys.stdout = record
            #     print('no response form ISP')
            time.sleep(self.connection_wait)
            self.login()
            return
        # with open('logout_details.txt', 'a') as record:
        #     sys.stdout = record
        #     print('opening web-page for login')
        self.driver = webdriver.Firefox()
        self.driver.get(self.url)
        username = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, self.usernameID)))
        username.send_keys(self.id)
        password = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, self.passwordID)))
        password.send_keys(self.password)
        login_button = WebDriverWait(self.driver, 5). \
            until(EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "' + self.loginValue + '")]')))
        login_button.click()
        self.quit()

    @staticmethod
    def default_value(attrib):
        if attrib is 'url':
            return 'http://192.168.1.1/redirect'
        elif attrib is 'usernameID':
            return 'username'
        elif attrib is 'passwordID':
            return 'password'
        elif attrib is 'loginValue':
            return 'Login'
        else:
            raise Exception('invalid parameter')

    @staticmethod
    def get_ssid():
        """
        :return:
        SSID of current wireless network
        """
        ssid = os.popen('iwgetid -r').read()[:-1]
        # print('SSID: ' + ssid)
        return ssid

    def quit(self):
        self.driver.quit()
        if os.path.isfile('/home/manthan/PycharmProjects/IP_connector/details.json'):
            return
        else:
            with open('/home/manthan/PycharmProjects/IP_connector/details.json', 'w') as file:
                data = {
                    'url': self.url,
                    'usernameID': self.usernameID,
                    'id': self.id,
                    'passwordID': self.passwordID,
                    'password': self.password,
                    'loginName': self.loginValue,
                }
                data = {
                    self.ssid: data
                }
                json.dump(data, file, indent=4)
