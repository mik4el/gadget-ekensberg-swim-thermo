import requests
from datetime import datetime, time
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