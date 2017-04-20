#!/usr/bin/env bash

# setup.sh
# --------
#
# Must be run from project root.
#
# Setup Vital Records Printing development environment.

# add vagrant box if not added
readonly DEFAULT_BOXPATH="./rhel-6.8.virtualbox.box"
echo Verifying vagrant box \"rhel-6.8-5.1.18\" added...
vagrant box list | grep rhel-6.8-5.1.18 >/dev/null 2>&1 || {
    echo Box not found.
    read -p "path to box file ($DEFAULT_BOXPATH): " boxpath
    boxpath=${boxpath:-$DEFAULT_BOXPATH}
    if [ -f $boxpath ]; then
        vagrant box add rhel-6.8-5.1.18 $boxpath
    else
        echo $boxpath not found
        exit 1
    fi
}

# install vagrant plugins if not installed
echo Checking vagrant plugins...
plugins=`vagrant plugin list`
echo $plugins | grep vagrant-reload >/dev/null 2>&1 || vagrant plugin install vagrant-reload
echo $plugins | grep vagrant-vbguest >/dev/null 2>&1 || vagrant plugin install vagrant-vbguest
echo $plugins | grep vagrant-triggers >/dev/null 2>&1 || vagrant plugin install vagrant-triggers

# Copy Vagrantfile.example if Vagrantfile not found
if [ ! -f Vagrantfile ]; then
    echo Copying Vagrantfile.example to Vagrantfile
    cp Vagrantfile.example Vagrantfile
    read -n1 -p "Would you like to stop this script and make changes to ./Vagrantfile? [y/n] " stop
    case $stop in
        y|Y) echo; echo Exiting; exit 0 ;;
    esac
    echo
fi

# get RedHat credentials from env or stdin
if [ "$RH_USER" -a "$RH_PASS" ]; then
    rh_username=$RH_USER
    rh_password=$RH_PASS
else
    echo Enter your RedHat Developer Account credentials
    read -p "username: " rh_username
    read -s -p "password: " rh_password
    echo
fi

# get DVR credentials from env or stdin
if [ "$DVR_USER" -a "$DVR_PASS" ]; then
    dvr_username=$DVR_USER
    dvr_password=$DVR_PASS
else
    echo "Enter the service account credentials for mounting DVR"
    read -p "username (doris_dvr): " dvr_username
    dvr_username=${dvr_username:-doris_dvr}
    read -s -p "password: " dvr_password
    echo
fi

# vagrant up with RedHat and DVR mounting credentials as environment variables
RH_USER=$rh_username RH_PASS=$rh_password DVR_USER=$dvr_username DVR_PASS=$dvr_password vagrant up
