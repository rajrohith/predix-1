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
	username=vcapdata['postgres'][0]['credentials']['username']
	password=vcapdata['postgres'][0]['credentials']['password']
	hostname=vcapdata['postgres'][0]['credentials']['uri']
	dbinstance=vcapdata['postgres'][0]['credentials']['database']

@app.route('/')
def hello_world():
	global message, conn
	dbcreate("dbscript/date.sql",hostname)	
 	return 'Hello World! I am instance ' + str(os.getenv("CF_INSTANCE_INDEX", 0) + hostname +"---"+message)

def dbConnect(uri):
		global message, conn
		print(uri)
		try:
			message="In OptimaDb class"
			conn = psycopg2.connect(uri)
		except:
			message="Unable to connect to database"
		return conn.cursor()	

def dbcreate(filename,uri):
	global message, conn
	cur=dbConnect(uri)
	cur.execute(open(filename,"r").read())
	cur.close()
	conn.commit()

if __name__ == '__main__':
    # Run the app, listening on all IPs with our chosen port number
    app.run(host='0.0.0.0', port=port)
