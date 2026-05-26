from flask import Flask, request
from flask_cors import CORS
import subprocess
import redis
import requests

redis_server = redis.Redis('localhost', decode_responses=True)

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

myIP = '192.168.0.3'
battery = 100.0

@app.route('/', methods=['POST'])
def main():
    coords = request.json
    
    redis_server.set('longitude', coords[0])
    redis_server.set('latitude', coords[1])
    redis_server.set('battery', battery)
    with requests.Session() as session:
        resp = session.post('http://' + myIP + ':5001/base', json=coords)
        
    return 'OK'

@app.route('/ping', methods=['POST'])
def ping():
    return 'ping'

@app.route('/route', methods=['POST'])
def route():
    to_coords = request.json

    long = redis_server.get('longitude')
    lat = redis_server.get('latitude')
    battery = redis_server.get('battery')
    
    print('Nu kör jag')

    subprocess.Popen(["python3", "simulator.py", '--clong', long, '--clat', lat,
                                                 '--tlong', str(to_coords[0]), '--tlat', str(to_coords[1]),
                                                 '--ip', myIP, '--battery', battery
                    ])
    
    return 'New route received'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
