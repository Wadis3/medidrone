from flask import Flask, render_template, request
from flask.json import jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import redis
import json

app = Flask(__name__)
CORS(app)

redis_server = redis.Redis("localhost", 6380, decode_responses=True)

@app.route('/', methods=['GET']) 
def bank():
    return render_template('index.html')

def update_storage(location, product, amount):
    existing = redis_server.get(location)
    products = json.loads(existing) if existing else {}
    products[product] = amount
    redis_server.sadd('locations', location)
    redis_server.set(location, json.dumps(products))

@app.route('/update_Storage', methods=['POST'])
def update_storage_request():
    update = request.json
    location = update[0]
    product = update[1]
    amount = update[2]

    update_storage(location, product, amount)

    return 'updated'

@app.route('/get_Storage', methods=['GET'])
def get_Storage():
    locations = redis_server.smembers('locations')

    storage_dict = {}
    for location in locations:
        storage_dict[location] = {}
        products = json.loads(redis_server.get(location))
        for product in products:
            storage_dict[location][product] = products[product]
            
    return jsonify(storage_dict)

update_storage('hospital_coords', 'blood A', 70)
update_storage('hospital_coords', 'blood B', 70)
update_storage('hospital_coords', 'blood AB', 70)
update_storage('hospital_coords', 'blood O', 70)
update_storage('hospital_coords', 'plasma', 70)
update_storage('hospital_coords', 'bandage', 70)

update_storage('car4', 'blood A', 70)
update_storage('car4', 'blood B', 70)
update_storage('car4', 'blood AB', 70)
update_storage('car4', 'blood O', 70)
update_storage('car4', 'plasma', 70)
update_storage('car4', 'bandage', 70)

update_storage('car3', 'blood A', 70)
update_storage('car3', 'blood B', 70)
update_storage('car3', 'blood AB', 70)
update_storage('car3', 'blood O', 70)
update_storage('car3', 'plasma', 70)
update_storage('car3', 'bandage', 70)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5010')

