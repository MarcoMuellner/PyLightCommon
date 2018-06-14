#!/usr/bin/env bash

mkdir temp
cd temp

wget $1
tar -xzvf *
cd PyLight*
cp -r * ../../../../../
cd ../../
rm -r temp
echo $2 > ../../../PyLightServer/version
touch ../../../PyLightServer/wsgi.py
