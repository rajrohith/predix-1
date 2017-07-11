# optima_file_service_poc

The following repo is a poc of creating postgres table on a cf enviornment. The sql scripts are stored under
dbscripts. The python script reads the sql script and execute the script on a cf instance. 

Following are the commands to test if you modify any code

Once you modified your code, commit the code to the git hub
Once commited, do 

cf push

Since this is an python flask based webapp. It will create a url on the cf space. To get the url, login to the cloudfoundry  space

cf a

the sample output will be like 

name                                        requested state   instances   memory   disk   urls

hello-service                               started           1/1         1G       1G     hello-service-sandbox.run.aws-usw02-pr.ice.predix.io

optima-file-service                         started           1/1         128M     256M   optima-file-service-immaterial-smirk.run.aws-usw02-pr.ice.predix.io

pg-optima-sandbox                           started           1/1         1G       1G     pg-optima-sandbox.run.aws-usw02-pr.ice.predix.io

RadouaneElberrak-Predix-HelloWorld-WebApp   started           1/1         256M     1G     radouaneelberrak-predix-helloworld-webapp.run.aws-usw02-pr.ice.predix.io


As per the mainfest file, the cf push , the optima-file-service to the cf enviornment. On you browser, if you open
optima-file-service-immaterial-smirk.run.aws-usw02-pr.ice.predix.io

Then as part of the root "/" context , the python based postgres tables will be created. 

To see the tables and values, use the following link

https://pg-optima-sandbox.run.aws-usw02-pr.ice.predix.io/

The userid, password and dbinstance name will be displayed as part of the root "/" response on the browser.

Issues:
* Python print command is not updating any output to the cf log
* Need to convert the python script to create the tables during the initialization of the python flask. Not when someone 
click on the browser.
