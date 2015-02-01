#!/usr/bin/python
import json
import requests
import argparse
import sys

def startinfo():
    print '\033[1;31;40m'
    print '=' * 52
    print '\tQuery Resource management system Info\t'
    print '*ENVIRONMENT:\t',args['environment']
    print '*ROLE:\t\t',args['role']
    print '*ATTRIBUTE:\t',args['attribute']
    print '*DATACENTER:\t',args['datacenter']
    print '*HOST:\t',args['Host']
    print '=' * 52
    print '\033[0m'
def endinfo(sum):
    print '\033[1;31;40m'
    print '=' * 52
    print '\tQuery number is\t', sum
    print '=' * 52
    print '\033[0m'

def listtype(a,b,c='public_ip'):
      url = "http://monitor.yottaa.com:8000/XXXXX/instance/instances/?format=json&limit=0&production_state=%d&role=%d" %  (a,b)
      r = requests.get(url, auth=('XXXXX', 'XXXXXXXXX'))
      data_string= json.loads(r.text)
      lx=c
      sum=0
      for ip in data_string["objects"]:
         sum = sum +1
         print ip[lx]
      endinfo(sum)

def listall(a,c='public_ip'):
      url = "http://XXXXXXXX:8000/XXXXX/instance/instances/?format=json&limit=0&production_state=%d" %  a
      r = requests.get(url, auth=('XXXXX', 'XXXXXXXXX'))
      data_string= json.loads(r.text)
      type=c
      sum=0
      for ip in data_string["objects"]:
          sum = sum + 1
          print ip[type]
      endinfo(sum)

def hosts(a):
    url = "http://XXXXX:8000/XXXXX/instance/instances/?format=json&limit=0&hostname=%s" % a
    r = requests.get(url, auth=('XXXXX', 'XXXXXXXXX'))
    data_string= json.loads(r.text)
    result = data_string['objects']
    print '\033[1;31;40m'
    print '=' * 52
    print '\tQuery  infomation for\t', args['Host']
    print '=' * 52
    print '\033[0m'
    print json.dumps(result,indent=4)

def yid(a):
    url = "http://XXXXXX:8000/XXXXX/instance/instances/?format=json&limit=0&yid=%s" % a
    r = requests.get(url, auth=('XXXXX', 'XXXXXXXXX'))
    data_string= json.loads(r.text)
    result = data_string['objects']
    print '\033[1;31;40m'
    print '=' * 52
    print '\tQuery  infomation for\t', args['yid']
    print '=' * 52
    print '\033[0m'
    print json.dumps(result,indent=4) 

def ip(a):
    url = "http://XXXXXX:8000/XXXXX/instance/instances/?format=json&limit=0&public_ip=%s" % a
    r = requests.get(url, auth=('XXXXX', 'XXXXXXXXX'))
    data_string= json.loads(r.text)
    result = data_string['objects']
    print '\033[1;31;40m'
    print '=' * 52
    print '\tQuery  infomation for\t', args['ip']
    print '=' * 52
    print '\033[0m'
    print json.dumps(result,indent=4)

def datacenter(a,b,c="hostname"):
    url = "http://XXXXXXXX:8000/XXXXX/instance/instances/?format=json&limit=0&production_state=%s&data_center=%s" % (a,b)
    r = requests.get(url, auth=('XXXXX', 'XXXXXXXXX'))
    data_string= json.loads(r.text)
    type=c
    sum=0
    for ip in data_string["objects"]:
         sum = sum + 1
         print ip[type]
    endinfo(sum)

def dataall(a,b="hostname"):
    url = "http://monitor.yottaa.com:8000/XXXXX/instance/instances/?format=json&limit=0&data_center=%s" % a 
    r = requests.get(url, auth=('XXXXX', 'XXXXXXXXX'))
    data_string= json.loads(r.text)
    type=b
    sum=0
    for ip in data_string["objects"]:
         sum = sum + 1
         print ip[type]
    endinfo(sum)

def dataxxx(a,b,c="hostname"):
    url = "http://XXXXXXX:8000/XXXXX/instance/instances/?format=json&limit=0&data_center=%s&role=%s" % (a,b)
    r = requests.get(url, auth=('XXXXX', 'XXXXXXXXX'))
    data_string= json.loads(r.text)
    type=c
    sum=0
    for ip in data_string["objects"]:
         sum = sum + 1
         print ip[type]
    endinfo(sum)

def datarole(a,b,c,d="hostname"):
    url = "http://XXXXXX:8000/XXXXX/instance/instances/?format=json&limit=0&production_state=%s&data_center=%s&role=%s" % (a,b,c)
    r = requests.get(url, auth=('XXXXX', 'XXXXXXXXX'))
    data_string= json.loads(r.text)
    type=d
    sum=0
    for ip in data_string["objects"]:
         sum = sum + 1
         print ip[type]
    endinfo(sum)

def all(a="hostname"):
    url = "http://XXXXXX:8000/XXXXX/instance/instances/?format=json&limit=0"
    r = requests.get(url, auth=('XXXXX', 'XXXXXXXXX'))
    data_string= json.loads(r.text)
    type=a
    sum=0
    for ip in data_string["objects"]:
         sum = sum + 1
         print ip[type]
    endinfo(sum)    


