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
        resp = session.post(drone_url, json=coords)

@app.route("/newDrone" methods=['POST'])
def newDrone():
    coords = redis_server.get("hospital_coords")
    drone_ip = request.get_json()
    DRONE_URL = 'http://' + DRONE_IP + ':5000'
    send_request(DRONE_URL, (coords['longitude'], coords['latitude']))