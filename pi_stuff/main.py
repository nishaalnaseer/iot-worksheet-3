import serial
from time import time, sleep
from models import *
from requests import post as http_post
import json
import logging


with open("config.json", 'r') as f:
    config = json.load(f)

PORT = config["port"]
SERVER = config["server"]
logging.basicConfig(level=logging.INFO)
HEADER = {
    "accept": "application/json",
    "Content-Type": "application/json"
}


def eval_bool(string) -> bool:
    """turn string to like 'False' to False type bool"""
    if string.lower() == 'false':
        return False
    else:
        return True


def handle_data(ser):
    """formats and send data through and http post request"""
    line = ser.readline()
    if line:
        row = line.decode().split(",")

        # to_pi = "{},{},{},{},{},{},{},{},".format(
        #     accel_x, accel_y, accel_z,
        #     temp, light_level, touch_pin0,
        #     touch_pin1, touch_pin2
        # ) format in microbit how data is sent

        accel_x = row[0]
        accel_y = row[1]
        accel_z = row[2]
        temp = row[3]
        light_level = row[4]
        touch_pin0 = row[5]
        touch_pin1 = row[6]
        touch_pin2 = row[7]

        logging.info(row)

        report = Report(
            time=int(time()),
            accel_x=int(accel_x),
            accel_y=int(accel_y),
            accel_z=int(accel_z),
            temp=int(temp),
            light_level=int(light_level),
            touch_pin0=eval_bool(touch_pin0),
            touch_pin1=eval_bool(touch_pin1),
            touch_pin2=eval_bool(touch_pin2),
        )

        response = http_post(url=f"{SERVER}/periodic_report", data=report.model_dump_json())
        code = response.status_code
        if code != 201:
            content = response.content.decode()
            logging.info(f"HTTP ERROR {code}: {content}")


def main():
    while True:
        try:
            with serial.Serial(PORT, 115200, timeout=5) as ser:
                handle_data(ser)
        except Exception as e:
            # error message
            logging.info(e)
            logging.debug(e)
        sleep(1)


if __name__ == "__main__":
    main()
