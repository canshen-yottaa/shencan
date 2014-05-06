#!/usr/bin/python
import pexpect
import sys
file = open("/tmp/vpnid")
for server in file:
   id= server
name = './build-key-server '+ id
print name
child = pexpect.spawn (name)
child.expect ('Country*')
child.sendline ('\r')
child.expect ('State or Province*')
child.sendline ('\r')
child.expect ('Locality Name*')
child.sendline ('\r')
child.expect('Organization Name*')
child.sendline ('\r')
child.expect('Common Name*')
child.sendline ('\r') 
child.expect('Na*')
child.sendline ('\r')
child.expect('Email.*')
child.sendline ('\r')
child.expect('.*challenge*')
child.sendline ('123456\r')
child.expect('An optional*')
child.sendline ('123456\r')
child.expect('Sign the.*')
child.sendline ('yes\r')
child.expect('1.*')
child.sendline ('yes\r')
