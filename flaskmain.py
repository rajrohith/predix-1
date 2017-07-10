from flask import Flask
import os
import json
from app.dbConnection import OptimaDb

app = Flask(__name__)
log = app.logger
username=""
password=""
dbinstance=""
hostname=""

# Get port from environment variable or choose 9099 as local default
port = int(os.getenv("PORT", 9099))
#optimadb=OptimaDb(username,password,dbinstance,hostname)


if 'VCAP_SERVICES' in os.environ:
	vcapdata= json.loads(os.getenv('VCAP_SERVICES'))
	username=vcapdata['postgres'][0]['credentials']['username']
	password=vcapdata['postgres'][0]['credentials']['password']
	hostname=vcapdata['postgres'][0]['credentials']['host']
	dbinstance=vcapdata['postgres'][0]['credentials']['database']

@app.route('/')
def hello_world():
#	app.response("db-initate",mimetype='text/html')
	print "I am here"
# 	optimadb=OptimaDb(username,password,dbinstance,hostname)
#	app.logger.info(optimadb.execute(dbscript/date.sql))
#	app.logger.info(' database error')
	print " I am here ..."	
#	app.response("db instance name "+ dbinstance, mimetype='text/html')
 	return 'Hello World! I am instance ' + str(os.getenv("CF_INSTANCE_INDEX", 0) + hostname )

if __name__ == '__main__':
    # Run the app, listening on all IPs with our chosen port number
    app.run(host='0.0.0.0', port=port)
