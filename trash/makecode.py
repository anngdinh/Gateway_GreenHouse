def on_data_received():
    pass
serial.on_data_received(serial.delimiters(Delimiters.HASH), on_data_received)

led.enable(False)

def on_forever():
    pins.digital_write_pin(DigitalPin.P0, 1)
    NPNBitKit.dht11_read(DigitalPin.P3)
    radio.send_string("!1:TEMP:" + str(NPNBitKit.dht11_temp()) + "#")
    pins.digital_write_pin(DigitalPin.P0, 0)
    basic.pause(3000)
basic.forever(on_forever)
