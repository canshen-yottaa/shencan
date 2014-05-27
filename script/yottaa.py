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
    print '*HOST:\t',args['Host']
    print '=' * 52
    print '\033[0m'

def listtype(a,b,c='public_ip'):
      url = "http://monitor.yottaa.com:8000/api/instance/instances/?format=json&limit=0&production_state=%d&role=%d" %  (a,b)
      r = requests.get(url, auth=('XXX', 'XXXXXXXX))
      data_string= json.loads(r.text)
      lx=c
      sum=0
      for ip in data_string["objects"]:
         sum = sum +1
         print ip[lx]
      print '\033[1;31;40m'
      print '=' * 52
      print '\tQuery number is\t', sum
      print '=' * 52
      print '\033[0m'
def listall(a,c='public_ip'):
      url = "http://monitor.yottaa.com:8000/api/instance/instances/?format=json&limit=0&production_state=%d" %  a
      r = requests.get(url, auth=('XXXX', 'XXXXXXX'))
      data_string= json.loads(r.text)
      type=c
      sum=0
      for ip in data_string["objects"]:
          sum = sum + 1
          print ip[type]
      print '\033[1;31;40m'
      print '=' * 52
      print '\tQuery number is\t', sum
      print '=' * 52
      print '\033[0m'

def hosts(a,b):
    url = "http://monitor.yottaa.com:8000/api/instance/instances/?format=json&limit=0&production_state=%s&hostname=%s" % (a,b)
    r = requests.get(url, auth=('XXXX', 'XXXXXXX'))
    result = data_string['objects']
    print '\033[1;31;40m'
    print '=' * 52
    print '\tQuery  infomation for\t', args['Host']
    print '=' * 52
    print '\033[0m'
    print json.dumps(result,indent=4)
   

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--role',        help='hosts role vars ex:lb tpu tmu dpu varnish ....')
    parser.add_argument('-e', '--environment', help='host  environment vars ex:production  stageing ')
    parser.add_argument('-a', '--attribute',   help='host attribute vars ex: public_ip instance_type topo_name hostname ....')
    parser.add_argument('-H', '--Host',   help=' hostname')

    args = vars(parser.parse_args())
    startinfo()
    typedict={'lb':1,'tpu':2,'tmu':3,'mca':4,'varnish':5,'dpu':6,'log':7,'cassandra':8,'mca-win':9,'zk':10,'ops':11,'mongodb':12,'mca-win-az':13,'elasticsearch':14,'mca-win-wmi':15}
    if args['environment'] == "production" and args['role']:
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
    elif args['environment'] == "stageing" and  args['Host']:
      hostname=args['Host']
      hosts(2,hostname)

    elif args['environment'] == "production" and  args['Host']:
      hostname=args['Host']
      hosts(1,hostname)

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
    else:
      parser.print_help()
      sys.exit()
