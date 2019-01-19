#!/usr/bin/env python3

from IP_Connector import networkSupervisor
from IP_Connector import ip_connector
import os
from IP_Connector.print_record import print_record


if __name__ == '__main__':
    ip_connector = ip_connector.IpConnector()
    print_record('created Ip connector\n')
    supervisor = networkSupervisor.NetworkSupervisor(ip_connector)
    print_record('starting surveillance\n')
    supervisor.start_surveillance()




