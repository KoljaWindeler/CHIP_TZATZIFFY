DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
sudo rmdir /sys/kernel/config/device-tree/overlays/JKW_TZATZIFFY/ >/dev/null 2>&1;
sudo mkdir /sys/kernel/config/device-tree/overlays/JKW_TZATZIFFY
dmesg >/tmp/pre_JKW_TZATZIFFY_load
su -c 'cat '$DIR'/JKW_tzatziki.dtbo > /sys/kernel/config/device-tree/overlays/JKW_TZATZIFFY/dtbo'
sleep 3
dmesg >/tmp/post_JKW_TZATZIFFY_load
diff /tmp/pre_JKW_TZATZIFFY_load /tmp/post_JKW_TZATZIFFY_load
rm /tmp/pre_JKW_TZATZIFFY_load /tmp/post_JKW_TZATZIFFY_load

