#!/usr/bin/python
import pexpect
child = pexpect.spawn ('./build-ca')
child.expect ('Country Name*')
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
