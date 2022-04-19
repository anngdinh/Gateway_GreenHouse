import requests
import datetime
from Notification import Notification

class FeedData:
    def __init__(self, info):
        self.info = info
        self.update()
    
    def update(self):
        content = requests.get(self.info["api_device"]).json()
        self.name = content["name"]
        self.unit = ""
        if self.name == "Temp":
            self.unit = "°C"
        elif self.name == "Humi":
            self.unit = "%"
        self.autoControl = content["auto"]
        self.lowerLimit = int(content["hourFrom"])
        self.upperLimit = int(content["hourTo"])
        print("Update feed data", self.name)
        self.print()
    
    def print(self):
        print(self.name, self.autoControl, self.lowerLimit, self.upperLimit)
    
    def checkLimit(self, value):
        if self.autoControl:
            value = int(value)
            if value < self.lowerLimit:
                Notification.push(self.name.upper() + " is " + str(value) + self.unit +  " lower than " + str(self.lowerLimit) + self.unit)
            elif value > self.upperLimit:
                Notification.push(self.name.upper() + " is " + str(value) + self.unit + " higher than " + str(self.upperLimit) + self.unit)


