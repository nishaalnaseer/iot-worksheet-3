#!/bin/bash

# check if we have sudo permission, if not exit
if [ "$UID" -ne 0 ]; then
    echo "Error: This script requires root (sudo) permissions."
    exit 1
fi

# create python virtual enviroment
python3 -m venv venv
source ./venv/bin/activate

pip install -r requirements.txt

# create script to run main.py file
echo "#!/bin/bash
sleep 60
cd /home/pi/Desktop/iot-worksheet-3/worksheet-3-pi_stuff
source ./venv/bin/activate
python3 main.py
" > run.sh

# give execution rights to our newly created file
chmod +x run.sh

echo "run.sh created successfully."

# setting up a service
echo "[Unit]
Description=microbit data recorder and sender to a web server

[Service]
ExecStart=/home/pi/Desktop/iot-worksheet-3/worksheet-3-pi_stuff/run.sh

[Install]
WantedBy=multi-user.target
" > /etc/systemd/system/worksheet-3-pi_stuff.service

# enabling the service on system startup and starting it
sudo systemctl daemon-reload
sudo systemctl enable worksheet-3-pi_stuff.service
sudo systemctl start worksheet-3-pi_stuff.service
sudo systemctl status worksheet-3-pi_stuff.service
