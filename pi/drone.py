from flask import Flask, request
from flask_cors import CORS
import subprocess
import redis

redis_server = redis.Redis('localhost', decode_responses=True)

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

myIP = '192.168.0.5'
battery = 100.0

@app.route('/', methods=['POST']) #Körs i new_drone
def main():
    coords = request.json
    
    redis_server.set('longitude', coords[0])
    redis_server.set('latitude', coords[1])
    redis_server.set('battery', battery)
    redis_server.set('base_long', coords[0])
    redis_server.set('base_lat', coords[1])

#    with open('data.txt', 'w') as f:
#        print(str(coords[0]) + "\n" + str(coords[1]))
#        f.write(str(coords[0]) + "\n" + str(coords[1]))
    
#    with open('base.txt', 'w') as f:
#        f.write(str(coords[0]) + "\n" + str(coords[1]))
        
    return 'OK'

@app.route('/route', methods=['POST'])
def route():
    to_coords = request.json

    long = redis_server.get('longitude')
    lat = redis_server.get('latitude')
    battery = redis_server.get('battery')

#    f = open("data.txt")
#    
#    current_longitude = float(f.readline())
#    current_latitude = float(f.readline())
#    
#    f.close()
    
    print('Nu kör jag')

    subprocess.Popen(["python3", "simulator.py", '--clong', long, '--clat', lat,
                                                 '--tlong', str(to_coords[0]), '--tlat', str(to_coords[1]),
                                                 '--ip', myIP, '--battery', battery
                    ])
    
    return 'New route received'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
