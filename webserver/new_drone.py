from flask import Flask, request
from flask_cors import CORS
import redis
import json
import requests

app = Flask(__name__)
CORS(app)

redis_server = redis.Redis("localhost", decode_responses=True)

def send_request(drone_url, coords):
    with requests.Session() as session:
        resp = session.post(drone_url, json=coords)

@app.route('/new_drone', methods=['POST'])
def newDrone():
    print("test")
    coords = json.loads(redis_server.get('hospital_coords'))
    drone_ip = '192.168.0.' + request.get_json()

    send_request('http://' + drone_ip + ':5000/')

    #print(drone_ip)
    redis_server.sadd('ips', drone_ip)
    redis_server.set(drone_ip, json.dumps({
        'longitude': coords['longitude'],
        'latitude': coords['latitude'],
        'status': 'idle'
    }))
    return 'woho'
    #DRONE_URL = 'http://' + drone_ip + ':5001'
    #send_request(DRONE_URL, (coords['longitude'], coords['latitude']))