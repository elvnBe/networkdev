import json
import os
import sys
import netmiko
import datetime
import requests

# Disable warnings (if certificate validation is disabled)
requests.packages.urllib3.disable_warnings()

filedir = 'C:\\Users\\win7-2\\Desktop\\files\\'
now = datetime.datetime.now()
user = 'admin'
passw = 'C1sco12345'
apicserver = '198.18.129.100'

apicuri = 'https://' + apicserver + '/api/v1'

def create_token (uri):
	apicall = '/ticket'
	contents = {'username' : user , 'password' : passw}
	header = {'content-type': 'application/json'}
	
	#construct URL
	uri += apicall

	#make API call (do not validate SSL certificate)
	response = requests.post(uri, data=json.dumps(contents), headers=header, verify=False).json()
	
	#return the service ticket number
	return response["response"]["serviceTicket"]

def get_devices_info (ticket, uri):
	deviceparams = {}
	devicecollection = []
	apicall = '/network-device'
	header = {'content-type': 'application/json', 'X-AUTH-TOKEN': ticket}
	
	#construct URL
	uri += apicall

	#make API call (do not validate SSL certificate)
	response = requests.get(uri, headers=header, verify=False).json()
	for device in response['response']:
		if device['reachabilityStatus'] == 'Reachable' and device['family'] == 'Switches and Hubs':
			deviceparams = {'id' : device['id'], 'hostname' : device['hostname']}
			devicecollection.append(deviceparams)

	return devicecollection

def get_device_config (ticket, uri, id):
	apicall = '/network-device/' + id + '/config'
	header = {'content-type': 'application/json', 'X-AUTH-TOKEN': ticket}

	#construct URL
	uri += apicall

	#make API call (do not validate SSL certificate)
	response = requests.get(uri, headers=header, verify=False).json()
	
	return response

def main():
	date = str(now.day) + '-' + str(now.month) + '-' + str(now.year)
	print 'Create APIC-EM ticket'
	ticket = create_token(apicuri)
	print 'Ticket Created'
	print 'Request Devices Info'
	devicesinfo = get_devices_info(ticket, apicuri)

	for info in devicesinfo:
		print 'Starting backup of: ' + info['hostname']
		config = get_device_config (ticket, apicuri, info['id'])
		filename = info['hostname'] + date + '.txt'
		file = open(filedir + filename, "w")
		file.write(config['response'])
		file.close()

	print 'Completed'

if __name__ == '__main__':
	sys.exit(main())