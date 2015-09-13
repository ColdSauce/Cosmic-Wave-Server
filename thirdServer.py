import time
import requests
IP = 'http://127.0.0.1'
PORT = '6736'



while True:
    try:
        requests.get(IP + ":" + PORT + "/recordSound/10")
    except Exception, e:
        print str(e) 
        continue
    time.sleep(10)
