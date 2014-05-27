#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
import urllib 
import json
import requests
def lists():
    data_center={'us-west':02,'ap-southeast':04,'us-east':01,'eu-west':03,'us-chicago':'08','us-miami':'09'}
    url = "http://monitor.yottaa.com:8000/api/instance/instances/?format=json&limit=0&production_state=1"
    r = requests.get(url, auth=('api', 'AtynccSCifmmgIoR'))
    data_string= json.loads(r.text)
    r = {}
    for item in data_string['objects']:
        group = item['data_center'] 
        itype = item['public_ip']
        if group in r:
            r[group].append(item['hostname'])
        else:
            r[group]=[item['hostname']]
    hosts_dict = dict()
    for i in r:
       cpis={}
       hostlist=r[i]
       cpis["hosts"]=hostlist
       r[i]=cpis
       hostlist=r[i]["hosts"]
       children=[]
       for host in hostlist:
          host_list = list()
          itype=host.split("-")[1]
          iadd = i.lower()
          zu = str(iadd + '@' + itype.lower())
          if itype in host:
              host_list.append(host)
          if zu not in hosts_dict.keys():
              hosts_dict[zu] = host_list
          else:
              hosts_dict[zu].extend(host_list)
          children.append(zu)
          children = list(set(children))
    r[i]["children"] = children
    r = dict(r.items()+hosts_dict.items());
    return json.dumps(r,indent=4)
    

def hosts(name):
    url = "http://monitor.yottaa.com:8000/api/instance/instances/?format=json&limit=0&production_state=1&hostname=%s" % name
    r = requests.get(url, auth=('api', 'AtynccSCifmmgIoR'))
    data_string= json.loads(r.text)
    result = data_string['objects'][0]
    ip= result['public_ip']
    user='yadmin'
    k='/Users/shencan/Downloads/key.pub'
    r = {'ansible_ssh_host': ip}
    n = {'ansible_user': user }
    key ={'ansible_ssh_private_key_file': k }
    cpis=dict(r.items()+n.items()+key.items())
    return json.dumps(cpis)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list', help='hosts list', action='store_true')
    parser.add_argument('-H', '--host', help='hosts vars')
    args = vars(parser.parse_args())

    if args['list']:
        print lists()
    elif args['host']:
        print hosts(args['host'])
    else:
        parser.print_help()
