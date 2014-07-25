class packages {

  package { ['bind-utils','wget','htop','nload'] : 
  ensure => 'installed',
          }
  case $::operatingsystemrelease {

    /^6/: {
        notify {'Centos 6.X OS.': }
        package { 'nmon-14g-1.el6.rf.x86_64.rpm':
        ensure => 'installed',
        source => ‘ftp://ftp.univie.ac.at/systems/linux/dag/redhat/el6/en/x86_64/dag/RPMS/nmon-14g-1.el6.rf.x86_64.rpm’,
        }

      }
   /^5/: {
        notify {'Centos 5.X OS.': }
        package { 'nmon-14g-1.el5.rf.x86_64.rpm':
        ensure => 'installed',
        source => ‘ftp://ftp.univie.ac.at/systems/linux/dag/redhat/el5/en/x86_64/dag/RPMS/nmon-14g-1.el5.rf.x86_64.rpm’,
        }
      }
    }

}
