from flask import Flask, request
from flask_cors import CORS
from sense_hat import SenseHat
import subprocess
import redis
import requests
import argparse

sense = SenseHat()
redis_server = redis.Redis('localhost', decode_responses=True)

def run(ip, SERVER_URL):
    coords = (redis_server.get('long'), redis_server.get('lat'))
    stepSize = 50/111111

    while True:
        event = sense.stick.wait_for_event()
        if event.direction =="right":
            coords[0] = coords[0] + stepSize

        elif event.direction == "left":
            coords[0] = coords[0] - stepSize

        elif event.direction == "down":
            coords[1] = coords[1] + stepSize

        elif event.direction == "up":
            coords[1] = coords[1] - stepSize

        with requests.Session() as session:
            car_info = {
                'IP': myIP,
                'longitude': coords[0],
                'latitude': coords[1]
            }
            resp = session.post(SERVER_URL, json=car_info)

        redis_server.set('long', coords[0])
        redis_server.set('lat', coords[1])

    return 'wassaaaa'
   
if __name__ == "__main__":
    SERVER_URL = "http://192.168.0.2:5001/car"

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", help ='drones ID' ,type=str)
    args = parser.parse_args()
    drone_long, drone_lat, final_battery = run(args.ip, SERVER_URL)
    
