class openvpn::conf  {

     file {'/etc/openvpn/server.conf':
     ensure => present,
     content => template('openvpn/server.conf.erb'),
     owner => 'root',
     group => 'root',
     mode => '0644',
     require => Class['openvpn::install'],
     }

     file {'/etc/openvpn/auth/ldap.conf':
     ensure => present,
     source => "puppet://$puppetserver/modules/openvpn/ldap.conf",
     owner => 'root',
     group => 'root',
     mode => '0644',
     require => Class['openvpn::install'],
     }
      

}
