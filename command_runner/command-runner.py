import json
import os
import sys
import netmiko


parmfile = 'hosts.json'
commandfile = 'commands.txt'

user = 'usr'
passw = 'pwd'

def main():
	print 'Parsing parameter file'
	params = json.load(open(parmfile))
	
	print 'Parsing commands file'
	file = open(commandfile, "r")
	commands = file.read().splitlines()
	
	for param in params:
		hostname = param['hostname']
		print 'Strating config runner for: ' + hostname
		connect = netmiko.ConnectHandler(device_type='cisco_ios', ip=param['mgmt_ip'], username=user, password=passw, global_delay_factor= 2)
		connect.config_mode()
		if connect.check_config_mode() == True:
			print connect.send_config_set(commands)
			print 'Commands done for: ' + hostname
		else:
			print 'Could not enter config mode'
			
		connect.disconnect()
		
	print 'Completed'

if __name__ == '__main__':
	sys.exit(main())