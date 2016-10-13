#!/bin/bash


# Get the rtmp:// location. Regex will get the url, but it will have backslashes in it.
WGET_STRING="`wget -q -O- "http://www.iheart.com/live/945-the-buzz-2281/?_country=US&_rel=648&_bare=1" | grep -o "rtmp:.*@[0-9]\{6\}"`"

# Remove the backslashes in the url.
URL=${WGET_STRING//\\/}

# Start the rtmp dump application and record stream to mplayer
screen -S "radio_screen" -d -m
screen -r "radio_screen" -X stuff "nice --10 rtmpdump -r $URL -v | mplayer -&\n"
