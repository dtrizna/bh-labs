#!/bin/bash

# download havoc
git clone https://github.com/HavocFramework/Havoc.git /opt/Havoc
cd /opt/Havoc

# install dependencies
sudo apt-get update
sudo apt install -y git build-essential apt-utils cmake libfontconfig1 libglu1-mesa-dev libgtest-dev libspdlog-dev libboost-all-dev libncurses5-dev libgdbm-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev libbz2-dev mesa-common-dev qtbase5-dev qtchooser qt5-qmake qtbase5-dev-tools libqt5websockets5 libqt5websockets5-dev qtdeclarative5-dev golang-go qtbase5-dev libqt5websockets5-dev python3-dev libboost-all-dev mingw-w64 nasm

# install go
sudo apt-get install -y golang-go
cd teamserver
go mod download golang.org/x/sys
go mod download github.com/ugorji/go

# build
cd ..
make ts-build

# start server
./havoc server --profile my-profile.yaotl -v --debug
