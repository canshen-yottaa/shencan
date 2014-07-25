#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author: Jiang Liu<jiang.liu@yottaa.com>
#date: 2014-3-28
#desc: get curren tcp statists
try:
    import json
except ImportError:
    import simplejson as json
import sys,os,re
from zabbix_socket_sender import Zabbix

data = {}
tcp_status = ["ERROR_STATUS","TCP_ESTABLISHED","TCP_SYN_SENT","TCP_SYN_RECV","TCP_FIN_WAIT1","TCP_FIN_WAIT2","TCP_TIME_WAIT",\
                "TCP_CLOSE","TCP_CLOSE_WAIT","TCP_LAST_ACK","TCP_LISTEN","TCP_CLOSING"]

def get_tcp_statists():

    statists = os.popen('cat /proc/net/tcp |awk -F " " \'{print $4}\' |sort |uniq -c |sort -n -r').readlines()
    for code in statists:
        code_name = code_to_name(code.split()[1])
        data[code_name] = int(code.split()[0])
    #print data
    return fill_nodata_zero(data)

def code_to_name(code):

    code_name = "UNKNOW"

    if code == "00":
        code_name = "ERROR_STATUS"
    elif code == "01":
        code_name = "TCP_ESTABLISHED"
    elif code == "02":
        code_name = "TCP_SYN_SENT"
    elif code == "03":
        code_name = "TCP_SYN_RECV"
    elif code == "04":
        code_name = "TCP_FIN_WAIT1"
    elif code == "05":
        code_name = "TCP_FIN_WAIT2"
    elif code == "06":
        code_name = "TCP_TIME_WAIT"
    elif code == "07":
        code_name = "TCP_CLOSE"
    elif code == "08":
        code_name = "TCP_CLOSE_WAIT"
    elif code == "09":
        code_name = "TCP_LAST_ACK"
    elif code == "0A":
        code_name = "TCP_LISTEN"
    elif code == "0B":
        code_name = "TCP_CLOSING"

    return code_name

def fill_nodata_zero(data):
    for code in tcp_status:
        if data.has_key(code):
            continue
        else:
            data[code]=0
    return data

def push_data():

    host = os.popen("cat /etc/company.facts |grep publicip |awk '{print $3}'").read().strip()
    tcpData = get_tcp_statists()
    hostvalues = {host:tcpData}
    Zabbix(hostvalues).run()

if __name__ == "__main__":

    # get_tcp_statists()
    push_data()
