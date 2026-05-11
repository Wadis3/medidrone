from os import fdopen
from flask import Flask, render_template, request, redirect, url_for, session
from flask.json import jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import redis
import json
import math

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
def delta_coords(meters, angle, current):
    y_meters = meters * math.sin(angle)
    x_meters = meters * math.cos(angle)

    d_long = y_meters / 111111
    d_lat = x_meters / (111111 * math.cos(d_long + current[0]))

    return (current[0] + d_long, current[1] + d_lat)

@app.route('/', methods=['GET'])
def map():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))
    return render_template('index.html', user = user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    user = session.get('user')
    
    if not user or user != 'admin':
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
    if request.method == 'POST':
        user = request.form.get('username')
        pw = request.form.get('password')
        
        user_data = json.loads(redis_server.get(user))

        if user_data is not None and user_data['password'] == pw:
            session['user'] = user
            return redirect(url_for('map'))
        
        session.pop('user', None)
        return render_template('login.html', error="Fel användarnamn eller lösenord")
    
    return render_template('login.html')

@app.route('/booking', methods=['GET'])
def booking():
    user = session.get('user')
    if not user or user == 'admin':
        return redirect(url_for('login'))
    return render_template('booking.html', user=user)

@app.route('/addDronePage', methods=['GET'])
def addDronePage():
    user = session.get('user')
    if not user or user != 'admin':
        return redirect(url_for('login'))
    return render_template('addDrone.html')

@app.route('/get_drones', methods=['GET'])
def get_drones():
    ips = redis_server.smembers('ips')
    drone_dict = {}
    for ip in ips:
        drone = json.loads(redis_server.get(ip))
        drone_dict[ip] = {
                'longitude': drone['longitude'],
                'latitude': drone['latitude'],
                'status': drone['status'],
                'battery': drone['battery']
        }
    #print(drone_dict)
    
    return jsonify(drone_dict)

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
