from os import fdopen
from flask import Flask, render_template, request
from flask.json import jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import time
import redis
import pickle
import json
import math

app = Flask(__name__)
CORS(app)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

# change this so that you can connect to your redis server
# ===============================================
redis_server = redis.Redis("localhost", decode_responses=True)
# ===============================================

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
    return render_template('index.html')

@app.route('/booking', methods=['GET'])
def booking():
    return render_template('booking.html')

@app.route('/addDronePage', methods=['GET'])
def addDronePage():
    return render_template('addDrone.html')

@app.route('/get_drones', methods=['GET'])
def get_drones():
    #=============================================================================================================================================
    # Get the information of all the drones from redis server and update the dictionary `drone_dict' to create the response 
    # drone_dict should have the following format:
    # e.g if there are two drones in the system with IDs: DRONE1 and DRONE2
    # drone_dict = {'DRONE_1':{'longitude': drone1_logitude_svg, 'latitude': drone1_logitude_svg, 'status': drone1_status},
    #               'DRONE_2': {'longitude': drone2_logitude_svg, 'latitude': drone2_logitude_svg, 'status': drone2_status}
    #              }
    # use function translate() to covert the coodirnates to svg coordinates
    #=============================================================================================================================================
    gorilla = json.loads(redis_server.get('Gorilla'))
    zebra = json.loads(redis_server.get('Zebra'))
    coordsG = translate((float(gorilla['longitude']), float(gorilla['latitude'])))
    coordsZ = translate((float(zebra['longitude']), float(zebra['latitude'])))
    drone_dict = {
                    'Gorilla':{
                        'longitude': coordsG[0],
                        'latitude': coordsG[1],
                        'status': gorilla['status']},
                    'Zebra': {
                        'longitude': coordsZ[0], 
                        'latitude': coordsZ[1], 
                        'status': zebra['status']}
                }
    #print(drone_dict)
    
    return jsonify(drone_dict)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000')
