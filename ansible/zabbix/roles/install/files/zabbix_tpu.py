#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author: Jiang Liu<jiang.liu@yottaa.com>
#date: 2014-1-14
from zabbix_socket_sender import Zabbix
from zabbix_function import *


def push_data():

    tpudata = {}
    host = os.popen("cat /etc/company.facts |grep publicip |awk '{print $3}'").read().strip()
    #varnish statists
    tpudata['adn_timestamp_diff'] = check_adn_timestamp()
    hostvalues = {host:tpudata}
    Zabbix(hostvalues).run()

if __name__ == "__main__":
    #varnishstat()
    push_data()