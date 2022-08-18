import requests
import json
import urllib3
from pathlib import Path
from time import sleep
from ipaddress import IPv4Network

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

####### Option load:
optionFile = Path(__file__).parent / './options.json'
with open(optionFile, "rb") as opt:
    options = json.load(opt)['firepower']
    USERNAME = options['username']
    PASSWORD = options['password']
    FDM = options['address']
    ROUTE = options['failover_route']
    GATEWAY = options['failover_gateway']
    FO_INTERFACE = options['failover_interface']
#######

oauth_data = {
    "grant_type": "password",
    "username": USERNAME,
    "password": PASSWORD
}

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
baseurl = "https://" + FDM + "/api/fdm/latest"


class FirePower():

    def __init__(self):
        # Set up HTTP session & get auth token / virtual router ID
        with requests.Session() as self.s:
            self.token = self.authRequest()
            self.getGlobalVR()
