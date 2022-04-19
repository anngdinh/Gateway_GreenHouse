import serial.tools.list_ports
import time
import  sys
from  Adafruit_IO import  MQTTClient
from Device import Device
from FeedData import FeedData
import schedule

AIO_FEED_ID = ['demo.led', 'demo.pump', 'demo.update'] # a feed to know when the limit, time auto control change
AIO_USERNAME = "an_ngdinh"
AIO_KEY = "aio_fFre76W77mjdTKM2ZYiG4ly1GsOn"

led_Info = {
    "headers": {'Content-type': 'application/json', 'Accept': 'text/plain'},
    "api_post": "https://io.adafruit.com/api/v2/an_ngdinh/feeds/demo.led/data",
    "api_device": "https://iot-do-an-api.herokuapp.com/device/Led",
    "api_feed": "https://io.adafruit.com/api/v2/an_ngdinh/feeds/demo.led",
    "key": AIO_KEY
}
pump_Info = {
    "headers": {'Content-type': 'application/json', 'Accept': 'text/plain'},
    "api_post": "https://io.adafruit.com/api/v2/an_ngdinh/feeds/demo.pump/data",
    "api_device": "https://iot-do-an-api.herokuapp.com/device/Pump",
    "api_feed": "https://io.adafruit.com/api/v2/an_ngdinh/feeds/demo.pump",
    "key": AIO_KEY
}
led = Device(led_Info)
pump = Device(pump_Info)

temp_Info = {
    # "headers": {'Content-type': 'application/json', 'Accept': 'text/plain'},
    # "api_post": "https://io.adafruit.com/api/v2/an_ngdinh/feeds/demo.temp/data",
    "api_device": "https://iot-do-an-api.herokuapp.com/device/Temp",
    # "api_feed": "https://io.adafruit.com/api/v2/an_ngdinh/feeds/demo.temp",
    # "key": AIO_KEY
}
humi_Info = {
    # "headers": {'Content-type': 'application/json', 'Accept': 'text/plain'},
    # "api_post": "https://io.adafruit.com/api/v2/an_ngdinh/feeds/demo.temp/data",
    "api_device": "https://iot-do-an-api.herokuapp.com/device/Humi",
    # "api_feed": "https://io.adafruit.com/api/v2/an_ngdinh/feeds/demo.temp",
    # "key": AIO_KEY
}
temp = FeedData(temp_Info)
humi = FeedData(humi_Info)

# Connect to adafruit
def connected(client):
    print("Ket noi thanh cong...")
    for feed in AIO_FEED_ID:
        client.subscribe(feed)

def subscribe(client , userdata , mid , granted_qos):
    print("Subcribe thanh cong...")

def disconnected(client):
    print("Ngat ket noi...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Nhan du lieu: ", client, feed_id, payload)
    if feed_id == "demo.led":
        ser.write(("LED_" + str(payload) + "#").encode())
    elif feed_id == "demo.pump":
        ser.write(("PUMP_" + str(payload) + "#").encode())
    elif feed_id == "demo.update":
        # schedule.clear()
        if str(payload) == "10":
            schedule.clear('Pump')
            pump.update()
        elif str(payload) == "20":
            schedule.clear('Led')
            led.update()
        elif str(payload) == "30":
            temp.update()
        elif str(payload) == "40":
            humi.update()
        else:
            schedule.clear()
            led.update()
            pump.update()
            temp.update()
            humi.update()
        print(schedule.get_jobs())

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()


# Connect to serial
def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
            print(commPort)
    return commPort

ser = serial.Serial( port="COM8", baudrate=115200)

mess = ""
def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    if splitData[1] == "TEMP":
        client.publish("demo.temp", splitData[2])
        temp.checkLimit(int(splitData[2]))
    elif splitData[1] == "HUMI":
        client.publish("demo.humi", splitData[2])
        humi.checkLimit(int(splitData[2]))

def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]

def main():
    
    print(schedule.get_jobs())
    while True:
        readSerial()
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()