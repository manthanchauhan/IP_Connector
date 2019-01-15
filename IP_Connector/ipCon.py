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


class IpConnector(object):
    def __init__(self,
                 login_id=None,
                 password=None,
                 connection_error_sleep=10
                 ):
        self.ssid = self.get_ssid()
        self.connection_error_sleep = connection_error_sleep

        try:
            with open('details.json', 'r') as details:
                data = json.load(details)
                if self.ssid not in data.keys():
                    raise FileNotFoundError
                if login_id:
                    self.id = login_id
                else:
                    self.id = data[self.ssid]['id']
                if password:
                    self.password = password
                else:
                    self.password = data[self.ssid]['password']
                self.url = data[self.ssid]['url']
                self.usernameID = data[self.ssid]['usernameID']
                self.passwordID = data[self.ssid]['passwordID']
                self.loginValue = data[self.ssid]['loginName']

        except FileNotFoundError:
            if any((login_id, password)) is None:
                raise Exception('id or password not provided')
            self.id = login_id
            self.password = password
            self.url = self.default_value('url')
            self.usernameID = self.default_value('usernameID')
            self.passwordID = self.default_value('passwordID')
            self.loginValue = self.default_value('loginValue')

        self.driver = None

    def login(self):
        try:
            if requests.get(self.url, verify=False, timeout=3).status_code is not requests.codes.ok:
                raise Exception('error: ' + str(requests.get(self.url).raise_for_status()))
        except requests.exceptions.ConnectTimeout:
            # print('Already logged in')
            return
        except requests.exceptions.ConnectionError:
            time.sleep(self.connection_error_sleep)
            self.login()
            return

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
