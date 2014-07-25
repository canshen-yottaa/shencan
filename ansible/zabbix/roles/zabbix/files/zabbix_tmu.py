#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author: Jiang Liu<jiang.liu@yottaa.com>
#date: 2014-3-27
try:
    import json
except ImportError:
    import simplejson as json
import os,commands
from zabbix_socket_sender import Zabbix

data = {}

def dns_health():
    
    status = commands.getstatusoutput('dig +time=3 +tries=3 +noall +answer @127.0.0.1 system.topology.tpu.yottaa.net >/dev/null 2>&1')
    data['dns_health'] = int(status[0])
    return data

def push_data():

    host = os.popen("cat /etc/company.facts |grep publicip |awk '{print $3}'").read().strip()
    TMUdata = dns_health()
    hostvalues = {host:TMUdata}
    Zabbix(hostvalues).run()

if __name__ == "__main__":

    push_data()