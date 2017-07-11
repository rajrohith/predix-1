#import requests
import ftplib

user_data={'username':'rshanmugamgeog','password':'1TDPpew'}

ftp= ftplib.FTP("fileshare.drillinginfo.com","2121")
ftp.login("rshanmugamgeog","rshanmugamgeog")
ftp.retrlines('LIST')
ftp.quit()