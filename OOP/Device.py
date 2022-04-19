import requests
import datetime
import json
import schedule

def takeTime(value):
    x = value.split(':')
    h = int(x[0]) if len(x) > 0 else 0
    m = int(x[1]) if len(x) > 1 else 0
    return [h, m]
class Device:
    def __init__(self, info):
        self.info = info
        self.update()
    
    def update(self):
        content = requests.get(self.info["api_device"]).json()
        self.name = content["name"]
        self.autoControl = content["auto"]
        self.hourFrom = takeTime(content["hourFrom"])
        self.hourTo = takeTime(content["hourTo"])
        content = requests.get(self.info["api_feed"]).json()
        self.last_value = content["last_value"]
        print("Update device", self.name)
        self.print()
        self.checkAuto()
    
    def print(self):
        print(self.name, self.autoControl, self.hourFrom, self.hourTo, self.last_value)
    
    def checkAuto(self):
        if self.autoControl:
            strStart = ("00" + str(self.hourFrom[0]))[-2:] + ":" + ("00" + str(self.hourFrom[1]))[-2:]
            strEnd   = ("00" + str(self.hourTo[0]))[-2:] + ":" + ("00" + str(self.hourTo[1]))[-2:]
            # print(strStart)
            # print(strEnd)
            schedule.every().day.at(strStart).do(self.postAdafruit, "ON").tag(self.name)
            schedule.every().day.at(strEnd  ).do(self.postAdafruit, "OFF").tag(self.name)

            now = datetime.datetime.now()
            start = now.replace(hour=self.hourFrom[0], minute=self.hourFrom[0])
            end = now.replace(hour=self.hourTo[0], minute=self.hourTo[0])
            if now >= start and now < end and self.last_value == "OFF":
                self.postAdafruit("ON")
            elif (now < start or now > end) and self.last_value == "ON":
                self.postAdafruit("OFF")
        else:
            self.postAdafruit("OFF")

    def postAdafruit(self, value):
        data = {
            "x-aio-key": self.info["key"],
            "datum": {
                "value": value
            }
        }
        x = requests.post(self.info["api_post"], data=json.dumps(data), headers=self.info["headers"])
        print(x.text)