def roleall(a,c="hostname"):
    url = "http://XXXXXXX:8000/XXXXX/instance/instances/?format=json&limit=0&role=%s" % a
    r = requests.get(url, auth=('XXXXX', 'XXXXXXXXX'))
    data_string= json.loads(r.text)
    type=c
    sum=0
    for ip in data_string["objects"]:
         sum = sum + 1
         print ip[type]
    endinfo(sum)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--role',        help='hosts role vars ex:lb tpu tmu dpu varnish ....')
    parser.add_argument('-e', '--environment', help='host  environment vars ex:production  stageing ')
    parser.add_argument('-a', '--attribute',   help='host attribute vars ex: public_ip instance_type topo_name hostname ....')
    parser.add_argument('-d', '--datacenter',   help='datacentr info ex:US-EAST-1 US-WEST-1 AP-SOUTHEAST-1  AP-NORTHEAST-1')
    parser.add_argument('-H', '--Host',   help=' hostname')
    parser.add_argument('-Y', '--yid',   help=' yid')
    parser.add_argument('-I', '--ip',    help=' ip address')
    parser.add_argument('-A', '--all',    help='list all host')
    args = vars(parser.parse_args())
    startinfo()

    typedict={'lb':1,'X':2,'X':3,'X':4,'X':5,'X':6,'X':7,'X':8,'X':9,'X':10,'X':11,'X':12,'X':13,'X':14,'X':15}
    datacenterdict={"US-EAST-1":'01',"US-WEST-1":'02','EU-WEST-1':'03','AP-SOUTHEAST-1':'04','AP-NORTHEAST-1':'05','US-WEST-2':'06','SA-EAST-1':'07','US-CHICAGO':'08','US-MIAMI':'09','AP-BJ':'10','US-DALLAS':'11','EU-UK':'12','EU-GERMANY':'13','AP-HONGKONG':'14','DAL2':'15','US-NYC':'16','EU-AMS':'17','AP-SIN':'18','AP-SOUTHEAST-2':'19','US-SJC':'20'}

    if args['environment'] == "production" and args['datacenter'] and args['role']:
      center=args['datacenter']
      if center.islower():
         center=center.upper()
      zhi=args['role']
      cha=datacenterdict[center]
      role=typedict[zhi]
      if args['attribute']:
         objects=args['attribute']
         datarole(1,cha,role,objects)
      else:
         datarole(1,cha,role)


    elif args['environment'] == "stageing" and args['datacenter'] and args['role']:
      center=args['datacenter']
      if center.islower():
         center=center.upper()
      zhi=args['role']
      cha=datacenterdict[center]
      role=typedict[zhi]
      if args['attribute']:
         objects=args['attribute']
         datarole(2,cha,role,objects)
      else:
         datarole(2,cha,role)

    elif args['environment'] == "production" and args['role']:
      zhi=args['role']
      cha=typedict[zhi]
      if args['attribute']:
         objects=args['attribute']
         listtype(1,cha,objects)
      else:
         listtype(1,cha)
    elif args['environment'] == "stageing" and args['role']:
      zhi=args['role']
      cha=typedict[zhi]
      if args['attribute']:
         objects=args['attribute']
         listtype(1,cha,objects)
      else:
         listtype(2,cha)

    elif args['datacenter'] and args['role']:
      zhi=args['role']
      center=args['datacenter']
      if center.islower():
         center=center.upper()
      cha=typedict[zhi]
      value=datacenterdict[center]
      if args['attribute']:
         objects=args['attribute']
         dataxxx(value,cha,objects)
      else:
         dataxxx(value,cha)

    elif args['environment'] == "production" and args['datacenter']:
      center=args['datacenter']
      if center.islower():
         center=center.upper()
      cha=datacenterdict[center]
      if args['attribute']:
         objects=args['attribute']
         datacenter(1,cha,objects)
      else:
         datacenter(1,cha)

    elif args['environment'] == "stageing" and args['datacenter']:
      center=args['datacenter']
      if center.islower():
         center=center.upper()
      cha=datacenterdict[center]
      if args['attribute']:
         objects=args['attribute']
         datacenter(2,cha,objects)
      else:
         datacenter(2,cha)

    elif args['datacenter']:
      center=args['datacenter']
      if center.islower():
         center=center.upper()
      cha=datacenterdict[center]
      if args['attribute']:
         objects=args['attribute']
         dataall(cha,objects)
      else:
         dataall(cha)
        
    elif args['Host']:
      hostname=args['Host']
      hosts(hostname)

    elif args['yid']:
      YID=args['yid']
      yid(YID)
    
    elif args['ip']:
      IP=args['ip']
      ip(IP)

    elif args['environment'] == "production":
      if args['attribute']:
         objects=args['attribute']
         listall(1,objects)
      else:
         listall(1)
    elif args['environment'] == "stageing":
      if args['attribute']:
         objects=args['attribute']
         listall(2,objects)
      else:
        listall(2)
   
    elif args['role']:
      zhi=args['role']
      cha=typedict[zhi]
      if args['attribute']:
         objects=args['attribute']
         roleall(cha,objects)
      else:
         roleall(cha) 

    elif args['all']:
      if args['attribute']:
        objects=args['attribute']
        all(objects)
      else:
        all()
    else:
      parser.print_help()
      sys.exit()
