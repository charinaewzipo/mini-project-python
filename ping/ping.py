import os
from pip._vendor import requests
import time
from configparser import ConfigParser

hostname = list()
config_object = ConfigParser()
config_object.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
serverinfo = config_object["server"]
hostname=serverinfo["ipaddr"]
hostname_list = hostname.split(",")

lineinfo = config_object["line"]
token_line= lineinfo["token"]

def checkNetwork(hostname):
    response = os.system("ping ", "-c ", "3 " + hostname)
    if response == 0:
        #notifyNetwork(hostname,'Up')
        pingstatus = 'Network Up'
    else:
        notifyNetwork(hostname,'Down')
        pingstatus = 'Network Down'
    return pingstatus


## line notify
def notifyNetwork(hostname,status):
    #token=""
    uri="https://notify-api.line.me/api/notify"
    header = {"Authorization":"Bearer "+token_line}
    msg={"message":"เซิฟเวอร์ IP "+hostname+" "+status}
    resp= requests.post(uri,headers=header,data=msg)


## loop time 1 min
starttime = time.time()
while True: 
    for i in hostname_list:
        print(checkNetwork(i))
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))    