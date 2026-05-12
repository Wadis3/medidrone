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
        timeout = 5 # seconds
        try:
            resp = session.post(drone_url, json=coords, timeout=timeout)
            return True
        except Exception as e:
            print("ERROR:", e)
            return False

@app.route('/new_drone', methods=['POST'])
def newDrone():
    data = request.get_json()
    drone = data.get('ip')
    base = data.get('base')
    
    coords = json.loads(redis_server.get(base))
    drone_ip = '192.168.0.' + drone

    print(coords)

    all_ok = send_request('http://' + drone_ip + ':5000/', (coords['longitude'], coords['latitude']))

    if (all_ok):
        #print(drone_ip)
        redis_server.sadd('ips', drone_ip)
        redis_server.set('drone '+drone_ip, json.dumps({
            'longitude': coords['longitude'],
            'latitude': coords['latitude'],
            'base': base,
            'status': 'idle',
            'battery': 100.0
        }))
        return 'woho'
    
    return 'Could not find drone with ip: ' + drone_ip
    #DRONE_URL = 'http://' + drone_ip + ':5001'
    #send_request(DRONE_URL, (coords['longitude'], coords['latitude']))

@app.route('/new_car', methods=['POST'])
def newCar():
    data = request.get_json()
    coords = json.loads(redis_server.get('hospital_coords'))
    car_ip = '192.168.0.' + data.get('ip')
    car_name = data.get('name')

    print(coords)

    all_ok = send_request('http://' + car_ip + ':5000/', (coords['longitude'], coords['latitude']))

    if (all_ok):
        #print(drone_ip)
        redis_server.sadd('ips', 'car '+car_ip)
        redis_server.set(car_ip, json.dumps({
            'name': car_name,
            'longitude': coords['longitude'],
            'latitude': coords['latitude']
        }))
        return 'woho'
    
    return 'Could not find car with ip: ' + car_ip
    #DRONE_URL = 'http://' + drone_ip + ':5001'
    #send_request(DRONE_URL, (coords['longitude'], coords['latitude']))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5003')