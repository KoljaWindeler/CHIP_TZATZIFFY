 #!/bin/bash
LP=""
B=`cat /sys/class/backlight/backlight/actual_brightness`

while true; do
	P=`cat /sys/class/backlight/backlight/bl_power`
	if [ "$P" != "$LP" ]; then
		if [ "$P" == "0" ]; then
			# disp on
			echo $B > /sys/class/backlight/backlight/brightness
			echo "switching display on, to level $B"
		else
			# disp off
			echo "switching display off"
			echo 1 > /sys/class/backlight/backlight/brightness
			echo 0 > /sys/class/backlight/backlight/brightness
		fi
		LP=$P
	fi
  sleep 0.5
done
