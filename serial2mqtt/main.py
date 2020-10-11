#!/bin/python3
import os
import time
import json
import logging
import threading
import sys
import paho.mqtt.client as mqtt
from serial import Serial, SerialException

# https://github.com/tonyp740613/hassio-mecer-axpert/blob/master/monitor.py
# https://github.com/bestlibre/hassio-addons/blob/master/caddy_proxy/run.sh
# https://developers.home-assistant.io/docs/add-ons/tutorial

serialdev = sys.argv[1]
serialbaud = int(sys.argv[2])
mqttserver = sys.argv[3]
mqttuser = sys.argv[4]
mqttpass = sys.argv[5]
mqtttopic = sys.argv[6]
debug = sys.argv[7] == 'true'

# buffer of data to output to the serial port
outputData = []

####  MQTT callbacks
def on_connect(client, userdata, flags, rc):
	if rc == 0:
	#rc 0 successful connect
		logging.warning('MQTT conected')
	else:
		raise Exception
	#subscribe to the output MQTT messages
	output_mid = client.subscribe(mqtttopic + "/#")
 
def on_publish(client, userdata, mid):
	if(debug):
		logging.warning('Published. mid:' + str(mid))

def on_subscribe(client, userdata, mid, granted_qos):
	if(debug):
		logging.warning('Subscribed. mid:' + str(mid))

def on_message_output(client, userdata, msg):
	if msg.topic.endswith("/set") == True:
		if(debug):
			logging.warning('Output Data: ' + msg.topic + ' data: ' + str(msg.payload))
		#add to outputData list
		outputData.append(msg)

def on_message(client, userdata, message):
	if(debug):
		logging.warning('Unhandled Message Received: ' + message.topic + ' : ' + str(message.payload))

#called on exit
#close serial, disconnect MQTT
def cleanup():
	logging.warning('Ending and cleaning up')
	ser.close()
	mqttc.disconnect()

def mqtt_to_JSON_output(mqtt_message):
	## JSON message 
	json_data = '{"topic": "' + mqtt_message.topic + '", "payload":"' + mqtt_message.payload.decode() + '"}'
	return json_data
	
#thread for reading serial data and publishing to MQTT client
def serial_read_and_publish(ser, mqttc):
	ser.flushInput()

	while True:
		line = ser.readline().decode()
		if(debug):
			logging.warning('serial in :' + str(line))
		
		# split the JSON packet up here and publish on MQTT
		json_data = json.loads(line)
		if(debug):
			logging.warning('json decoded:' + str(json_data))

		try:
			topic = str( json_data['topic'] )
			payload = str( json_data['payload'] ).replace("'",'"')
			mqttc.publish(topic, payload)
		except(KeyError):
			# TODO should probably do something here if the data is malformed
			pass

############ MAIN PROGRAM START
try:
	logging.warning('Starting')
	logging.warning('Connecting... ' + serialdev + ' at ' + str(serialbaud))
	#connect to serial port
	ser = Serial(serialdev, serialbaud, timeout=None) #timeout 0 for non-blocking. Set to None for blocking.

except SerialException as exc:
	logging.error("Unable to open serial port: %s", exc)
	logging.warning('Failed to connect serial ' + serialdev)
	#unable to continue with no serial input
	raise SystemExit

try:
	#create an mqtt client
	mqttc = mqtt.Client("serial2mqtt")
	mqttc.username_pw_set(mqttuser, mqttpass)
	#attach MQTT callbacks
	mqttc.on_connect = on_connect
	mqttc.on_publish = on_publish
	mqttc.on_subscribe = on_subscribe
	mqttc.on_message = on_message
	mqttc.message_callback_add(mqtttopic + '/#', on_message_output)

	#connect to broker
	mqttc.connect(mqttserver, 1883, 60)

	# start the mqttc client thread
	mqttc.loop_start()
	
	serial_thread = threading.Thread(target=serial_read_and_publish, args=(ser, mqttc))
	serial_thread.daemon = True
	serial_thread.start()
	
	while True: # main thread
		#writing to serial port if there is data available
		if( len(outputData) > 0 ):
			lineout = mqtt_to_JSON_output(outputData.pop()) + "\n"
			ser.write(lineout.encode())
			if(debug):
				logging.warning('=> serial:' + lineout)

		time.sleep(0.5)

# handle app closure
except (KeyboardInterrupt):
	logging.error('Interrupt received')
	cleanup()
except (RuntimeError):
	logging.warning('time to die')
	cleanup()
