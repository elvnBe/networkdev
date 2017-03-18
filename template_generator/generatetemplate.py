import jinja2
import json
import os
import sys

template_file = 'template-v1.j2'
common_paramfile = 'common_params.json'
specific_paramfile = "specific_params.json"
filedir = 'C:\\Users\\win7-2\\Desktop\\files\\'

#module to merge 2 dictinaries
def dict_merge(dict1, dict2):
	result = dict1.copy()
	result.update(dict2)
	return result

def main():
	#read the parameter file
	print 'Parsing parameter files'
	params_specific = json.load(open(specific_paramfile))
	params_common = json.load(open(common_paramfile))

	#Create jinja2 environment
	print 'create Jinja2 env'
	env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="."),trim_blocks=True,lstrip_blocks=True)
	template = env.get_template(template_file)

	print "Generating Configurations"
	for param in params_specific:
		print 'Generating configuration for: ' + param['hostname'] + ' -- Serial: ' + param['serial']  
		params_all = dict_merge(param, params_common)
		filename = param['hostname'] + '_generated.conf'
		output = template.render(params_all)
		file = open(filedir + filename, "w")
		file.write(output)
		file.close()

	print 'Completed'

if __name__ == '__main__':
	sys.exit(main())