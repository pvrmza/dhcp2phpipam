#!/usr/bin/python
__author__ = 'pvrmza'
author_email = 'pvr.mza@gmail.com',

import sys
import requests 
import json
import datetime

### Parameters ###
phpipam_url = 'https://phpipam.local'
api_id = 'your_api_name'
api_token = 'your_api_key'
base_url = phpipam_url + "/api/" + api_id +"/";

#### FUNCTIONS ###
def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
#--------------------------------------
def find_addressId(base_url,api_token,ip,silence=1):
    if silence == 0: print("Finding address...")
    res = requests.get(base_url + "addresses/search/" + ip + "/", headers={'token': api_token})
    if res.ok:
        result = res.json()
        if 'data' in result:
            data = json.loads(res.content)['data']
            ipId=data[0]['id']
            subnetId=data[0]['subnetId']

            if silence == 0: print("IP: %s - id %s - subnetId %s" % (ip, ipId, subnetId))
            return ipId, subnetId
        else:
            if silence == 0: print ("Address not found")
            return "0", "0"
    else:
        if silence == 0: print ("error")
        return "0", "0"
#--------------------------------------
def delete_address(base_url,api_token,ip,silence=1):
    if silence == 0: print("Find address...")
    ipId, subnetId = find_addressId(base_url,api_token,ip,silence)
    if ipId != "0":
        if silence == 0: print("Deleting address...")
        if silence == 0: print("IP: %s - id %s - subnetId %s" % (ip, ipId, subnetId))
        res = requests.delete(base_url + "addresses/" + ipId + "/", headers={'token': api_token})
        if res.ok: print ("Delete OK")
        else: print("HTTP-D %i - %s, Message %s" % (res.status_code, res.reason, res.text))     
    else:
         print ("Address not found - No delete")      
#--------------------------------------
def add_address(base_url,api_token,ip,mac,hostname="",router=0,silence=1):
    if silence == 0: print("Find network...")
    if router != "0":
        routerIpId, subnetId = find_addressId(base_url,api_token,router,silence)
    else:
        print ("aun no soportado")
        exit(2)
        #ipId, subnetId = find_addressId(base_url,api_token,router,silence)

    now=str(datetime.datetime.now())

    if silence == 0: print("Find host...")
    hostIpId, hostSubnetId = find_addressId(base_url,api_token,ip,silence)
    
    if hostIpId == "0" :
        if silence == 0: print("Host not found... adding")
        # add
        DATA={"subnetId":subnetId, "ip": ip, "hostname":hostname, "mac":mac, "lastSeen":now }
        res = requests.post(base_url + "addresses/", headers={'token': api_token}, json=DATA)
        if res.ok: print ("Added OK")
        else: print("HTTP-I %i - %s, Message %s" % (res.status_code, res.reason, res.text))
    else:
        if silence == 0: print("Host found... updating")
        # update
        DATA={"hostname":hostname, "mac":mac, "lastSeen":now }
        res = requests.patch(base_url + "addresses/" + hostIpId + "/", headers={'token': api_token}, json=DATA)
        if res.ok: print ("Update OK")
        else: print("HTTP-U %i - %s, Message %s" % (res.status_code, res.reason, res.text))
#-------------------------------------
def update_address(base_url,api_token,ip,mac,hostname="",silence=1):
    if silence == 0: print("Find host...")
    hostIpId, hostSubnetId = find_addressId(base_url,api_token,ip,silence)
    if hostIpId == "0" :
        if silence == 0: 
            print("Host not found... exit")
            exit(2)
    else:
        if silence == 0: print("Host found... updating")
        # update
        DATA={"hostname":hostname, "mac":mac, "lastSeen":now }
        res = requests.patch(base_url + "addresses/" + hostIpId + "/", headers={'token': api_token}, json=DATA)
        if res.ok: print ("Update OK")
        else: print("HTTP-U %i - %s, Message %s" % (res.status_code, res.reason, res.text))
    

#-------------------------------------

len_options=len(sys.argv)-1
if len_options > 0 :
    action=str(sys.argv[1])

    if action == "add" :
        if len_options < 4 :
            exit(2)
        # ejecutar delete
        hostIp=str(sys.argv[2])
        hostMac=str(sys.argv[3])
        hostName=str(sys.argv[4])
        if len_options == 5 : 
            hostGw=str(sys.argv[5])
        else:
            hostGw="0"

        add_address(base_url, api_token,hostIp,hostMac,hostName,hostGw,1)

    elif action == "update" :
        if len_options < 3 :
            print "action 'del' need IP addresses to delete"
            exit(2)
        # ejecutar delete
        hostIp=str(sys.argv[2])
        hostMac=str(sys.argv[3])
        hostName=str(sys.argv[4])

        update_address(base_url, api_token,hostIp,hostMac,hostName,1)

    elif action == "del" :
        if len_options < 2 :
            print "action 'del' need IP addresses to delete"
            exit(2)
        # ejecutar delete
        hostIp=str(sys.argv[2])
        delete_address(base_url, api_token,hostIp, 1)
    else:
        print "las opciones son add o del"

else:
    print "mete bien los dedos"
