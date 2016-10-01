#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
MIN="$( uptime | awk -F'( |,|:)+' '{if ($7=="min") m=$6; else {if ($7~/^day/) {d=$6;h=$8;m=$9} else {h=$6;m=$7}}} {m=m+60*h+3600*d; print m}' )"
if [ "$MIN" -gt "3" ]; then
	echo "no-wait-start"
else
	echo "system just started, waiting extra 30sec"
	sleep 30
fi

export XAUTHORITY=/home/chip/.Xauthority
export DISPLAY=:0

xset s off
xset -dpms
xset s noblank

cd $DIR
python3 main.py
