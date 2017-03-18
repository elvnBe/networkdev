import json
import os
import sys
import datetime
import requests
from openpyxl import Workbook

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
			deviceparams = {'hostname' : device['hostname'], 'location' : device['snmpLocation'], 'serialnumber' : device['serialNumber'], 'platform' : device['platformId'], 'software' : device['softwareVersion']}
			devicecollection.append(deviceparams)

	return devicecollection

def main():
	date = str(now.day) + '-' + str(now.month) + '-' + str(now.year)
	book = Workbook()
	sheet = book.active
	
	print 'Create APIC-EM ticket'
	ticket = create_token(apicuri)
	print 'Ticket Created'
	print 'Request Devices Info'
	devicesinfo = get_devices_info(ticket, apicuri)
	
	for info in devicesinfo:
		row = (info['hostname'], info['location'], info['serialnumber'], info['platform'], info['software'])
		sheet.append(row)

	book.save(filedir + 'inventory.xlsx')
	print 'Completed'

if __name__ == '__main__':
	sys.exit(main())