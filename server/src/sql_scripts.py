"""prepared sql scripts here"""

insert_report = \
"""
INSERT INTO periodic_report (time, accel_x, accel_y,
accel_z, temp, light_level, touch_pin0, touch_pin1,
touch_pin2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

select_temps = \
"""
SELECT `time`, `temp`
FROM `periodic_report`
WHERE `time` > %s AND `time` < %s;
"""

select_light = \
"""
SELECT `time`, `light_level`
FROM `periodic_report`
WHERE `time` > %s AND `time` < %s;
"""

select_pins = \
"""
SELECT `time`, `touch_pin0`, `touch_pin1`, `touch_pin2`
FROM `periodic_report`
WHERE `time` > %s AND `time` < %s;
"""