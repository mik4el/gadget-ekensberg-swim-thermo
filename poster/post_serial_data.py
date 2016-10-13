import os
import serial
import requests
from datetime import datetime
import threading
import queue


class DataAuther:
    def __init__(self, username, password, base_url):
        self.login_url = base_url + '/backend/api-token-auth/'
        self.username = username
        self.password = password
        self.token = None

    def auth_and_get_token(self):
        credentials = {'username': self.username, 'password': self.password}
        r = requests.post(self.login_url, json=credentials)
        self.token = r.json()['token']
        return self.token


class DataPosterWorker(threading.Thread):
    def __init__(self, token, base_url, data_string, status_queue):
        threading.Thread.__init__(self)
        gadget_slug = "ekensberg-swim-thermo"
        self.post_url = base_url + '/backend/api/v1/gadgets/' + gadget_slug + '/data/'
        self.headers = {'Authorization': 'Bearer ' + token}
        self.data_string = data_string
        self.status_queue = status_queue

    def run(self):
        if self.data_string != "Setup complete!":
            self.post_data_from_string(self.data_string)

    def post_data(self, data):
        payload = {
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        try:
            r = requests.post(self.post_url, json=payload, headers=self.headers)
        except:
            self.update_status("Error when posting.")
            return
        if r.status_code != 201:
            self.update_status(r.status_code)
            self.update_status(r.json())
            self.update_status("Request not ok when posting.")
        else:
            self.update_status("Posted: '{}'".format(data))

    def update_status(self, message):
        self.status_queue.put(message)

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
            raise Exception('Not valid data "' + data_string + '"')

        transmission_id = data_list[0]
        temp_air = data_list[1]
        temp_surface = data_list[2]
        battery_v = data_list[3]
        data = {
            'transmission_id': transmission_id,
            'temp_air': temp_air,
            'temp_surface': temp_surface,
            'battery_v': battery_v
        }
        return data

    def post_data_from_string(self, data_string):
        self.post_data(self.data_from_string(data_string))


if __name__ == '__main__':
    print("Started...")	
 
    username = os.environ.get('GADGET_DATA_POSTER_USERNAME', None)
    password = os.environ.get('GADGET_DATA_POSTER_PASSWORD', None)
    base_url = os.environ.get('GADGET_DATA_POSTER_URL', '')

    status_queue = queue.Queue()
    data_auther = DataAuther(username, password, base_url)
    token = data_auther.auth_and_get_token()

    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # linux address
    except:
        try:
            ser = serial.Serial('/dev/cu.wchusbserialfd130', 9600, timeout=1)  # osx address 2
        except:
            try:
                ser = serial.Serial('/dev/cu.wchusbserial1410', 9600, timeout=1)  # osx address 1
            except:
                print("No more serial ports to try. Exiting.")
                exit()

    print("Serial connected...")

    try:
        while True:
            while not status_queue.empty():
                try:
                    message = status_queue.get()
                except queue.Empty:
                    pass
                else:
                    print("{:%Y-%m-%d %H:%M} {}".format(datetime.now(), message))
                    if message == "Request not ok when posting.":
                        # reauth
                        token = data_auther.auth_and_get_token()
                        print("Token updated.")
                        with status_queue.mutex:
                            status_queue.queue.clear()

            line = ser.readline().rstrip()
            if len(line) > 0:
                line = line.decode('ascii')
                data_poster = DataPosterWorker(token, base_url, line, status_queue)
                data_poster.start()
                log_message = "{:%Y-%m-%d %H:%M} {}".format(datetime.now(), line)
                with open('temp_sensor.log', 'a') as logfile:
                    print(log_message, file=logfile)
                print(log_message)
    except KeyboardInterrupt:
        print("Done")
