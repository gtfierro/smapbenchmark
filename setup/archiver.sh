# bash script to setup environment on Ubuntu 14.04 for sMAP unitoftime archiver

# install infrastructure, then update from git
sudo add-apt-repository ppa:cal-sdb/smap
sudo apt-get update
sudo apt-get install -y python-smap readingdb powerdb2 git python-pip

# get latest version
cd
git clone http://github.com/SoftwareDefinedBuildings/smap
cd smap/python
sudo pip install -e .
