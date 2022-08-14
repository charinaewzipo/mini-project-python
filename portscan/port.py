import socket
import os
from pip._vendor import requests
import time
from configparser import ConfigParser
socket.setdefaulttimeout(.5)





## line notify
def notifyNetwork(hostname,status):
    token="IOmu1Lm2i1XbR9GxYlksAJIqw5hfhqn19ABKgUWpGgp"
    uri="https://notify-api.line.me/api/notify"
    header = {"Authorization":"Bearer "+token_line}
    msg={"message":"เซิฟเวอร์ IP "+hostname+" "+status}
    resp= requests.post(uri,headers=header,data=msg)


def port_check(ip,port):

    DEVICE_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result_of_check = DEVICE_SOCKET.connect_ex((ip,port))

    if result_of_check == 0:
       print(str(ip)+" is Listening on Port "+ str(port))
       #notifyNetwork(str(ip),'is Listening on Port ',str(port))
       DEVICE_SOCKET.close()
    else:
       print(str(ip)+" is not Listening on Port "+ str(port))
       notifyNetwork(str(ip),'is not Listening on Port ',str(port))
       DEVICE_SOCKET.close()

config_object = ConfigParser()
config_object.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
serverinfo = config_object["server"]

hostname = list()
hostname=serverinfo["ipaddr"]
hostname_list=hostname.split(",")

lineinfo = config_object["line"]
token_line= lineinfo["token"]


## loop time 1 min
starttime = time.time()
while True: 
    for i in hostname_list:
        text=i.split(":")
        x=text[0]
        y=text[1]
        port_check(x,int(y))
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))    
