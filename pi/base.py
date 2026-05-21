from flask import Flask, request
from flask_cors import CORS
import subprocess
import redis

redis_server = redis.Redis('localhost', decode_responses=True)

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

myIP = '192.168.0.3'

@app.route('/base', methods=['POST'])
def main():
    base_coords = request.json
    
    redis_server.set('base_long', base_coords[0])
    redis_server.set('base_lat', base_coords[1])
    
    if redis_server.get('status') == 'idle':
        redis_server.set('longitude', base_coords[0])
        redis_server.set('latitude', base_coords[1])
            
    return 'New base coords registered'

@app.route('/ping', methods=['POST'])
def ping():
    return 'ping'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

