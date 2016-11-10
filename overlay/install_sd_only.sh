#!/bin/bash
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo "@reboot "$DIR"/load.sh" >> mycron
#install new cron file
crontab mycron
rm mycron
echo "installation done, please reboot now"
