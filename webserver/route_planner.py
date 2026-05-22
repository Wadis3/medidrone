from cmath import pi
from flask import Flask, request, render_template, jsonify, session
from flask.globals import current_app 
from geopy.geocoders import Nominatim
from flask_cors import CORS
import redis
import json
import requests
import time
import math

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
    filtered = [x for x in set(ips) if x.startswith('drone ')]
    
    print(ips)
    time.sleep(2)
#FRÅN
    availableDrones = [x for x in filtered if json.loads(redis_server.get(ip))['status']=='idle']
    if len(availableDrones) == 0:
        return 'no available drones'

    droneDistances = []
    for ip in availableDrones:
        drone = json.loads(redis_server.get(ip))
        if drone['status'] == 'idle':
            drone_long = float(drone['longitude'])
            drone_lat = float(drone['latitude'])
            distance = math.sqrt((drone_long - long)**2 + (drone_lat - lat)**2)
            available_drones.append(ip)
            drone_distances.append(distance)

    closest_index = drone_distances.index(min(drone_distances))
    ip = available_drones[closest_index]
    
    send_request('http://' + ip + ':5000/route', [long, lat])
    redis_server.lpop('requests')
    return 'Drone ' + ip + ' is delivering to ' + user
        
        
# def route_planner():
#     pending_requests = redis_server.lrange('requests', 0, -1)
#     if len(pending_requests) == 0:
#         return 'no requests'
    
#     first_request = json.loads(pending_requests[0])
#     user = first_request['user']
#     long = first_request['longitude']
#     lat = first_request['latitude']
    
    #ips = redis_server.smembers('ips')
    #filtered = [x.removeprefix('drone ') for x in set(ips) if x.startswith('drone ')]
    
    #available_drones = []
    #drone_distances = []
    
    # for ip in filtered:
    #     drone = json.loads(redis_server.get('drone ' + ip))
    #     print(drone)
    #     if drone['status'] == 'idle':
    #         drone_long = float(drone['longitude'])
    #         drone_lat = float(drone['latitude'])
    #         distance = math.sqrt((drone_long - long)**2 + (drone_lat - lat)**2)
    #         available_drones.append(ip)
    #         drone_distances.append(distance)
    
    # if len(available_drones) == 0:
    #     return 'no available drones'
    
    # closest_index = drone_distances.index(min(drone_distances))
    # ip = available_drones[closest_index]
    
    # send_request('http://' + ip + ':5000/route', [long, lat])
    # redis_server.lpop('requests')
    # return 'Drone ' + ip + ' is delivering to ' + user

if __name__ == "__main__":
    while True:
        response = route_planner()
        if response != 'no requests':
            print(response)