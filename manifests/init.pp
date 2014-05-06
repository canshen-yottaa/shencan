class openvpn {
     $vpn = hiera_hash('vpn')
     $id = $vpn['HK']['host']
     $net =  $vpn['HK']['net']
     $mask = $vpn['HK']['mask']
     exec { 'vpn id':
     command => "echo  $id >/tmp/vpnid",
     cwd => "/root/",
     path => ["/bin","/usr/bin/"],
     }
     include openvpn::epel
     include openvpn::install
     include openvpn::conf
     include openvpn::key

}
