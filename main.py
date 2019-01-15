#!/usr/bin/env python3
import ipCon
import autoConnector
import sys
import os

if __name__ == '__main__':
    try:
        os.remove('/home/manthan/PycharmProjects/IP_connector/logout_details.txt')
    except FileNotFoundError:
        pass
    sys.stdout = open('/home/manthan/PycharmProjects/IP_connector/logout_details.txt', 'w')
    connector = ipCon.IpConnector(id='ravi61', password='mamta267')
    autoCon = autoConnector.autoConnect(connector)
    autoCon.surveillance()




