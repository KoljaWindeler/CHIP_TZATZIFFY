#! /bin/sh

echo "version"
uname -r
echo ""

echo "listing all install overlays"
find /lib/firmware/nextthingco/chip/
echo ""

echo "is module w1_ds2431 loaded"
if [[ $(lsmod | grep w1_ds2431) ]]; then
	echo "yes, module is loaded"
else
	echo "module not loaded, reading /etc/modules"
	if [[ $(cat /etc/modules | grep w1_ds2431) ]]; then
		echo "it should be loaded, hmmm"
	else
		echo "/etc/modules wasn't modified correct"
		echo "will do it for you now"
		echo "echo "w1_ds2431" >> /etc/modules" | sudo sh
		echo "done, please reboot and rerun this"
	fi
fi
echo ""

echo "what eeprom were found"
ls /sys/bus/w1/devices/
echo ""

echo "reading eeprom code"
cat /sys/bus/w1/devices/2d-000*/eeprom | hexdump -C
echo ""

echo "is the backlight device loaded"
ls /sys/class/backlight/backlight/
