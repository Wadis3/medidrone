from os import fdopen
from flask import Flask, render_template, request, redirect, url_for, session
from flask.json import jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import redis
import json
import math
import requests

app = Flask(__name__)
CORS(app)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

# change this so that you can connect to your redis server
# ===============================================
redis_server = redis.Redis("localhost", decode_responses=True)
# ===============================================

redis_server.set('hospital_coords', json.dumps({
    'longitude': 49.97425,
    'latitude': 36.1960665,
}))

#redis_server.sadd('ips', '192.168.0.3')

# Translate OSM coordinate (longitude, latitude) to SVG coordinates (x,y).
# Input coordsG_osm is a tuple (longitude, latitude).
@app.route('/', methods=['GET'])
def map():
    user = session.get('user')
    if not user:
        session['error'] = 'Need to login to view map'
        return redirect(url_for('login'))
    return render_template('index.html', user = user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    user = session.get('user')
    
    if not user or user != 'admin':
        session['error'] = "Admin-access krävs för registrering"
        return redirect(url_for('login')) 
    
    if request.method == 'POST':
        user = request.form.get('username')

        if user == 'admin':
            return render_template('register.html', error="Fel användarnamn eller lösenord")

        pw = request.form.get('password')
        long = request.form.get('longitude')
        lat = request.form.get('latitude')

        redis_server.sadd('users', user)
        
        redis_server.set(user, json.dumps({
            'password': pw,
            'longitude': long,
            'latitude': lat
        }))
        
        return redirect(url_for('map'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = session.pop('error', None)  # Flyttad hit, läses vid både GET och POST
    if request.method == 'POST':
        user = request.form.get('username')
        pw = request.form.get('password')
        user_data = redis_server.get(user)
        if user_data is not None:
            user_data = json.loads(user_data)  # Parsa JSON här
            if user_data['password'] == pw:
                session['user'] = user
                return redirect(url_for('map'))
        session.pop('user', None)
        return render_template('login.html', error="Fel användarnamn eller lösenord")
    
    return render_template('login.html', error=error)

@app.route('/booking', methods=['GET'])
def booking():
    user = session.get('user')
    if not user or user == 'admin':
        session['error'] = 'Only common users can book supplies'
        return redirect(url_for('login'))
    return render_template('booking.html', user=user)

@app.route('/addDronePage', methods=['GET'])
def addDronePage():
    user = session.get('user')
    if not user or user != 'admin':
        session['error'] = 'Admin-access required'
        return redirect(url_for('login'))
    return render_template('addDrone.html')

@app.route('/addCarPage', methods=['GET'])
def addCarPage():
    user = session.get('user')
    if not user or user != 'admin':
        session['error'] = 'Admin-access required'
        return redirect(url_for('login'))
    return render_template('addCar.html')

@app.route('/get_drones', methods=['GET'])
def get_drones():
    ips = redis_server.smembers('ips')
    filtered = [x.removeprefix('drone ') for x in set(ips) if x.startswith('drone ')]
    drone_dict = {}
    for ip in filtered:
        try: 
            #with requests.Session() as session:
            #    timeout = 5
            #    resp = session.post('http://' + ip + ':5000/ping', timeout=timeout)
            drone = json.loads(redis_server.get('drone '+ip))
            drone_dict[ip] = {
                    'longitude': drone['longitude'],
                    'latitude': drone['latitude'],
                    'base': drone['base'],
                    'status': drone['status'],
                    'battery': drone['battery']
            }
        except:
            print(ip, 'not available')
    
    return jsonify(drone_dict)

@app.route('/get_cars', methods=['GET'])
def get_cars():
    ips = redis_server.smembers('ips')
    filtered = [x.removeprefix('car ') for x in set(ips) if x.startswith('car ')]
    car_dict = {}
    for ip in filtered:
        try:
            car = json.loads(redis_server.get('car '+ip))
            car_dict[ip] = {
                    'longitude': car['longitude'],
                    'latitude': car['latitude']
            }
        except:
            print(ip, 'not available')
    
    return jsonify(car_dict)

@app.route('/get_field', methods=['GET'])
def get_field():
    users = redis_server.smembers('users')
    field_dict = {}
    for user in users:
        user_data = json.loads(redis_server.get(user))
        field_dict[user] = {
            'longitude': user_data['longitude'],
            'latitude': user_data['latitude']
        }
    
    return jsonify(field_dict)

@app.route('/get_requests', methods=['GET'])
def get_requests():
    requests = redis_server.lrange('requests', 0, -1)
    return jsonify(requests)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000')