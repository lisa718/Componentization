import os
import ConfigParser
import optparse
import subprocess

def get_svn_info():
	try:
		command = 'svn info'
		result = subprocess.check_output(command,shell=True)
	except:
		result = ""
	return result

def parse_svn_info(svn_info_string):
	info_dic = {}
	info_str_list = svn_info_string.split("\n")
	for info_str in info_str_list:
		info_list = info_str.split(":", 1)
		if len(info_list) > 0:
			if len(info_list[0]) >0: 
			    info_dic[info_list[0]] = info_list[1]
	return info_dic

def save_to_file(file_name, md5):
	cf = ConfigParser.ConfigParser()

	if os.path.exists(file_name):
		cf.read(file_name)
	else:
		cf.add_section("info")

	svn_info = get_svn_info()
	info_dic = parse_svn_info(svn_info)

	cf.set("info", "svn_version", info_dic["Revision"])
	cf.set("info", "svn_path", info_dic["Relative URL"])
	cf.set("info", "lib_md5", md5)
	cf.set("info", "distr_version", "")
	cf.set("info", "desc", "")
	cf.write(open(file_name, "w"))


if __name__ == '__main__':
    
    parser = optparse.OptionParser()

    parser.add_option("-f", "--file", dest="file",
                      help="target file")

    parser.add_option("-m", "--md5", dest="md5",
                      help="md5 for target file")

    (options, args) = parser.parse_args()
    if options.file is not None and options.md5 is not None:
        save_to_file(options.file, options.md5)
    else:
        parser.print_help()