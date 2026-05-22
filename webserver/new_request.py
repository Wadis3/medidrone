from flask import Flask, request, jsonify
from flask_cors import CORS
import redis
import json
import requests

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'
redis_server = redis.Redis("localhost", decode_responses=True)

STORAGE_URL = "http://127.0.0.1:5010"

def get_storage():
    resp = requests.get(STORAGE_URL + '/get_Storage')
    return resp.json()

def update_storage(location, product, amount):
    requests.post(STORAGE_URL + '/update_Storage', json=[location, product, amount])

def get_drone_location(user):
    user_data = json.loads(redis_server.get(user))
    base = user_data.get('base', 'hospital_coords')
    return base

@app.route('/new_request', methods=['POST'])
def new_request():
    data = request.json
    user = data.get('user')
    items = data.get('items', [])

    user_data = json.loads(redis_server.get(user))
    long = float(user_data['longitude'])
    lat = float(user_data['latitude'])

    redis_server.rpush('requests', json.dumps({
        'user': user,
        'longitude': long,
        'latitude': lat,
        'items': items
    }))

    place_in_line = redis_server.llen('requests')
    return 'Din beställning har könummer ' + str(place_in_line)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5004')