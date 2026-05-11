from cmath import pi
from flask import Flask, request, render_template, jsonify, session
from flask.globals import current_app 
from geopy.geocoders import Nominatim
from flask_cors import CORS
import redis
import json
import requests
import time

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

redis_server = redis.Redis("localhost", decode_responses=True)

@app.route('/new_request', methods=['POST'])
def new_request():
    user = request.json.get('user')
    user_data = json.loads(redis_server.get(user))
    long = float(user_data['longitude'])
    lat =  float(user_data['latitude'])

    redis_server.rpush('requests', json.dumps({
            'user': user,
            'longitude': long,
            'latitude': lat
        }))
    
    place_in_line = redis_server.llen('requests')
    
    return 'Your request has line number ' + str(place_in_line)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5004')