from flask import Flask, request
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

myIP = '192.168.0.3'
battery = 100.0

@app.route('/', methods=['POST']) #Körs i new_drone
def main():
    coords = request.json

    with open('data.txt', 'w') as f:
        print(str(coords[0]) + "\n" + str(coords[1]))
        f.write(str(coords[0]) + "\n" + str(coords[1]))
    
    with open('base.txt', 'w') as f:
        f.write(str(coords[0]) + "\n" + str(coords[1]))
        
    return 'OK'

@app.route('/route', methods=['POST'])
def route():
    to_coords = request.json

    f = open("data.txt")
    
    current_longitude = float(f.readline())
    current_latitude = float(f.readline())
    
    f.close()
    print('Nu kör jag')

    subprocess.Popen(["python3", "simulator.py", '--clong', str(current_longitude), '--clat', str(current_latitude),
                                                 '--tlong', str(to_coords[0]), '--tlat', str(to_coords[1]),
                                                 '--ip', myIP, '--battery', str(battery)
                    ])
    
    return 'New route received'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
