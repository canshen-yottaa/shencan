#!/usr/bin/python
import cPickle as p
import json
f = file('test1')
storedlist = p.load(f)
datacen=[]
for x in storedlist:
    datacen.append(x.lower())
hosts_dict={}
for line in storedlist:
    group=[]
    print '=' * 40 + line.lower() + '=' * 40
    print '[' + line.lower() + ':children]'
    for host in  storedlist[line]:
        host_list= []
        itype=host.split("-")[1]
        iadd = line.lower()
        zu = str(iadd + '@' + itype.lower())
        group.append(zu)
        jb= list(set(group))
        if itype in host:
              host_list.append(host)
        if zu not in hosts_dict.keys():
              hosts_dict[zu] = host_list
        else:
              hosts_dict[zu].extend(host_list)
    for i in jb:
        print i
    for i in jb:
        print '[' +  i  + ']'
        for xx in hosts_dict[i]:
            ipadd=xx.split('-')[-1]
            print "%s  ansible_ssh_host=%s ansible_ssh_user=yadmin" % ( xx, ipadd )
    print '=' * 40 + line.lower() + '=' * 40
