# dhcp2phpipam
A Python interface to manage IP addresses in phpIPAM through REST API, with integration to ISC-DHCP

phpIPAM is an open-source web IP address management application. Its goal is to provide light and simple IP address management application.

Site: [phpIPAM homepage](http://phpipam.net)

![phpIPAM logo](http://phpipam.net/wp-content/uploads/2014/12/phpipam_logo_small.png)


# Usage
## Add IP Adreess
```bash
	./dhcp2phpipam.py add ClientIP ClientDHCID ClientName RouterIP
```
Where: 
* ClientIP : Host IP address
* ClientDHCID : Host MAC Address
* ClientName : Hostname 
* RouterIP : `RouterIP` is required to determine the subnet in which the `ClientIP` should be added. `ClientIP` is added on the same subnet where `RouterIP` is located. It can be the IP of the gateway of the subnet or some other reference IP in that subnet

## Update IP Adreess
```bash
	./dhcp2phpipam.py update ClientIP ClientDHCID ClientName
```
## Delete IP Adreess
```bash
	/dhcp2phpipam.py del ClientIP
```


# Installation with ISC-DHCP in Ubuntu

1. Install packages
```bash
	pip install requests
```
or 
```bash
	sudo apt update && sudo apt install python-requests libssl-dev
```
2. Create directory `/etc/dhcp/dhcpd-hooks.d/` 

3. Download and copy [`dhcp2phpipam.py`](https://raw.githubusercontent.com/pvrmza/dhcp2phpipam/master/dhcp2phpipam.py) in `/etc/dhcp/dhcpd-hooks.d/`

4. Edit `dhcp2phpipam.py` and set phpIPAM url, api name and api token
```python
	phpipam_url = 'https://phpipam.local'
	api_id = 'your_api_name'
	api_token = 'your_api_key'
```
5. Set execute permission on `dhcp2phpipam.py`
```bash
	chmod +x `/etc/dhcp/dhcpd-hooks.d/dhcp2phpipam.py`
```

6. Download and copy [`usr.sbin.dhcpd`](https://raw.githubusercontent.com/pvrmza/dhcp2phpipam/master/usr.sbin.dhcpd) in: `/etc/apparmor.d/local/` and restart apparmor service

7. Create directory `/etc/dhcp/dhcpd.conf.d/`

8. Download and copy [`dhcpd-event.conf`](https://raw.githubusercontent.com/pvrmza/dhcp2phpipam/master/dhcpd-event.conf) in `/etc/dhcp/dhcpd.conf.d/`

9. Edit `/etc/dhcp/dhcpd.conf` and include `dhcpd-event.conf` with trigers update
```bash
	include "/etc/dhcp/dhcpd.conf.d/dhcpd-event.conf";
```
10. Restart DHCP Server

11. Enjoy


# Other API clients
- https://github.com/adzhurinskij/phpipam-client
- https://github.com/adzhurinskij/phpipam-api-pythonclient (only Python 2.7)
- https://github.com/efenian/phpipamsdk
- https://github.com/michaelluich/phpIPAM
