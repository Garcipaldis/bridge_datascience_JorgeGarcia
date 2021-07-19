#!/bin/bash
# Author: Gabriel Vázquez Torres @gabvaztor
install_python_yum(){

  echo "*********************"
  echo "UPDATING/INSTALLING PYTHON..."
  echo "*********************"
  sudo yum install -y python-pip
  sudo yum install -y python3
  alias python3="/usr/bin/python3"
  alias pip="python -m pip"
  alias pip3="python3 -m pip"
  sudo python -m pip install --upgrade pip
  sudo python -m pip install virtualenv
  sudo python3 -m pip install --upgrade pip
  sudo python3 -m pip install virtualenv
  echo "*********************"
  echo " PYTHON  CONFIGURED "
  echo "*********************" 
}

install_python2_yum

