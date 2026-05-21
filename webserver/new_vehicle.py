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
    base = data.get('base')  # Namnet på basen, t.ex. "Volvo 1"
    
    base_data = redis_server.get(base)
    if base_data is None:
        return f'Basen "{base}" finns inte', 404
    
    coords = json.loads(base_data)
    drone_ip = '192.168.0.' + drone
    
    all_ok = send_request('http://' + drone_ip + ':5000/', (coords['longitude'], coords['latitude']))
    if all_ok:
        redis_server.sadd('ips', 'drone ' + drone_ip)
        redis_server.set('drone ' + drone_ip, json.dumps({
            'longitude': coords['longitude'],
            'latitude': coords['latitude'],
            'base': base,
            'status': 'idle',
            'battery': 100.0
        }))
        return 'woho'
    return 'Could not find drone with ip: ' + drone_ip

@app.route('/new_car', methods=['POST'])
def newCar():
    data = request.get_json()
    car_ip = '192.168.0.' + data.get('ip')
    car_name = data.get('name')
    
    # Hämta sjukhuskoordinater som startposition
    coords = json.loads(redis_server.get('hospital_coords'))
    
    all_ok = send_request('http://' + car_ip + ':5003/', (coords['longitude'], coords['latitude']))
    if all_ok:
        redis_server.sadd('ips', 'car ' + car_ip)
        redis_server.sadd('bases', car_name)
        redis_server.set('car ' + car_ip, json.dumps({
            'name': car_name,
            'longitude': coords['longitude'],
            'latitude': coords['latitude']
        }))
        # Spara basen med bilens namn som nyckel så drönare kan hämta koordinater
        redis_server.set(car_name, json.dumps({
            'ip': car_ip,
            'longitude': coords['longitude'],
            'latitude': coords['latitude']
        }))
        return 'woho'
    return 'Could not find car with ip: ' + car_ip

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5003')