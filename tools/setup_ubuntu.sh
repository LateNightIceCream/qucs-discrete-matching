#!/bin/sh
git submodule init
git submodule update

sudo add-apt-repository -y ppa:rock-core/qt4
sudo apt update
sudo apt install -y python3-matplotlib python3-numpy
sudo apt install -y adms automake build-essential libtool libtool-bin gperf flex bison pkg-config qt5-default

mkdir qucs_git
cd qucs_git
# get source
git clone git://git.code.sf.net/p/qucs/git qucs
cd qucs
git submodule init
git submodule update

cd qucs
./bootstrap
./configure
make
sudo make install
