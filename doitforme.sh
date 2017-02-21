wget -q --tries=10 --timeout=20 --spider http://google.com
if [[ $? -eq 0 ]]; then
        echo "Online"
	sudo apt update; 
	sudo apt install git -y; 
	cd /opt/;
	sudo git clone https://github.com/KoljaWindeler/CHIP_TZATZIFFY.git;
	sudo /opt/CHIP_TZATZIFFY/overlay/chip/install.sh;
	sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf.bak; 
	sudo cp /opt/CHIP_TZATZIFFY/scripts/xorg.conf /etc/X11/;
	sudo reboot;
else
        echo "Offline"
fi
