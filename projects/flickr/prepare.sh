#!/bin/sh
sudo apt update
sudo apt install python3-pil.imagetk python3-pil python3-tk git -y
cd /opt/
sudo git clone https://github.com/KoljaWindeler/CHIP_TZATZIFFY.git
sudo python3 /opt/CHIP_TZATZIFFY/projects/flickr/setup.py
sudo /opt/CHIP_TZATZIFFY/projects/flickr/start.sh
cd /opt/CHIP_TZATZIFFY/projects/flickr/
echo "run /opt/CHIP_TZATZIFFY/projects/flickr/start.sh to start"
echo "run python3 /opt/CHIP_TZATZIFFY/projects/flickr/setup.sh to change config"


