'''
This is main module which runs whole application.
'''

import sys

import requests

from main.model import Division

APP_NAME = 'main.py'
DIVISION_REQUEST_URL = 'http://www.cbf.cz/xml/api/divs.php'

def print_usage(argv):
    print("usage: {} cbf-phase".PHASE_REQUEST_URLformat(APP_NAME))

def main(argv):
    if len(argv) <= 1:
        print_usage(argv)
        exit(1)

    phase = argv[1]

    params = {'json' : 1, 'season' : 2017, 'female' : 0}
    r = requests.get(DIVISION_REQUEST_URL, params)
    json_dict = r.json()

    divisions = []
    for div in json_dict:
        divisions.append(Division(**div))

    d = divisions[0]

    division = Division(2343)

    print(d)



if __name__ == '__main__':
    main(sys.argv)