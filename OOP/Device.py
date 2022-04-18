import requests
import datetime
import json

class Device:
    def __init__(self, info):
        self.info = info
        self.update()
    
    def update(self):
        content = requests.get(self.info["api_device"]).json()
        self.name = content["name"]
        self.autoControl = content["auto"]
        self.hourFrom = int(content["hourFrom"])
        self.hourTo = int(content["hourTo"])
        content = requests.get(self.info["api_feed"]).json()
        self.last_value = content["last_value"]
        print("Update device", self.name)
        self.print()
    
    def print(self):
        print(self.name, self.autoControl, self.hourFrom, self.hourTo, self.last_value)
    
    def checkAuto(self):
        if self.autoControl:
            now = datetime.datetime.now()
            hour = int(now.hour)
            if hour >= self.hourFrom and hour < self.hourTo and self.last_value == "OFF":
                # post API on, off
                pass
            elif (hour < self.hourFrom or hour >= self.hourTo) and self.last_value == "ON":
                pass
    def postAdafruit(self, value):
        data = {
            "x-aio-key": self.info["key"],
            "datum": {
                "value": value
            }	
        }
        x = requests.post(self.info["api_post"], data=json.dumps(data), headers=self.info["headers"])
        print(x.text)

