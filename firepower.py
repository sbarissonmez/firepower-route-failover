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

    def authRequest(self):
        # Authenticate to FDM and retrieve token
        authurl = baseurl + "/fdm/token"
        print("Posting AUTH request to FDM")
        resp = self.s.post(authurl, headers=headers,
                           data=json.dumps(oauth_data),
                           verify=False)
        if resp.status_code == 200:
            print("Auth success - got token.")
            return json.loads(resp.text)['access_token']
        else:
            print("Authentication Failed.")
            print(resp.text)

    def getGlobalVR(self):
        # Grab list of virtual routers
        print("Pulling list of virtual routers...")
        vr_url = "/devices/default/routing/virtualrouters"
        resp = self.getData(vr_url)
        # Parse for Global virtual router
        print("Got virtual routers - finding global vrouter...")
        vrouters = json.loads(resp)['items'][0]
        if vrouters['name'] == "Global":
            print("Got Global routing table, ID: " + vrouters['id'])
            self.globalVR = vrouters["id"]
