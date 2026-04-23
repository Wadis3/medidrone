from cmath import pi
from flask import Flask, request, render_template, jsonify
from flask.globals import current_app 
from geopy.geocoders import Nominatim
from flask_cors import CORS
import redis
import json
import requests

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

# change this to connect to your redis server
# ===============================================
redis_server = redis.Redis("localhost", decode_responses=True)
# ===============================================

geolocator = Nominatim(user_agent="my_request")
region = ", Lund, Skåne, Sweden"

# Example to send coords as request to the drone
def send_request(drone_url, coords):
    with requests.Session() as session:
        resp = session.post(drone_url, json=coords)

@app.route('/planner', methods=['POST'])
def route_planner():
    ips = redis_server.smembers('ips')

    for ip in ips:
        drone = json.loads(redis_server.get(ip))
        if drone['status'] == 'idle':
            send_request('http://' + drone + ':5000/drone', [50.361825, 35.915570])
    #print(drone_dict)
    
    return 'weee'


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5002')
