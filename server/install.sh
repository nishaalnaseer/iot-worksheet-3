#!/bin/bash

# check if we have sudo permission, if not exit
if [ "$UID" -ne 0 ]; then
    echo "Error: This script requires root (sudo) permissions."
    exit 1
fi

# create python virtual enviroment
python3 -m venv venv
source ./venv/bin/activate

# installing dependencies
pip install -r requirements.txt

# setup database
python3 init/init.py

# create script to run main.py file
echo "#!/bin/bash
cd /home/pi/Desktop/iot-worksheet-3/worksheet-3-server
source ./venv/bin/activate
python3 main.py
" > run.sh

# give execution rights to our newly created file
chmod +x run.sh

echo "run.sh created successfully."

# setting up a service
echo "[Unit]
Description=backend for recording and data handling of the microbit device

[Service]
ExecStart=/home/pi/Desktop/iot-worksheet-3/worksheet-3-server/run.sh

[Install]
WantedBy=multi-user.target
" > /etc/systemd/system/worksheet-3-server.service

# enabling the service, and starting it on system startup
sudo systemctl daemon-reload
sudo systemctl enable worksheet-3-server.service
sudo systemctl start worksheet-3-server.service
sudo systemctl status worksheet-3-server.service
