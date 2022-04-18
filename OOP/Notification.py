import requests
import datetime

class Notification:
    @staticmethod
    def push(content):
        date = datetime.datetime.now()
        data = {'content': content,'date': date}
        x = requests.post("https://iot-do-an-api.herokuapp.com/noti", data = data)
        print(x.text)
        return x.text

