from flask import Flask
import os
import json
from app.dbConnection import OptimaDb
import psycopg2


app = Flask(__name__)
log = app.logger
username=""
password=""
dbinstance=""
hostname=""
conn=""
message=""

# Get port from environment variable or choose 9099 as local default
port = int(os.getenv("PORT", 9099))
#optimadb=OptimaDb(username,password,dbinstance,hostname)


if 'VCAP_SERVICES' in os.environ:
	vcapdata= json.loads(os.getenv('VCAP_SERVICES'))
#	username=vcapdata['postgres'][0]['credentials']['username']
#	password=vcapdata['postgres'][0]['credentials']['password']
	hostname=vcapdata['postgres'][0]['credentials']['uri']
else:
	hostname="postgres://postgres:postgres@localhost:5432/postgres?sslmode=disable"	
#	dbinstance=vcapdata['postgres'][0]['credentials']['database']

@app.route('/')
def file_service():
	global message, conn
	try:
		for root,directory,files in os.walk("dbscript"):
			message=message+"<br> In file "+str(files)+"</br>"
			for filename in files:
				
				filepath = os.path.join(root, filename)
				print(filepath)
				message=message+"<br> In file "+str(filepath)+"</br>"
				dbcreate(str(filepath),hostname)	
	except Exception as e:
		message=message+"<br> error:"+ str(e)+"</br>"
		pass
 	return (hostname +"<br>---"+message)

#def hello_world():
#	global message, conn
#	dbcreate("dbscript/date.sql",hostname)	
# 	return 'Hello World! I am instance ' + str(os.getenv("CF_INSTANCE_INDEX", 0) + hostname +"---"+message)

def dbConnect(uri):
		global message, conn
		print(uri)
		try:
			message=message+"In OptimaDb class</br>"
			conn = psycopg2.connect(uri)
		except Exception as e:
			message=message+"<br>Unable to connect to database"+str(e)+"</br>"
			pass
		return conn.cursor()	

def dbcreate(filename,uri):
	global message, conn
	try:
		cur=dbConnect(uri)
		print("----------------------")
		sqlfile=open(filename,"r")
		sqllines=sqlfile.read()
		sqlcommands = sqllines.split(';')

		for sqlstatement in sqlcommands:
			print(sqlstatement)
			cur.execute(sqlstatement)
		cur.close()
		conn.commit()
	except Exception as e:
		message=message+"<br> error:"+ str(e)+"</br>"
		pass

if __name__ == '__main__':
    # Run the app, listening on all IPs with our chosen port number
    app.run(host='0.0.0.0', port=port)
