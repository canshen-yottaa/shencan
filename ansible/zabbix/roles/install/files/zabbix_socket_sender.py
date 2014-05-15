#!/usr/bin/python
#-*- coding:utf-8 -*-
#Author Jiang Liu<jiang.liu@yottaa.com>
import os
import time
import socket
import struct
import cPickle
import logging
try:
    from hashlib import sha1
except ImportError:
    from sha import sha as sha1
try:
    import json
except ImportError:
    import simplejson as json

DUMP = 'dump'
if not os.path.isdir(DUMP):
    os.makedirs(DUMP, mode=0755)

class Zabbix(object):

    logger = logging.getLogger('zabbix')

    def __init__(self, values=None):
        if values is not None:
            self.__dict__['values'] = values

    def __getattr__(self, name):
        if name in ('values'):
            return self.__dict__[name]
        return None

    def __setattr__(self, name, value):
        if name == 'values':
            self.__dict__[name] = value

    def gen_request(self, jsons):
        if isinstance(jsons, basestring):
            data = '%s\n' % jsons
        else:
            data = json.dumps(jsons)
        header = 'ZBXD\x01'
        datalen = struct.pack('Q', len(data))
        return header + datalen + data

    def dump(self, host, port, jsons):
        data = {'host': host, 'port': port, 'jsons': jsons}
        hash = sha1(json.dumps(data)).hexdigest()
        path = '%s.%s.%d.%s.error' % (host, port, int(time.time()), hash)
        try:
            write = open(os.path.join(DUMP, path), 'wb')
            cPickle.dump(data, write, -1)
            write.close()
        except:
            self.logger.exception('cannot dump to file %s', path)

    def get_zbx_result(self, host, port, jsons):
        retry = 3
        while retry:
            try:
                data = self._get_zbx_result(host, port, jsons)
                if data is None:
                    break
                return data
            except socket.error:
                self.logger.exception('cannot communit with zabbix')

            time.sleep(5)
            retry -= 1

        self.logger.error('cannot send data to zabbix server')
        self.dump(host, port, jsons)

    def _get_zbx_result(self, host, port, jsons):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.send(self.gen_request(jsons))
        self.logger.debug('sent %s', jsons)

        recv = sock.recv(5)
        if recv != 'ZBXD\x01':
            self.logger.error('Invalid Response')
            self.dump(host, port, jsons)
            return None

        recv = sock.recv(8)
        (datalen,) = struct.unpack('Q', recv)
        data = sock.recv(datalen)
        sock.close()
        self.logger.debug('received %s', data)
        return data

    def getvalue(self):
        # shoulde be {host: {key: value}}
        return self.values

    def run(self):
        hostvalues = self.getvalue()
        if not isinstance(hostvalues, dict):
            self.logger.error('invalid hostvalues: %s', str(hostvalues))
            return False

        clock = int(time.time())
        jsons = {
            'request': 'agent data',
            'data': [],
            'clock': clock,
        }
        data = jsons['data']
        for host, values in hostvalues.iteritems():
            for key, value in values.iteritems():
                data.append({
                    'host': host,
                    'key': key,
                    'value': value,
                    'clock': clock,
                })
        return self.get_zbx_result(ZBX_HOST, ZBX_PORT, jsons)

ZBX_HOST = 'zabbix.yottaa.com'
ZBX_PORT = 10051

handler = logging.FileHandler(filename='/tmp/zabbix.%s.log' % time.strftime('%Y%m%d'), mode='a')
formatter = logging.Formatter('%(asctime)s %(name)s %(lineno)s %(levelname)s %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    pass
