#!/usr/bin/env python3


# developed by Gabi Zapodeanu, TSA, GPO, Cisco Systems


import json

import requests
import urllib3
from requests.auth import HTTPBasicAuth  # for Basic Auth
from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings

from config import DNAC_URL, DNAC_PASS, DNAC_USER

urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings

DNAC_AUTH = HTTPBasicAuth(DNAC_USER, DNAC_PASS)


def pprint(json_data):
    """
    Pretty print JSON formatted data
    :param json_data: data to pretty print
    :return:
    """
    print(json.dumps(json_data, indent=4, separators=(' , ', ' : ')))


def get_dnac_jwt_token(dnac_auth):
    """
    Create the authorization token required to access Cisco DNA C
    Call to Cisco DNA C - /api/system/v1/auth/login
    :param dnac_auth - Cisco DNA C Basic Auth string
    :return: Cisco DNA C JWT token
    """

    url = DNAC_URL + '/api/system/v1/auth/login'
    header = {'content-type': 'application/json'}
    response = requests.get(url, auth=dnac_auth, headers=header, verify=False)
    response_header = response.headers
    dnac_jwt_token = response_header['Set-Cookie']
    return dnac_jwt_token

def get_client_info(client_ip, dnac_jwt_token):
    """
    This function will retrieve all the information from the client with the IP address
    :param client_ip: client IPv4 address
    :param dnac_jwt_token: Cisco DNA C token
    :return: client info, or {None} if client does not found
    """
    url = DNAC_URL + '/api/v1/host?hostIp=' + client_ip
    header = {'content-type': 'application/json', 'Cookie': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    client_json = response.json()
    try:
        client_info = client_json['response'][0]
        return client_info
    except:
        return None


# get the Cisco DNA Center JWT auth

dnac_jwt_auth = get_dnac_jwt_token(DNAC_AUTH)
print('The Cisco DNA Center Auth JWT is: ', dnac_jwt_auth)

# get the client info

client_ip_add = '10.93.130.34'
client_detail = get_client_info(client_ip_add, dnac_jwt_auth)
print('The information for the client with the IP address: ', client_ip_add)
pprint(client_detail)

