#!/bin/sh
apt-get install python3-pil.imagetk python3-pil python3-tk
echo "xset s off # don't activate screensaver" >> /etc/X11/xinit/xinitrc
echo "xset -dpms # disable DPMS (Energy Star) features." >> /etc/X11/xinit/xinitrc
echo "xset s noblank" >> /etc/X11/xinit/xinitrc
