"""
Ip connector class
"""
import json
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import os
import time
from IP_Connector.PrintRecord import print_record


class IpConnector(object):

    def __init__(self):
        self.ssid = self.get_ssid()
        self._isp_wait = 10
        self._login_id = None
        self._password = None
        self._driver = None
        self._login_details = 'details.json'
        self._record = 'logout_details.txt'

        try:
            self._load_details(self._login_details)
        except FileNotFoundError:
            pass
        self._open_record(self._record)

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

    @property
    def login_details(self):
        return self._login_details

    @login_details.setter
    def login_details(self, path):
        self._login_details = path

    @property
    def record(self):
        return self._record

    @record.setter
    def record(self, path):
        self._record = path

    def login(self):
        redirect_url = 'http://192.168.1.1/redirect'

        try:
            request = requests.get(redirect_url, verify=False, timeout=3)
            if request.status_code is not requests.codes.ok:
                try:
                    request.raise_for_status()
                except requests.exceptions.HTTPError:
                    print_record('Bad request \n')
                    return
        except requests.exceptions.ConnectTimeout:
            print_record('Already logged in \n')
            return
        except requests.exceptions.ConnectionError:
            time.sleep(self.isp_wait)
            self.login()
            return

        self._driver = webdriver.Firefox()
        self._driver.get(redirect_url)
        username = WebDriverWait(self._driver, 3).until(ec.presence_of_element_located((By.ID, 'username')))
        username.send_keys(self._login_id)
        password = WebDriverWait(self._driver, 3).until(ec.presence_of_element_located((By.ID, 'password')))
        password.send_keys(self._password)
        login_button = WebDriverWait(self._driver, 3). \
            until(ec.presence_of_element_located((By.XPATH, '//button[contains(text(), "Login")]')))
        login_button.click()
        self._quit()

    @staticmethod
    def get_ssid():
        ssid = os.popen('iwgetid -r').read()[:-1]
        return ssid

    def _quit(self):
        self._driver.quit()

        try:
            details = open(self._login_details, 'r')
            data = json.load(details)
            details.close()
        except FileNotFoundError:
            data = None

        with open(self._login_details, 'w') as details:
            if not data:
                data = {}
            data[self.ssid] = {
                'id': self._login_id,
                'password': self._password,
            }
            json.dump(data, details, indent=4)
