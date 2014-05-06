class openvpn::key {
#     exec { 'cp easy-rsa':
#     command => " cp -ra /usr/share/easy-rsa/2.0/ /etc/openvpn/easy-rsa/",
#     cwd => "/root/",
#     path => ["/bin","/usr/bin/"],
#     onlyif => "test ! -d /etc/openvpn/easy-rsa/",
#     require => Class['openvpn::install']
#     }


    file  {'/usr/share/easy-rsa/2.0/vars':
     ensure => present,
     content => template('openvpn/vars.erb'),
     owner => 'root',
     group => 'root',
     mode => '0644',
     require => Class['openvpn::install'],
    }

    file {'/usr/share/easy-rsa/2.0/run.py':
    ensure => present,
    owner => 'root',
    group => 'root',
    mode => '0755',
    source =>   "puppet://$puppetserver/modules/openvpn/run.py",
    require => Class['openvpn::install'],    
    }

    file {'/usr/share/easy-rsa/2.0/run-server.py':
    ensure => present,
    owner => 'root',
    group => 'root',
    mode => '0755',
    source =>   "puppet://$puppetserver/modules/openvpn/run-server.py",
    require => Class['openvpn::install'],    
    }


    file {'/usr/share/easy-rsa/2.0/yottaa.sh':
    ensure => present,
    owner => 'root',
    group => 'root',
    mode => '0755',
    source =>   "puppet://$puppetserver/modules/openvpn/yottaa.sh",
    require => Class['openvpn::install'],
    }

     exec { 'key':  
     command => "sh yottaa.sh",
     cwd => "/usr/share/easy-rsa/2.0/",
     path => ["/bin","/usr/bin/"],
     require => File['/usr/share/easy-rsa/2.0/vars']
     }

     service {'openvpn':
     ensure => running,
     enable => true,
     require => Class['openvpn::conf'],
     }

}
