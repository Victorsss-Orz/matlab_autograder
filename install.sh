#!/bin/sh

apt update
apt install -y python3
apt update
if apt install -y octave; then
    echo "Octave installed successfully"
else
    echo "Failed to install Octave"
fi
apt install -y python3-pip

pip3 install --no-cache-dir scipy