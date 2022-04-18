import serial.tools.list_ports
import random
import time
import  sys
from  Adafruit_IO import  MQTTClient

AIO_FEED_ID = "test"
AIO_USERNAME = "an_ngdinh"
AIO_KEY = "aio_mCse60UxmTyMAW9N2bepjWjIp1n8"

def  connected(client):
    print("Ket noi thanh cong...")
    client.subscribe(AIO_FEED_ID)

def  subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong...")

def  disconnected(client):
    print("Ngat ket noi...")
    sys.exit (1)

def  message(client , feed_id , payload):
    print("Nhan du lieu: " + payload)
    ser.write((str(payload) + "#").encode())


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
    return commPort

ser = serial.Serial( port=getPort(), baudrate=115200)

# client = MQTTClient(AIO_USERNAME , AIO_KEY)
# client.on_connect = connected
# client.on_disconnect = disconnected
# client.on_message = message
# client.on_subscribe = subscribe
# client.connect()
# client.loop_background()

# while True:
#     value = random.randint(0, 1)
#     print("Cap nhat:", value)
#     client.publish("test", value)
#     time.sleep(3)


mess = ""
def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    # if splitData[1] == "TEMP":
    client.publish("test", splitData[2])

mess = ""
def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = ser.read(bytesToRead).decode("UTF-8")
        if ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            # processData(mess[start:end + 1])
            print(mess[start:end + 1])
            # if (end == len(mess)):
            #     mess = ""
            # else:
            #     mess = mess[end+1:]

while True:
    readSerial()
    time.sleep(1)
readSerial()
time.sleep(1)
    