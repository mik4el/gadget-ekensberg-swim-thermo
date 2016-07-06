import requests
import os
import serial
from time import strftime
from datetime import datetime, time


class DataPoster:

	def __init__(self, token, base_url):
		gadget_id = "1" 
		self.post_url = base_url+'/api/v1/gadgets/'+gadget_id+'/data/'
		self.headers = {'Authorization': 'Bearer '+token}

	def post_data(data):
		try:
			payload = {
				'data':data,
				'timestamp': datetime.now().isoformat()
			}
			r = requests.post(self.post_url, json=payload, headers=self.headers)
			print("Posted")
		except:
			print("Error when posting")

	def data_from_string(data_string):
		transmission_id = 57279
		temp_deep = 17.50
		temp_surface = 20.00
		battery_v = 4.04
		data = {
			'transmission_id': transmission_id, 
			'temp_deep"': temp_deep,
			'temp_surface': temp_surface,
			'battery_v': battery_v
		}
		return data

	def post_data_from_string(data_string):
		post_data(data_from_string(data_string))

username = os.environ.get('GADGET_DATA_POSTER_USERNAME', None)
password = os.environ.get('GADGET_DATA_POSTER_PASSWORD', None)
base_url = os.environ.get('GADGET_DATA_POSTER_URL', '')

try:
	login_url = base_url + '/api-token-auth/'
	credentials = {'username':username, 'password':password}
	r = requests.post(login_url, json=credentials)
	token=r.json()['token']
	print('Token received')
except:
	print('No credentials...')
	exit()

data_poster = DataPoster(token, base_url)

data_string = "57279,17.50,20.00,4.04"
data_poster.post_data_from_string(data)

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