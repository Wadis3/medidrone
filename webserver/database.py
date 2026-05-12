from flask import Flask, request
from flask_cors import CORS
import redis
import json


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
    
    data = {
        'IP': droneIP,
        'longitude': drone_longitude,
        'latitude': drone_latitude,
        'status': drone_status,
        'battery': drone_battery
    }
    redis_server.set('drone '+droneIP, json.dumps(data))
    
    return 'Get data'

@app.route('/car', methods=['POST'])
def car():
    car = request.get_json()
    carIP = car['IP']
    car_long = car['longitude']
    car_lat = car['latitude']

    car_name = json.loads(redis_server.get('car '+carIP)).get('name')

    data = {
        'IP': carIP,
        'name': car_name,
        'longitude': car_long,
        'latitude': car_lat
    }

    redis_server.set('car '+carIP, json.dumps(data))

    return 'Updated'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5001')
