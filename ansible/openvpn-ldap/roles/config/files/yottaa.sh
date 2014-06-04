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
cat <<EOF >/root/client.conf
client
dev tun
proto tcp
remote  XXXXX  1194
resolv-retry infinite
nobind
persist-key
persist-tun
<ca>
`cat /usr/share/easy-rsa/2.0/keys/ca.crt`
</ca>
ns-cert-type server
comp-lzo
verb 3
auth-user-pass
EOF
service openvpn restart 

echo -e "\e[32m clinet files is /root/client.conf you need change openvpn server ip address \e[0m"
