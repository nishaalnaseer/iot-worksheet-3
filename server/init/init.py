import json
import pymysql


def main():
    with open("src/config.json", 'r') as f:
        config = json.load(f)

    with open("init/init.sql", 'r') as f:
        script = f.read()

    connection = pymysql.Connection(
        host=config["db_ip"],
        user=config["username"],
        password=config["password"],
        port=config["port"],
    )
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS `worksheet-3`")
    cursor.execute("USE `worksheet-3`")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS `periodic_report` (
            `time` int(11) NOT NULL,
            `accel_x` int(11) NOT NULL,
            `accel_y` int(11) NOT NULL,
            `accel_z` int(11) NOT NULL,
            `temp` int(11) NOT NULL,
            `light_level` int(11) NOT NULL,
            `touch_pin0` bit(1) NOT NULL,
            `touch_pin1` bit(1) NOT NULL,
            `touch_pin2` bit(1) NOT NULL,
            PRIMARY KEY (`time`),
            UNIQUE KEY `time` (`time`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    """)
    cursor.close()
    connection.commit()

if __name__ == "__main__":
    main()
