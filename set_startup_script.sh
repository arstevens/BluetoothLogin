#!/bin/bash
cd /etc
sudo sed -i '13,100d' rc.local
sudo echo './home/pi/main/BluetoothLogin/startup_scripts/pull.sh' >> rc.local
sudo echo './home/pi/main/BluetoothLogin/startup_scripts/bt_login_startup.sh &' >> rc.local
sudo echo 'exit 0' >> rc.local

