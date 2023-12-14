#!/bin/sh

apt update
apt install -y python3
apt install -y octave
apt install -y python3-pip

pip3 install --no-cache-dir scipy