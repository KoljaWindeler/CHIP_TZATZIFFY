echo "listing all install overlays"
find /lib/firmware/nextthingco/chip/
echo ""

echo "is module w1_ds2431 loaded"
lsmod | grep w1_ds2431
echo ""

echo "what eeprom were found"
ls /sys/bus/w1/devices/
echo ""

echo "reading eeprom code"
cat /sys/bus/w1/devices/2d-000*/eeprom | hexdump -C
echo ""

echo "is the backlight device loaded"
ls /sys/class/backlight/backlight/
