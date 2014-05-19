#!/bin/bash
id=`cat /tmp/vpnid`
cd /usr/share/easy-rsa/2.0/  
source ./vars
./clean-all
./build-ca 
./build-key-server $id
./build-dh dh2048.pem
cd /root/
/bin/cp -ra /usr/share/easy-rsa/2.0/  /etc/openvpn/easy-rsa
service openvpn restart 

