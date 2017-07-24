from flask import Flask
from tqdm import tqdm
import os
import json
from app.dbConnection import OptimaDb
import psycopg2
import requests
import urllib2
import urlparse
from boto.s3.connection import S3Connection


app = Flask(__name__)
log = app.logger
username=""
password=""
dbinstance=""
hostname=""
conn=""
message=""
dmessage=""
tabledatalist=[["dimingredient.sql","DIMIngredient_Table.txt"],["dimpurpose.sql","DIMPurpose_Table.txt"],
				["dimsupplier.sql","DIMSupplier_Table.txt"],["dimtrade.sql","DIMTrade_Table.txt"]]
tabledata=""
tablename=""
appfolder=""
fileshareurl="http://fileshare.drillinginfo.com/"
URLPATHS=["DI%20Analytics%20Core%20-%0A%20Delaware%20Basin/Core/DelawareBasin_Permit_20170712.zip"]
access_key=""
secret_access_key=""
bucket_name=""
s3_host=""
blob_url="https://raj-drillinginfo-upload.run.aws-usw02-pr.ice.predix.io/blob/"


headers = {
    'authorization': 'Basic cnNoYW5tdWdhbWdlb2c6MVREUHBldw==',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'postman-token': '691681df-6679-a786-69bb-826b1e39eb7a',
}

download_command=[
  ('command', 'download'),
 ] 

# Get port from environment variable or choose 9099 as local default
port = int(os.getenv("PORT", 9099))
#optimadb=OptimaDb(username,password,dbinstance,hostname)


if 'VCAP_SERVICES' in os.environ:
	vcapdata= json.loads(os.getenv('VCAP_SERVICES'))
#	username=vcapdata['postgres'][0]['credentials']['username']
#	password=vcapdata['postgres'][0]['credentials']['password']
	hostname=vcapdata['postgres-2.0'][0]['credentials']['uri']
	access_key=vcapdata['predix-blobstore'][0]['credentials']['access_key_id']
	secret_access_key=vcapdata['predix-blobstore'][0]['credentials']['secret_access_key']
	bucket_name=vcapdata['predix-blobstore'][0]['credentials']['bucket_name']
	s3_host=vcapdata['predix-blobstore'][0]['credentials']['host']
	appfolder="/app/"
else:
	hostname="postgres://postgres:postgres@localhost:5432/postgres?sslmode=disable"	
#	dbinstance=vcapdata['postgres'][0]['credentials']['database']

@app.route('/')
def file_service():
	global message, conn , tabledata ,tablename
	try:
		for root,directory,files in os.walk("dbscript"):
			message=message+"<br> In file "+str(files)+"</br>"
			for filename in files:
				tabledata=dataFile(filename)
				tablename=filename.strip(".sql")
				filepath = os.path.join(root, filename)
				print(filepath)
				message=message+"<br> In file "+str(filepath)+"</br>"
				dbcreate(str(filepath),hostname)	
	except Exception as e:
		message=message+"<br> error:"+ str(e)+"</br>"
		pass
 	return (hostname +"<br>---"+message)


@app.route('/download')
def file_download():
	global dmessage
	try:
		print("In route download")
		for urlPath in URLPATHS:
			urlDownload(urlPath)
	except Exception as e:
		dmessage=dmessage+str(e)		
	return (dmessage)	
#def hello_world():
#	global message, conn
#	dbcreate("dbscript/date.sql",hostname)	
# 	return 'Hello World! I am instance ' + str(os.getenv("CF_INSTANCE_INDEX", 0) + hostname +"---"+message)

@app.route('/s3')
def s3_bucket():
	print("In s3")
	try:
		message=listS3()
	except Exception as e:
		return(str(e))	
	return (message)

def dataFile(tablename):
	datadict=dict(tabledatalist)
	return datadict[tablename]

def dbConnect(uri):
		global message, conn
		print(uri)
		try:
			
			conn = psycopg2.connect(uri)
		except Exception as e:
			message=message+"<br>Unable to connect to database"+str(e)+"</br>"
			pass
		return conn.cursor()	

def dbcreate(filename,uri):
	global message, conn
#	SET client_encoding = 'ISO_8859_5';
	
	try:
		cur=dbConnect(uri)
		print("----------------------")
		sqlfile=open(filename,"r")
		sqllines=sqlfile.read()
		sqlcommands = sqllines.split(';')

		for sqlstatement in sqlcommands:
			print("executing:"+sqlstatement)
			if not sqlstatement.strip():
				print ("debug:empty string")
			else:
				cur.execute(sqlstatement)
				print ("Done")
		cur.close()
		conn.commit()
		print("Dump data")	
	#	dumpData(uri)
		dumpBolbData(uri)
		dropTable(uri)
		renameTable(uri)
		
	except Exception as e:
		message=message+"<br> error:"+ str(e)+"</br>"
		pass

