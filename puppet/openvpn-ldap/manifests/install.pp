class openvpn::install {
  package { ['openvpn','openvpn-auth-ldap','easy-rsa','pexpect'] : 
  ensure => 'installed',
}

}
