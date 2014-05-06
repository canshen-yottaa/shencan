#!/bin/bash
cd /usr/share/easy-rsa/2.0  
./clean-all
source ./vars
python run.py
python run-server.py
./build-dh dh2048.pem
cd /root/
cp -ra /usr/share/easy-rsa/2.0 /etc/openvpn/easy-rsa

