import unittest
from data_poster import DataPosterWorker


class TestDataPosterWorker(unittest.TestCase):
	def setUp(self):
		self.token = 'eyJaaGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjasLCJ1c2VybmFtZSI6Im1pazRlbCIsImVtYWlsIjoibWlrNGVsLjRuZGVyc3NvbkBnbWFpbC5jb20iLCJleHAiOjE0NjkwODkxMjIsIm9yaWdfaWF0IjoxNDY3ODc5NTIyfQ.ekFnrBFR5DosdDvwNf5u3-shOMtNFkQWTTAvCINd3pY'
		base_url = 'https://m4bd.se'
		self.data_string = "57279,17.50,20.00,4.04"
		self.data_poster = DataPosterWorker(self.token, base_url, self.data_string)

	def test_values_set(self):
		self.assertEqual(self.data_poster.post_url, 'https://m4bd.se/api/v1/gadgets/1/data/')
		self.assertEqual(self.data_poster.headers['Authorization'], 'Bearer '+ self.token)
		self.assertEqual(self.data_poster.data_string, self.data_string)

	def test_data_from_string(self):
		data_string = "57279,17.50,20.00,4.04"
		data = self.data_poster.data_from_string(data_string)
		self.assertEqual(data['transmission_id'], 57279)
		self.assertEqual(data['temp_deep'], 17.50)
		self.assertEqual(data['temp_surface'], 20.00)
		self.assertEqual(data['battery_v'], 4.04)

		data_string = "57273,15.50,10.00,2.04"
		data = self.data_poster.data_from_string(data_string)
		self.assertEqual(data['transmission_id'], 57273)
		self.assertEqual(data['temp_deep'], 15.50)
		self.assertEqual(data['temp_surface'], 10.00)
		self.assertEqual(data['battery_v'], 2.04)

		data_string = "a57273,15.50,10.00,2.04"  # args not number
		data = self.assertRaises(Exception, self.data_poster.data_from_string, data_string)
		
		data_string = "57273,15.50,10.00"  # to few args
		data = self.assertRaises(Exception, self.data_poster.data_from_string, data_string)
		