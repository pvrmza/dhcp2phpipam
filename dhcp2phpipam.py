import requests 
import json
import datetime

### Parameters ###
phpipam_url = 'https://phpip.local'
api_id = 'dhcp'
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
def add_address(base_url,api_token,ip,hostname,mac,router=0,silence=1):
    if silence == 0: print("Find network...")
    if router != "0":
        routerIpId, subnetId = find_addressId(base_url,api_token,router,silence)
    else:
        print ("aun no soportado")
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
        else: print("HTTP-I %i - %s, Message %s" % (res.status_code, res.reason, res.text))


    
    
#delete_address(base_url, api_token,"192.168.2.211", 0)
#add_address(base_url, api_token,"192.168.2.211","SCT-INF-E01","30:9c:23:02:16:93","192.168.2.249", 0)

