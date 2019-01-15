#!/usr/bin/env python3
from IP_Connector import networkSupervisor
from IP_Connector import ipCon
import os

if __name__ == '__main__':
    try:
        if os.stat('login_details.txt').st_size >= 1000000000:
            os.remove('logout_details.txt')
    except FileNotFoundError:
        pass

    ip_connector = ipCon.IpConnector(login_id='ravi61', password='mamta267')
    autoCon = networkSupervisor.NetworkSupervisor(ip_connector)
    autoCon.start_surveillance()




