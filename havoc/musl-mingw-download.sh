#!/bin/bash
mkdir -p /opt/musl-mingw && cd /opt/musl-mingw

wget https://musl.cc/x86_64-w64-mingw32-cross.tgz -O /opt/musl-mingw/x86_64-w64-mingw32-cross.tgz
tar -xvzf /opt/musl-mingw/x86_64-w64

wget https://musl.cc/i686-w64-mingw32-cross.tgz -O /opt/musl-mingw/i686-w64-mingw32-cross.tgz
tar -xvzf /opt/musl-mingw/i686-w64-mingw32-cross.tgz
