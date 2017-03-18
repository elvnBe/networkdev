import json
import os
import sys
import netmiko
import datetime

filedir = 'C:\\Users\\win7-2\\Desktop\\files\\'

parmfile = 'hosts.json'

now = datetime.datetime.now()
user = 'user'
passw = 'pwd'

def main():
	print 'Parsing parameter file'
	params = json.load(open(parmfile))
	
	for param in params:
		hostname = param['hostname']
		date = str(now.day) + '-' + str(now.month) + '-' + str(now.year)
		hour = str(now.hour) + ':' + str(now.minute)
		print 'Strating backup of switch: ' + hostname
		filename = hostname + '_' + date + '.txt'
		connect = netmiko.ConnectHandler(device_type='cisco_ios', ip=param['mgmt_ip'], username=user, password=passw, global_delay_factor= 2) 
		output = connect.send_command('show run')
		file = open(filedir + filename, "w")
		file.write('------------------------------------------------------------------' + '\n' + 'Switch: ' + hostname + '\n' + 'Time of backup: ' + date + ' ' + hour + '\n' + '------------------------------------------------------------------' + '\n')
		file.write(output)
		file.close()
		connect.disconnect()

	print 'Completed'

if __name__ == '__main__':
	sys.exit(main())