"""
Overloading 'print()'
"""
import sys


def print_record(string):
    with open('logout_details.txt', 'a') as record:
        stdout = sys.stdout
        sys.stdout = record
        print(string, end='')
        sys.stdout = stdout
    return
