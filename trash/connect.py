import requests
import json

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
url="https://io.adafruit.com/api/v2/an_ngdinh/feeds/demo.led/data"
data={
    "x-aio-key": "aio_fFre76W77mjdTKM2ZYiG4ly1GsOn",
    "datum": {
        "value": "ON"
    }
}

x=requests.post(url,data=json.dumps(data),headers=headers)
print(x.text)
