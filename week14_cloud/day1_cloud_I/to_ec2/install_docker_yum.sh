#!/bin/bash
# Author: Gabriel Vázquez Torres @gabvaztor
###  Control will jump here if $DIR does NOT exists ###
echo "***************************"
echo "**DOCKER INSTALLATION STARTED...**"
echo "***************************"

sudo yum update -y
sudo yum uninstall docker -y
sudo amazon-linux-extras install docker -y
sudo service docker start
# change this if needed
sudo usermod -a -G docker ec2-user
sudo service docker restart

echo ""
echo "***************************"
echo "** DOCKER INSTALLATION FINISHED **"
echo "***************************"
