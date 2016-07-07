import os
import serial
from time import strftime
from datetime import datetime, time
from data_poster import DataAuther, DataPosterWorker

if __name__ == '__main__':
	username = os.environ.get('GADGET_DATA_POSTER_USERNAME', None)
	password = os.environ.get('GADGET_DATA_POSTER_PASSWORD', None)
	base_url = os.environ.get('GADGET_DATA_POSTER_URL', '')

	data_auther = DataAuther(username, password, base_url)
	token = data_auther.auth_and_get_token()

	if token is not None:
		data_string = "57279,17.50,20.00,4.04"
		data_poster = DataPosterWorker(token, base_url, data_string)
		data_poster.start()
	else:
		print("No token")

'''
Main thread

try:
	ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # linux address
except:
	try:
		ser = serial.Serial('/dev/cu.wchusbserialfd130', 9600, timeout=1)  # osx address 2
	except:
		ser = serial.Serial('/dev/cu.wchusbserial1410', 9600, timeout=1)  # osx address 1 

try:
	while 1:
		line=ser.readline().rstrip()
		if len(line)>0: 
			now = datetime.now()
			print("%s %s"%(now.strftime("%Y-%m-%d %H:%M:%S"),line))
			f=open('temp_sensor.log','a')
			print >> f, ("%s %s"%(now.strftime("%Y-%m-%d %H:%M:%S"),line))
			f.close()
except KeyboardInterrupt:
	print("\ndone")
'''