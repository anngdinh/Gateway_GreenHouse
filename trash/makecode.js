let cmd = ""
serial.onDataReceived(serial.delimiters(Delimiters.Hash), function () {
    cmd = serial.readUntil(serial.delimiters(Delimiters.Hash))
    if (cmd == "LTrue") {
        basic.showString("L1")
    } else if (cmd == "LFalse") {
        basic.showString("L0")
    } else if (cmd == "PTrue") {
        basic.showString("P1")
    } else if (cmd == "PFalse") {
        basic.showString("P0")
    }
})
basic.forever(function () {
    serial.writeString("!1:TEMP:" + input.temperature() + "#")
    basic.pause(5000)
    serial.writeString("!1:LIGHT:" + input.lightLevel() + "#")
    basic.pause(5000)
})
