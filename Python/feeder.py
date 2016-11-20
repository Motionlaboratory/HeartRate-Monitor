import paho.mqtt.client as mqtt
import CsvLoader
import time

from PanTom import Detector
detector = Detector()

CLIENT_ID = '02WXO01'

data_csv = CsvLoader.load()
client = mqtt.Client(client_id=CLIENT_ID)
client.connect("localhost", 1883, 60)

# device_id = msg.topic.split('/')[1]
device_id = "02WXO01"

for raw in data_csv:
   data = detector.add_data(float(raw))
   if data[0] != 'filling':
	
	# send bpm for the first time
	bpm = round(float(sum(data[7])) / len(data[7]), 2)
	# client.publish("bpm/"+device_id, bpm, qos=2)  # ini bikin errorr
	client.publish("bpm/"+device_id, bpm)

	for filtered_data in data[0]:
		print "forwarding data to dashboard", filtered_data
		client.publish("visual/"+device_id, filtered_data)
		# client.publish("visual/"+device_id, filtered_data, qos=2)

		time.sleep(0.010)

		# break this if you want direct get alert without visualization
		# break

	# Sent alert after
	alert_data = {}

	alert_data['PVC'] = True if True in data[1] else False
	alert_data['PAC'] = True if True in data[2] else False
	alert_data['BUNDLE_BRANCH'] = True if True in data[3] else False
	alert_data['AtrialTachycardia'] = bool(data[4][0])
	alert_data['VentricularTachycardia'] = bool(data[5][0])
	alert_data['BundleBranchBlock'] = bool(data[6][0])
	alert_data['bpm'] = round(float(sum(data[7])) / len(data[7]), 2)