#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 20:58:48 2017

@author: RajkumarShanmugam
"""

from flask import Flask
#   from tqdm import tqdm
import os
import json
import sys
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
#tabledatalist=[["dimingredient.sql","DIMIngredient_Table.txt"],["dimpurpose.sql","DIMPurpose_Table.txt"],
#               ["dimsupplier.sql","DIMSupplier_Table.txt"],["dimtrade.sql","DIMTrade_Table.txt"],
#               ["date.sql","Date_Table.txt"],["factdisclosuredetail.sql","FACTDisclosureDetail_Table.txt"],
#               ["factjobdetail.sql","FactjobDetail_Table.txt"],["dimdiwellheadermaster.sql","DIMDIWellHeaderMaster_Table.txt"],
#               ["topingredientsusedforeachpurpose.sql","TopIngredientsUsedForEachPurpose_Table.txt"],
#               ["purposerollup.sql","PurposeRollUp_Table.txt"],["dimdiscloure.sql","DIMDisclosure_Table.txt"]]
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


def throws():
    raise RuntimeError('loading fail .. please check the file and table')

download_command=[
  ('command', 'download'),
 ] 

# Get port from environment variable or choose 9099 as local default
port = int(os.getenv("PORT", 9099))
#optimadb=OptimaDb(username,password,dbinstance,hostname)


if 'VCAP_SERVICES' in os.environ:
    vcapdata= json.loads(os.getenv('VCAP_SERVICES'))
#   username=vcapdata['postgres'][0]['credentials']['username']
#   password=vcapdata['postgres'][0]['credentials']['password']
    hostname=vcapdata['postgres-2.0'][0]['credentials']['uri']
    access_key=vcapdata['predix-blobstore'][0]['credentials']['access_key_id']
    secret_access_key=vcapdata['predix-blobstore'][0]['credentials']['secret_access_key']
    bucket_name=vcapdata['predix-blobstore'][0]['credentials']['bucket_name']
    s3_host=vcapdata['predix-blobstore'][0]['credentials']['host']
    appfolder="/app/"
else:
    hostname="postgres://postgres:postgres@localhost:5432/postgres?sslmode=disable" 
#   dbinstance=vcapdata['postgres'][0]['credentials']['database']

@app.route('/')
def file_service():
    global message, conn , tabledata ,tablename
    try:
        for root,directory,files in os.walk("dbscript"):
            message=message+"<br> In file "+str(files)+"</br>"
            for filename in files:
                filepath = os.path.join(root, filename)
                print(filepath)
                message=message+"<br> In file "+str(filepath)+"</br>"
                dbcreate(str(filepath),hostname)
        dumpdata(hostname)          
    except (Exception, psycopg2.DatabaseError) as e:
        message=message+"<br> error:"+ str(e)+"</br>"
        raise
    return (hostname +"<br>---"+message)                                         
                            
def dbConnect(uri):
        global message, conn
        print(uri)
        try:
            
            conn = psycopg2.connect(uri)
        except (Exception, psycopg2.DatabaseError) as e:
            message=message+"<br>Unable to connect to database"+str(e)+"</br>"
            sys.exit(1)
        return conn.cursor()    

def dumpdata(uri):
    global message, conn
    try:
        print("Dump data")  
        #   dumpData(uri)
        with open("./conf/tabledatalist.txt","r") as handle:
            for line in handle:
                tablename, tabledata = line.rstrip('\n').split(',')     
                dumpBolbData(uri,tablename,tabledata)
                throws()
    except (Exception, psycopg2.DatabaseError) as e:
        message = message+"<br> dumpdata:"+ str(e)+"</br>"
        raise
        
    
def dbcreate(filename,uri):
    global message, conn
#   SET client_encoding = 'ISO_8859_5';
    
    try:
        cur=dbConnect(uri)
        print("----------------------")
        sqlfile=open(filename,"r")
        sqllines=sqlfile.read()
        sqlcommands = sqllines.split(';')

        for sqlstatement in sqlcommands:
            if not sqlstatement.strip():
                print ("debug:empty string")
            else:
                sqlstatement=' '.join(sqlstatement.split("  "))
                print("executing:"+sqlstatement)
                cur.execute(sqlstatement)
                print ("Done")
        cur.close()
        conn.commit()   
    except (Exception, psycopg2.DatabaseError) as e:
        print(str(e))
        message=message+"<br> error:"+ str(e)+"</br>"
        pass
        
def dropTable(uri,tablename):
    global message, conn
    cur=dbConnect(uri)
    command = "DROP TABLE IF EXISTS "+ "public."+tablename+";"
    message=message+"Dropping existing table public."+tablename+"  </br>"
    try:
        cur.execute(command)
        cur.close()
        conn.commit()   
    except (Exception, psycopg2.DatabaseError) as e:
        message=message+"<br> DROP TABLE error:"+ str(e)+"</br>"
        sys.exit(1)

def renameTable(uri,tablename):
    global message, conn
    cur=dbConnect(uri)
    command = "ALTER TABLE temp_"+tablename+" RENAME TO "+tablename+";"
    message=message+"Rename table public."+tablename+"  </br>"
    try: 
            cur.execute(command)
            cur.close()
            conn.commit()   
    except (Exception, psycopg2.DatabaseError) as e:
        message=message+"<br> RENAME TABLE error:"+ str(e)+"</br>"
        sys.exit(1) 
        
def dumpBolbData(uri,tablename,tabledata):
    global message, conn, appfolder
    cur=dbConnect(uri)
    copy_command = "COPY "+ "public.temp_"+tablename+" FROM STDIN DELIMITER ',' NULL AS ''  CSV HEADER ENCODING 'WINDOWS-1251';"
    message=message+"Dumping data to public."+tablename+"from file "+ tabledata+" </br>"
    try:    
        print(blob_url+tabledata+".csv")
        delFile(tabledata+".csv")
        download_blob(blob_url+tabledata+".csv")
        with open(tabledata+".csv",'r') as f:
            print(copy_command)
            cur.copy_expert(sql=copy_command, file=f)
            cur.execute("SELECT * FROM public.temp_"+tablename)
            count= cur.rowcount
            print ("row count"+count)
            if count > 0 :
                print ("Data loaded succuessfully"+tablename)
                dropTable(uri,tablename)
                renameTable(uri,tablename)
                cur.close()
                conn.commit()   
                print("inside data copy")
            else:
                print ("Data is not loaded successfully !!" +tablename)

    except (Exception, psycopg2.DatabaseError) as  e:
           print("check the error table " +tablename +"and file name " +tabledata +"!!!")
           message=message+"<br> dump data error:"+ str(e)+"</br>"
           pass

def download_blob(url):
    global message

    try:
        local_filename = url.split('/')[-1]
        print("Starting to download file"+local_filename)
    # NOTE the stream=True parameter
        r = requests.get(url, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastia
    except Exception as e:
        message=message+"<br> download blob:"+ str(e)+"</br>"
        pass
        print ("---***---Download completed----***----")        
        return local_filename

def delFile(filename):
    global message
    try:
        os.remove(filename)
    except Exception as e:
        message=message+"<br> delete Filename:"+ str(e)+"</br>"
        pass    

    
if __name__ == '__main__':
    # Run the app, listening on all IPs with our chosen port number
    app.run(host='0.0.0.0', port=port)