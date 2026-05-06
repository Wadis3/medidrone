from flask import Flask, render_template, request
from flask.json import jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import redis
import json

app = Flask(__name__)
CORS(app)

redis_server = redis.Redis("localhost", decode_responses=True)

@app.route('/', methods=['GET'])
def bank():
    return render_template('bank.html')

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

    # storage = {
    # location = {
    # bandage = 10
    # blood = 5
    #}
    #}
    #
    #


#ips = redis_server.smembers('ips')
#    drone_dict = {}
#    for ip in ips:
#        drone = json.loads(redis_server.get(ip))
#        drone_dict[ip] = {
#                'longitude': drone['longitude'],
#                'latitude': drone['latitude'],
#               'status': drone['status'],
#               'battery': drone['battery']
#               }
#   return jsonify(drone_dict)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000')

