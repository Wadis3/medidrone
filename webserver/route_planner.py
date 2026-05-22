from flask import Flask, request, render_template, jsonify, session
from flask_cors import CORS
import redis
import json
import requests
import time
import math

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'
redis_server = redis.Redis("localhost", decode_responses=True)

STORAGE_URL = "http://127.0.0.1:5010"

def send_request(drone_url, coords):
    with requests.Session() as session:
        resp = session.post(drone_url, json=coords)

def update_storage(base, items, location_storage):
    for item in items:
        if item['type'] == 'blod':
            key = 'blood ' + item['blodtyp']
            available = float(location_storage.get(key, 0))
            requests.post(STORAGE_URL + '/update_Storage', json=[base, key, available - float(item['liter'])])
        elif item['type'] == 'plasma':
            available = float(location_storage.get('plasma', 0))
            requests.post(STORAGE_URL + '/update_Storage', json=[base, 'plasma', available - float(item['liter'])])
        elif item['type'] == 'forband':
            available = float(location_storage.get('bandage', 0))
            requests.post(STORAGE_URL + '/update_Storage', json=[base, 'bandage', available - float(item['antal'])])

def route_planner():
    pending_requests = redis_server.lrange('requests', 0, -1)
    if len(pending_requests) == 0:
        return 'no requests'

    first_request = json.loads(pending_requests[0])
    user = first_request['user']
    long = first_request['longitude']
    lat = first_request['latitude']
    items = first_request.get('items', [])

    ips = redis_server.smembers('ips')
    filtered = [x for x in set(ips) if x.startswith('drone ')]

    time.sleep(2)

    available_drones = [x for x in filtered if json.loads(redis_server.get(x) or '{}').get('status') == 'idle']
    if len(available_drones) == 0:
        return 'no available drones'

    drone_distances = []
    for ip in available_drones:
        drone = json.loads(redis_server.get(ip))
        drone_long = float(drone['longitude'])
        drone_lat = float(drone['latitude'])
        distance = math.sqrt((drone_long - long)**2 + (drone_lat - lat)**2)
        drone_distances.append(distance)

    closest_index = drone_distances.index(min(drone_distances))
    ip = available_drones[closest_index]
    drone = json.loads(redis_server.get(ip))
    base = drone.get('base', 'hospital_coords')

    # Kontrollera lagret
    storage_resp = requests.get(STORAGE_URL + '/get_Storage').json()
    location_storage = storage_resp.get(base, {})

    for item in items:
        if item['type'] == 'blod':
            key = 'blood ' + item['blodtyp']
            available = float(location_storage.get(key, 0))
            if available < float(item['liter']):
                print(f'Inte tillräckligt med {key} i {base} ({available} kvar)')
                return f'Inte tillräckligt med {key} i lagret'
        elif item['type'] == 'plasma':
            available = float(location_storage.get('plasma', 0))
            if available < float(item['liter']):
                print(f'Inte tillräckligt med plasma i {base} ({available} kvar)')
                return 'Inte tillräckligt med plasma i lagret'
        elif item['type'] == 'forband':
            available = float(location_storage.get('bandage', 0))
            if available < float(item['antal']):
                print(f'Inte tillräckligt med förband i {base} ({available} kvar)')
                return 'Inte tillräckligt med förband i lagret'

    # Allt finns i lagret – dra av och skicka drönaren
    update_storage(base, items, location_storage)

    print(f'Skickar drönare {ip} med bas {base} till {user}')
    send_request('http://' + ip.removeprefix('drone ') + ':5000/route', [long, lat])
    redis_server.lpop('requests')
    return 'Drone ' + ip + ' is delivering to ' + user

if __name__ == "__main__":
    while True:
        response = route_planner()
        if response != 'no requests':
            print(response)
        if 'tillräckligt' in response:
            print('Väntar på lager...')
            time.sleep(10)  # Vänta innan nästa försök