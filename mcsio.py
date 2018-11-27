#!/usr/bin/env python
import time
import sys
import httplib, urllib
import json
import RPi.GPIO as GPIO

deviceId = "D360XOPV"
deviceKey = "BCve1urEYIIvzVNI"

def post_to_mcs(payload):
	headers = {"Content-type": "application/json", "deviceKey":deviceKey}
	not_connected = 1
	while (not_connected):
		try:
			httpClient = httplib.HTTPConnection("api.mediatek.com:80")
			httpClient.connect()
			not_connected = 0
		except (httplib.client.HTTPException, socket.error) as ex:
			print ("Error: %s" % ex)
			time.sleep(10)
			# sleep 10 seconds
	httpClient.request("POST", "/mcs/v2/devices/" + deviceId + "/datapoints", json.dumps(payload), headers)
	response = httpClient.getresponse()
	print( response.status, response.reason, json.dumps(payload), time.strftime("%c"))
	data = response.read()
	httpClient.close()

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True :
	Switch = GPIO.input(24)
	if (Switch==0):
		print('Button pressed!')
		payload = {"datapoints":[{"dataChnId":"Switch","values":{"value":Switch}}]}
		post_to_mcs(payload)
	else:
		print('Button released!')
sys.exit(1)
