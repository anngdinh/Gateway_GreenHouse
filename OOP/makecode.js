let cmd = ""
serial.onDataReceived(serial.delimiters(Delimiters.Hash), function () {
    cmd = serial.readUntil(serial.delimiters(Delimiters.Hash))
    if (cmd == "LED_ON") {
        basic.showString("L1")
    } else if (cmd == "LED_OFF") {
        basic.showString("L0")
    } else if (cmd == "PUMP_ON") {
        basic.showString("P1")
    } else if (cmd == "PUMP_OFF") {
        basic.showString("P0")
    }
})
basic.forever(function () {
    serial.writeString("!1:TEMP:" + input.temperature() + "#")
    basic.pause(5000)
    serial.writeString("!1:HUMI:" + input.humidity() + "#")
    basic.pause(5000)
    // serial.writeString("!1:LIGHT:" + input.lightLevel() + "#")
    // basic.pause(5000)
})
