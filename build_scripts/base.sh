#!/usr/bin/env bash
#
# Usage
#
#	./base.sh mount_user mount_password
#
# Base setup post proxy setup and RedHat registration

# install packages
sudo yum -y groupinstall "Development Tools"
sudo yum -y install kernel-devel cifs-utils

# activate virtualbox guest additions
sudo /etc/init.d/vboxadd setup

# auto-cd to /vagrant on login
echo "cd /vagrant" >> /home/vagrant/.bash_profile

# setup auto-mounting DVR
sudo mkdir /mnt/dvr /etc/samba
sudo printf "username=$1\npassword=$2\n" > /etc/samba/passwd
sudo printf "//10.132.41.31/DVR\t/mnt/dvr\tcifs\t_netdev,credentials=/etc/samba/passwd\t0 0\n" >> /etc/fstab
