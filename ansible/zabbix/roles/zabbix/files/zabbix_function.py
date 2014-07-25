#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author: Jiang Liu<jiang.liu@yottaa.com>
#date: 2014-1-14

import subprocess
def gc_status():

    status = {} # Times:   Max:
    script = '''
        gc_logfile=$(ls -r /data1/log/router/gc* | grep -v 'offset' | head -1)
        sudo /usr/sbin/logtail $gc_logfile | 2>/dev/null \
        awk 'BEGIN {Times=0; Max=0}
            {if ($0 ~ "Total time for which application threads were stopped") {
                Times++
                TimeTaken=1000 * $(NF-1)
                Max=TimeTaken>Max?TimeTaken:Max
                }
            } END {print Times":"Max}'
    '''
    gc_status = subprocess.Popen(script,shell=True,stdout=subprocess.PIPE)
    #print gc_status.communicate()
    value = gc_status.communicate()[0].strip().split(":")
    status['times'] = int(value[0])
    status['maxtime'] = float(value[1])
    return status

def check_adn_timestamp():

    status = {}
    script = '''
        hosts[0]="b235587061bb012f3565123138132fe0.yottaa.net"
        hosts[1]="ea6eaa2061bb012fd2461231380b8e8c.yottaa.org"
        hosts[2]="4f24b600d49e012f2b2e12313b0451c1.yottaa.info"
        for ((x=0; x<${#hosts[@]}; x++))
        do
            timestamp=$(java -jar /opt/monitor/bin/cmdline-jmxclient-0.10.3.jar zenoss:eWgPagd7vXif7mrZVsLS 127.0.0.1:8877 yottaa:type=AdnService getAdnTimeStamp=${hosts[$x]} 2>&1|awk -F': ' '{print $NF}')
            sys_timestamp=$(date +%s)
            if [ $timestamp -gt 0 ];then
                adn_timestamp=${timestamp%???}
                offset_timestamp=$[ ${sys_timestamp} - ${adn_timestamp} ]
                echo ${offset_timestamp}
            fi
        done
    '''
    timestamp = subprocess.Popen(script,shell=True,stdout=subprocess.PIPE).communicate()[0]
    if len(timestamp) <1:
        timestamp == 0
    return timestamp

if __name__ == "__main__":

    pass
    #print gc_status()