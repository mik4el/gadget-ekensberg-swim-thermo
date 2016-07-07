import os
import serial
from time import strftime
import requests
from datetime import datetime
import threading

class DataAuther:

	def __init__(self, username, password, base_url):
		gadget_id = "1" 
		self.login_url = base_url + '/api-token-auth/'
		self.username = username
		self.password = password
		self.token = None

	def auth_and_get_token(self):
		try:
			credentials = {'username':self.username, 'password':self.password}
			r = requests.post(self.login_url, json=credentials)
			self.token=r.json()['token']
		except:
			self.token=None
		return self.token


class DataPosterWorker(threading.Thread):

	def __init__(self, token, base_url, data_string):
		threading.Thread.__init__(self)
		gadget_id = "1" 
		self.post_url = base_url+'/api/v1/gadgets/'+gadget_id+'/data/'
		self.headers = {'Authorization': 'Bearer '+ token}
		self.data_string = data_string

	def run(self):
		if self.data_string != "Setup complete!":
			self.post_data_from_string(self.data_string)

	def post_data(self, data):
		try:
			payload = {
				'data':data,
				'timestamp': datetime.now().isoformat()
			}
			r = requests.post(self.post_url, json=payload, headers=self.headers)
		except:
			raise Exception("Error when posting")

	def to_number(self, s):
		try:
			return int(s)
		except ValueError:
			return float(s)
			
	def data_from_string(self, data_string):
		try:
			f = lambda x: self.to_number(x)
			data_list = [f(x) for x in data_string.split(',')]
			last = data_list[3]
		except:
			raise Exception('Not valid data "' + data_string+'"')

		transmission_id = data_list[0]
		temp_deep = data_list[1]
		temp_surface = data_list[2]
		battery_v = data_list[3]
		data = {
			'transmission_id': transmission_id, 
			'temp_deep': temp_deep,
			'temp_surface': temp_surface,
			'battery_v': battery_v
		}
		return data

	def post_data_from_string(self, data_string):
		self.post_data(self.data_from_string(data_string))

if __name__ == '__main__':
	username = os.environ.get('GADGET_DATA_POSTER_USERNAME', None)
	password = os.environ.get('GADGET_DATA_POSTER_PASSWORD', None)
	base_url = os.environ.get('GADGET_DATA_POSTER_URL', '')

	data_auther = DataAuther(username, password, base_url)
	token = data_auther.auth_and_get_token()

	if token is None:
		print("No token")
		exit()

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
				line = line.decode('ascii')
				data_poster = DataPosterWorker(token, base_url, line)
				data_poster.start()
				log_message = "{:%Y-%m-%d %H:%M} {}" .format(datetime.now(),line)
				with open('temp_sensor.log','a') as logfile:
					logfile.write(log_message)
				print(log_message)
	except KeyboardInterrupt:
		print("\ndone")