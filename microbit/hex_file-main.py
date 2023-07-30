from microbit import accelerometer, temperature, display, pin0, pin1, pin2, uart, sleep

while True:

    # get data
    accel_x, accel_y, accel_z = accelerometer.get_values()
    temp = temperature()
    light_level = display.read_light_level()
    touch_pin0 = pin0.is_touched()
    touch_pin1 = pin1.is_touched()
    touch_pin2 = pin2.is_touched()

    # turn data into a csv format
    to_pi = "{},{},{},{},{},{},{},{},".format(
        accel_x, accel_y, accel_z,
        temp, light_level, touch_pin0,
        touch_pin1, touch_pin2
    )

    if not uart.any():
        # send data if  there are any buffer is empty
        display.scroll("Sending")
        uart.write(to_pi)
    sleep(1000)  # wait, if not this will keep sending
