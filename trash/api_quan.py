import serial.tools.list_ports
import random
import time
import  sys
from  Adafruit_IO import  MQTTClient
AIO_FEED_ID = "BBC_LED"
AIO_USERNAME = "thucquan"
AIO_KEY = "aio_Ipyu08olQehDLPEOmU7DrthaIsDW"

from flask import Flask, jsonify
from flask import request


app = Flask(__name__)



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
    # ser.write((str(payload) + "#").encode())


# def getPort():
#     ports = serial.tools.list_ports.comports()
#     N = len(ports)
#     commPort = "None"
#     for i in range(0, N):
#         port = ports[i]
#         strPort = str(port)
#         if "USB Serial Device" in strPort:
#             splitPort = strPort.split(" ")
#             commPort = (splitPort[0])
#     print(commPort)
#     return commPort

# ser = serial.Serial( port="COM7", baudrate=115200)

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()
# connected(client)

@app.route("/BBC_LED/add", methods=["POST"])
# @cross_origin(origin='*')
def add_data():
    request_json = request.json
    print(request_json["last"])
    client.publish("BBC_LED", request_json["last"])
    return "success"

while True:
    # value = random.randint(20, 10)
    # print("Cap nhat:", value)
    # client.publish("BBC_LED", value)
    # time.sleep(2)
    app.run(debug=True)