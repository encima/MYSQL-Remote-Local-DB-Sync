from ConfigParser import *
import sys
import os

class RDS_Backup:
	def backup(self, path):
		conf = ConfigParser()
		conf.read(path)
		sections =  conf.sections()
		local = {}
		remote = {}
		for section in sections:
			options  = conf.options(section)
			for opt in options:
				if section == "Local":
					try:
						local[opt] = conf.get(section, opt)					
					except:
						print "Error reading %s" % opt
						local[opt] = -1
				elif section == "Remote":
					try:
						remote[opt] = conf.get(section, opt)
					except:
						print "Error reading %s" % opt
						remote[opt] = -1
		return local, remote

#May get around to implementing reading the config file into here at some point
class DB:
	def __init__(self, user, passwd, host, db, local):
		self.user = user
		self.passwd = passwd
		self.host = host
		self.db = db
		self.local = local 
	
	def __repr__(self):
		print 'DB - User: %s, Pass: %s, Host: %s, db'
		
rds = RDS_Backup()
local, remote = rds.backup(sys.argv[1])
if sys.argv[2] == 'local2remote':
	cmd = """mysqldump --user={0} --password={1} {2} > rds.sql |
	mysql --user={3} --pass={4} --host={5} {6} < rds.sql""".format(local['user'], local['password'], local['db'], remote['user'], remote['password'], remote['host'], remote['db'])
	print cmd
	os.system(cmd)
elif sys.argv[2] == 'remote2local':
	cmd = """mysqldump --host={0} --user={1} --password={2} {3} > rds.sql |
	mysql --user={4} --pass={5} {6} < rds.sql""".format(remote['host'], remote['user'], remote['password'], remote['db'], local['user'], local['password'], local['db'])
	print cmd
	os.system(cmd)
else:
	print 'Usage rds_backup.py {config_path} local2remote | rds_backup.py {config_path} remote2local'



