echo 412 > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio412/direction
echo 1 > /sys/class/gpio/gpio412/value
