from flask import Flask, request
from flask_cors import CORS
from sense_hat import SenseHat
import subprocess
import redis
import requests

sense = SenseHat()
redis_server = redis.Redis('localhost', decode_responses=True)

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

myIP = '192.168.0.4'
stepSize = 50/111111

SERVER_URL = "http://192.168.0.2:5001/car"

coords = []

#coords = [float(redis_server.get('long')), float(redis_server.get('lat'))]

@app.route('/', methods=['POST'])
def main():
	coords = request.json
	
	subprocess.Popen(["python3", "simulator.py", '--ip', myIP])

	redis_server.set('long', coords[0])
	redis_server.set('lat', coords[1])
	while True:
	    event = sense.stick.wait_for_event()
	    if event.direction =="right":
	        coords[0] = coords[0] + stepSize

	    elif event.direction == "left":
	        coords[0] = coords[0] - stepSize

	    elif event.direction == "down":
	        coords[1] = coords[1] + stepSize

	    elif event.direction == "up":
	        coords[1] = coords[1] - stepSize

	    with requests.Session() as session:
	        car_info = {
	            'IP': myIP,
	            'longitude': coords[0],
	            'latitude': coords[1]
	        }
	        resp = session.post(SERVER_URL, json=car_info)

	    redis_server.set('long', coords[0])
	    redis_server.set('lat', coords[1])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
