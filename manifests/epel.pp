class openvpn::epel {
 case $::operatingsystemrelease {
      /^5/: {
       notify {'Centos 5.X OS.': }
       file { 'copy epel file':
       name => "/tmp/epel-release-5-4.noarch.rpm",
       ensure => present,
       owner => root,
       mode => 0644,
       source => "puppet://$puppetserver/modules/openvpn/epel-release-5-4.noarch.rpm",
             }
      }
      /^6/: {
       notify {'Centos 6.X OS.': }
       file { 'copy epel file':
       name => "/tmp/epel-release-6-8.noarch.rpm",
       ensure => present,
       owner => root,
       mode => 0644,
       source => "puppet://$puppetserver/modules/openvpn/epel-release-6-8.noarch.rpm",
           }
      }
    }
	

     exec { 'install epel':  
     command => "rpm -vih epel-release-$operatingsystemmajrelease-*.noarch.rpm",
     cwd => "/tmp/",
     path => ["/bin","/usr/bin/"],
     onlyif => "test ! -f /etc/yum.repos.d/epel-testing.repo",
     require => file['copy epel file'],
      }

}
