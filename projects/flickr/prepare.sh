#!/bin/sh
sudo apt install python3-pil.imagetk python3-pil python3-tk git -y
cd /opt/
sudo git clone https://github.com/KoljaWindeler/CHIP_TZATZIFFY.git
python3 /opt/CHIP_TZATZIFFY/projects/flickr/setup.py


