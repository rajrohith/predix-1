import psycopg2

class OptimaDb(object):
	"""docstring for OptimaDb"""
	def __init__(self, userid,passwd,dbinstance,hostname):
		super(OptimaDb, self).__init__()
		self.userid = userid
		self.passwd = passwd
		self.dbinstance = dbinstance
		self.hostname = hostname

	def dbConnect():
		try:
			print "In OptimaDb class"
			conn = psycopg2.connect("dbname=self.dbinstance user=self.userid host=self.hostname password=self.password")
		except:
			print "Unable to connect to database"
		return conn.cursor()
	
	def execute(filename):
		cur = dbConnect()
		cur.execute(open(filename,"r").read())