def dropTable(uri):
	global message, conn, tabledata , tablename
	cur=dbConnect(uri)
	command = "DROP TABLE IF EXISTS "+ "public."+tablename+";"
	message=message+"Dropping existing table public."+tablename+"  </br>"
	try:
		cur.execute(command)
		cur.close()
		conn.commit()	
	except Exception as e:
		message=message+"<br> DROP TABLE error:"+ str(e)+"</br>"
		pass

def renameTable(uri):
	global message, conn, tabledata , tablename
	cur=dbConnect(uri)
	command = "ALTER TABLE temp_"+tablename+" RENAME TO "+tablename+";"
	message=message+"Rename table public."+tablename+"  </br>"
	try: 
			cur.execute(command)
			cur.close()
			conn.commit()	
	except Exception as e:
		message=message+"<br> RENAME TABLE error:"+ str(e)+"</br>"
		pass		

def dumpData(uri):
	global message, conn, tabledata , tablename, appfolder
	cur=dbConnect(uri)
	copy_command = "COPY "+ "public.temp_"+tablename+" FROM STDIN DELIMITER '|' NULL AS ''  CSV HEADER ENCODING 'WINDOWS-1251';"
	message=message+"Dumping data to public."+tablename+"from file "+ tabledata+" </br>"
	try: 
		with open(appfolder+"dbdata/"+tabledata,'r') as f:
			print(copy_command)
			cur.copy_expert(sql=copy_command, file=f)
			cur.close()
			conn.commit()	
			print("inside data copy")
	except Exception as e:
		message=message+"<br> dump data error:"+ str(e)+"</br>"
		pass

def dumpBolbData(uri):
	global message, conn, tabledata , tablename, appfolder
	cur=dbConnect(uri)
	copy_command = "COPY "+ "public.temp_"+tablename+" FROM STDIN DELIMITER '|' NULL AS ''  CSV HEADER ENCODING 'WINDOWS-1251';"
	message=message+"Dumping data to public."+tablename+"from file "+ tabledata+" </br>"
	try: 	
		print(blob_url+tabledata)
		download_blob(blob_url+tabledata)
		with open(tabledata,'r') as f:
			print(copy_command)
			cur.copy_expert(sql=copy_command, file=f)
			cur.close()
			conn.commit()	
			print("inside data copy")
	except Exception as e:
		message=message+"<br> dump data error:"+ str(e)+"</br>"
		pass		

def download_file(url, desc=None):
    u = urllib2.urlopen(url)

    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
    filename = os.path.basename(path)
    if not filename:
        filename = 'downloaded.file'
    if desc:
        filename = os.path.join(desc, filename)

    with open(filename, 'wb') as f:
        meta = u.info()
        meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
        meta_length = meta_func("Content-Length")
        file_size = None
        if meta_length:
            file_size = int(meta_length[0])
        print("Downloading: {0} Bytes: {1}".format(url, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)

            status = "{0:16}".format(file_size_dl)
            if file_size:
                status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
            status += chr(13)
            print(status)
        print()

    return filename

def download_blob(url):
	local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
	r = requests.get(url, stream=True)
	with open(local_filename, 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024): 
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastia
	return local_filename
    

def urlDownload(path):
	global dmessage,headers,download_command
	dfilename=os.path.basename(path)
	dmessage=dmessage+dfilename
	data = [
  			('command', 'download'),
  			('path', '%2FDI%2520Analytics%2520Core%2520-%2520Delaware%2520Basin%2FCore%2FDelawareBasin_Permit_20170712.zip'),
			]
	print("In urldownload")
	dresponse=requests.post('http://fileshare.drillinginfo.com/', headers=headers, data=data,stream=True)
	dmessage=dmessage+str(dresponse)
#	dresponse = requests.get(fileshareurl+path, headers=headers, data=download_command,stream=True)
	with open(dfilename, "wb") as handle:
		for data in tqdm(dresponse.iter_content()):
#			print(data)
			handle.write(data)

def listS3():
	global access_key, secret_access_key, bucket_name
	try:
		conn = S3Connection(access_key,secret_access_key)
		bucket = conn.get_bucket(bucket_name)
		for key in bucket.list():
			print(key.name.encode('utf-8'))
	except Exception as e:
		return(str(e))		
	return("success")	


if __name__ == '__main__':
    # Run the app, listening on all IPs with our chosen port number
    app.run(host='0.0.0.0', port=port)
