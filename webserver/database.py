from flask import Flask, request
from flask_cors import CORS
import redis
import json
import requests

app = Flask(__name__)
CORS(app)

redis_server = redis.Redis("localhost", decode_responses=True)

@app.route('/drone', methods=['POST'])
def drone():
    drone = request.get_json()
    droneIP = drone['ip']
    drone_longitude = drone['longitude']
    drone_latitude = drone['latitude']
    drone_status = drone['status']
    drone_battery = drone['battery']
    
    # Hämta befintlig data för att behålla base
    existing = redis_server.get('drone ' + droneIP)
    drone_base = json.loads(existing).get('base') if existing else None
    
    redis_server.set('drone ' + droneIP, json.dumps({
        'ip': droneIP,
        'longitude': drone_longitude,
        'latitude': drone_latitude,
        'base': drone_base,
        'status': drone_status,
        'battery': drone_battery
    }))
    return 'Updated'

@app.route('/car', methods=['POST'])
def car():
    data = request.get_json()
    carIP = data['IP']
    car_long = data['longitude']
    car_lat = data['latitude']
    
    existing = redis_server.get('car ' + carIP)
    car_name = json.loads(existing).get('name') if existing else None
    
    redis_server.set('car ' + carIP, json.dumps({
        'ip': carIP,
        'name': car_name,
        'longitude': car_long,
        'latitude': car_lat
    }))
    
    if car_name:
        base_data = json.loads(redis_server.get(car_name) or '{}')
        base_data['longitude'] = car_long
        base_data['latitude'] = car_lat
        redis_server.set(car_name, json.dumps(base_data))
        
        all_ips = redis_server.smembers('ips')
        drone_ips = [x.removeprefix('drone ') for x in all_ips if x.startswith('drone ')]
        for drone_ip in drone_ips:
            drone_data = json.loads(redis_server.get('drone ' + drone_ip) or '{}')
            if drone_data.get('base') == car_name:
                try:
                    requests.post(
                        f'http://{drone_ip}:5001/base',
                        json=[car_long, car_lat],
                        timeout=2
                    )
                    if drone_data['status'] == 'idle':
                        drone_data['longitude'] = car_long
                        drone_data['latitude'] = car_lat
                    redis_server.set('drone '+drone_ip, json.dumps(drone_data))
                except Exception as e:
                    print(f'Kunde inte uppdatera bas för {drone_ip}:', e)
    
    return 'Updated'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5001')
