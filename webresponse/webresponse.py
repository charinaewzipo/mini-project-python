import os
from pip._vendor import requests
import time
from configparser import ConfigParser


hostname = list()
config_object = ConfigParser()
config_object.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
serverinfo = config_object["web"]
hostname=serverinfo["url"]
hostname_list = hostname.split(",")

lineinfo = config_object["line"]
token_line= lineinfo["token"]

## line notify
def notifyNetwork(hostname,status):
    #token="IOmu1Lm2i1XbR9GxYlksAJIqw5hfhqn19ABKgUWpGgp"
    uri="https://notify-api.line.me/api/notify"
    header = {"Authorization":"Bearer "+token_line}
    msg={"message":"เซิฟเวอร์ IP "+hostname+" "+status}
    resp= requests.post(uri,headers=header,data=msg)


## loop time 1 min
starttime = time.time()
while True: 
    for i in hostname_list:
        x = requests.get(i)
        print(i +' <Response> ' +str(x.status_code))
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))    