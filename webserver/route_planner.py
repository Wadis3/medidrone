from cmath import pi
from flask import Flask, request, render_template, jsonify, session
from flask.globals import current_app 
from geopy.geocoders import Nominatim
from flask_cors import CORS
import redis
import json
import requests
import time

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

# change this to connect to your redis server
# ===============================================
redis_server = redis.Redis("localhost", decode_responses=True)
# ===============================================

# Example to send coords as request to the drone
def send_request(drone_url, coords):
    with requests.Session() as session:
        resp = session.post(drone_url, json=coords)

def route_planner():
    pending_requests = redis_server.lrange('requests', 0, -1)

    if len(pending_requests) == 0:
        return 'no requests'
    
    first_request = json.loads(pending_requests[0])

    user = first_request['user']
    long = first_request['longitude']
    lat =  first_request['latitude']

    ips = redis_server.smembers('ips')
    
    time.sleep(2)

    for ip in ips:
        drone = json.loads(redis_server.get(ip))
        if drone['status'] == 'idle':
            send_request('http://' + ip + ':5000/route', [long, lat])
            redis_server.lpop('requests')
            return 'Drone ' + ip + ' is delivering to ' + user
    return 'no available drones'

if __name__ == "__main__":
    while True:
        response = route_planner()
        if response != 'no requests':
            print(response)