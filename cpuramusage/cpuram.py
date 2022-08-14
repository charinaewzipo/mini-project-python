#!/usr/bin/env python3
"""
Test program with functions for monitoring CPU and RAM usage in Python with PsUtil.
"""
__docformat__ = 'reStructuredText'

import os
import psutil
import sys
from psutil._common import bytes2human
from pip._vendor import requests
import time
from configparser import ConfigParser
import time


def main():
    # Output current CPU usage as a percentage
    print('CPU usage is {} %'.format(get_cpu_usage_pct()))
    if get_cpu_usage_pct() > int(cpu_usage):
        notifyCPU(hostname,str(get_cpu_usage_pct()))
    # Output current CPU frequency in MHz.
    print('CPU frequency is {} MHz'.format(get_cpu_frequency()))
    # Output current CPU temperature in degrees Celsius
    #print('CPU temperature is {} degC'.format(get_cpu_temp()))
    # Output current RAM usage in MB
    print('RAM usage is {} MB'.format(int(get_ram_usage() / 1024 / 1024)))
    
    # Output total RAM in MB
    print('RAM total is {} MB'.format(int(get_ram_total() / 1024 / 1024)))
    # Output current RAM usage as a percentage.
    print('RAM usage is {} %'.format(get_ram_usage_pct()))
    if get_ram_usage_pct()  > int(ram_usage):
        notifyRAM(hostname,str(get_ram_usage_pct()))
    # Output current Swap usage in MB
    print('Swap usage is {} MB'.format(int(get_swap_usage() / 1024 / 1024)))
    # Output total Swap in MB
    print('Swap total is {} MB'.format(int(get_swap_total() / 1024 / 1024)))
    # Output current Swap usage as a percentage.
    print('Swap usage is {} %'.format(get_swap_usage_pct()))
    # Output Disk device
    print(get_disk())


    
hostname = list()
config_object = ConfigParser()
config_object.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
serverinfo = config_object["server"]
hostname=serverinfo["ipaddr"]

lineinfo = config_object["line"]
token_line= lineinfo["token"]

deviceinfo = config_object["device"]
cpu_usage=deviceinfo["cpu_usage"]
ram_usage=deviceinfo["ram_usage"]
disk_usage=deviceinfo["disk_usage"]

loopinfo = config_object["loop"]
status_loop =loopinfo["status"]
time_loop =loopinfo["time"]

    
## line notify
def notifyCPU(hostname,status):
    #token="IOmu1Lm2i1XbR9GxYlksAJIqw5hfhqn19ABKgUWpGgp"
    uri="https://notify-api.line.me/api/notify"
    header = {"Authorization":"Bearer "+token_line}
    msg={"message":"เซิฟเวอร์ IP "+hostname+" CPU usage is "+status+"%"}
    resp= requests.post(uri,headers=header,data=msg)
def notifyRAM(hostname,status):
    #token="IOmu1Lm2i1XbR9GxYlksAJIqw5hfhqn19ABKgUWpGgp"
    uri="https://notify-api.line.me/api/notify"
    header = {"Authorization":"Bearer "+token_line}
    msg={"message":"เซิฟเวอร์ IP "+hostname+" RAM usage is "+status+"%"}
    resp= requests.post(uri,headers=header,data=msg)
def notifyDisk(hostname,disk,status):
    #token="IOmu1Lm2i1XbR9GxYlksAJIqw5hfhqn19ABKgUWpGgp"
    uri="https://notify-api.line.me/api/notify"
    header = {"Authorization":"Bearer "+token_line}
    msg={"message":"เซิฟเวอร์ IP "+hostname+" Device "+disk +" usage is "+status+"%"}
    resp= requests.post(uri,headers=header,data=msg)

def get_cpu_usage_pct():
    """
    Obtains the system's average CPU load as measured over a period of 500 milliseconds.
    :returns: System CPU load as a percentage.
    :rtype: float
    """
    return psutil.cpu_percent(interval=0.5)


def get_cpu_frequency():
    """
    Obtains the real-time value of the current CPU frequency.
    :returns: Current CPU frequency in MHz.
    :rtype: int
    """
    return int(psutil.cpu_freq().current)


def get_cpu_temp():
    """
    Obtains the current value of the CPU temperature.
    :returns: Current value of the CPU temperature if successful, zero value otherwise.
    :rtype: float
    """
    # Initialize the result.
    result = 0.0
    # The first line in this file holds the CPU temperature as an integer times 1000.
    # Read the first line and remove the newline character at the end of the string.
    if os.path.isfile('/sys/class/thermal/thermal_zone0/temp'):
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            line = f.readline().strip()
        # Test if the string is an integer as expected.
        if line.isdigit():
            # Convert the string with the CPU temperature to a float in degrees Celsius.
            result = float(line) / 1000
    # Give the result back to the caller.
    return result


def get_ram_usage():
    """
    Obtains the absolute number of RAM bytes currently in use by the system.
    :returns: System RAM usage in bytes.
    :rtype: int
    """
    return int(psutil.virtual_memory().total - psutil.virtual_memory().available)


def get_ram_total():
    """
    Obtains the total amount of RAM in bytes available to the system.
    :returns: Total system RAM in bytes.
    :rtype: int
    """
    return int(psutil.virtual_memory().total)


def get_ram_usage_pct():
    """
    Obtains the system's current RAM usage.
    :returns: System RAM usage as a percentage.
    :rtype: float
    """
    return psutil.virtual_memory().percent


def get_swap_usage():
    """
    Obtains the absolute number of Swap bytes currently in use by the system.
    :returns: System Swap usage in bytes.
    :rtype: int
    """
    return int(psutil.swap_memory().used)


def get_swap_total():
    """
    Obtains the total amount of Swap in bytes available to the system.
    :returns: Total system Swap in bytes.
    :rtype: int
    """
    return int(psutil.swap_memory().total)


def get_swap_usage_pct():
    """
    Obtains the system's current Swap usage.
    :returns: System Swap usage as a percentage.
    :rtype: float
    """
    return psutil.swap_memory().percent

def get_disk():
    templ = "%-17s %8s %8s %8s %5s%% %9s  %s"
    print(templ % ("Device", "Total", "Used", "Free", "Use ", "Type",
                   "Mount"))
    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt':
            if 'cdrom' in part.opts or part.fstype == '':
                # skip cd-rom drives with no disk in it; they may raise
                # ENOENT, pop-up a Windows GUI error for a non-ready
                # partition or just hang.
                continue
        usage = psutil.disk_usage(part.mountpoint)
        print(templ % (
            part.device,
            bytes2human(usage.total),
            bytes2human(usage.used),
            bytes2human(usage.free),
            int(usage.percent),
            part.fstype,
            part.mountpoint))
        if usage.percent > int(disk_usage):    
            notifyDisk(hostname,part.device,str(usage.percent))

if __name__ == "__main__":
    starttime = time.time()
    while True: 
        main()
        if status_loop == 'yes':
            time.sleep(int(time_loop) - ((time.time() - starttime) % 60.0))
        else:
            exit()    