#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author: Jiang Liu<jiang.liu@yottaa.com>
#date: 2014-1-14
from __future__ import division
try:
    import json
except ImportError:
    import simplejson as json
import os
import re
from zabbix_socket_sender import Zabbix
from zabbix_function import *

def varnishstat():

    data = {}
    status = os.popen("varnishstat -j").read()
    for key,value in json.loads(status).iteritems():
        if re.match('(timestamp|VBE)',key):
            continue
        data[key] = int(value["value"])
    data["cache_hit_ratio"] = "%3.2f" % float(int(data["cache_hit"])/(int(data["cache_hit"])+int(data["cache_miss"])))
    return data

def push_data():

    host = os.popen("cat /etc/company.facts |grep publicip |awk '{print $3}'").read().strip()
    #varnish statists
    lbdata = varnishstat() 
    #GC times and max gc time
    lbdata['gc_times'] = gc_status()['times']
    lbdata['gc_maxtime'] = gc_status()['maxtime']
    lbdata['adn_timestamp_diff'] = check_adn_timestamp()
    hostvalues = {host:lbdata}
    Zabbix(hostvalues).run()

if __name__ == "__main__":
    #varnishstat()
    push_data()